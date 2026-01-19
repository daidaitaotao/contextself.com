"""
Single image analysis API endpoint.

Analyzes an uploaded image using taocore-human extractors and returns
geometric signals and behavioral patterns without interpretation.
"""

import os

# Configure writable directories for serverless environment
# Must be set BEFORE importing MediaPipe
os.environ["HOME"] = "/tmp"
os.environ["XDG_CACHE_HOME"] = "/tmp/.cache"
os.environ["MEDIAPIPE_RESOURCE_DIR"] = "/tmp/mediapipe"

import json
import base64
from http.server import BaseHTTPRequestHandler
from typing import Dict, Any, Optional
import numpy as np

# Import taocore-human extractors
TAOCORE_AVAILABLE = False
MEDIAPIPE_AVAILABLE = False
CLIP_AVAILABLE = False

try:
    from taocore_human.extractors import MediaPipeExtractor, StubExtractor
    from taocore_human.extractors.base import FaceDetection, PoseDetection, SceneFeatures
    TAOCORE_AVAILABLE = True
    MEDIAPIPE_AVAILABLE = MediaPipeExtractor is not None
except ImportError:
    pass

# CLIP requires torch/transformers - import separately to handle missing deps
try:
    from taocore_human.extractors import CLIPSceneExtractor
    CLIP_AVAILABLE = True
except (ImportError, Exception):
    # torch/transformers not available - CLIP disabled
    CLIPSceneExtractor = None
    CLIP_AVAILABLE = False


def verify_api_key(request_key: Optional[str]) -> bool:
    """Verify the provided API key against the environment variable."""
    expected_key = os.environ.get("ANALYZE_API_KEY")
    if not expected_key:
        # If no API key is configured, reject all requests
        return False
    return request_key == expected_key


def decode_image(image_data: str) -> tuple[np.ndarray, dict]:
    """Decode base64 image data to numpy array and extract metadata."""
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    import io

    # Register HEIC support
    try:
        from pillow_heif import register_heif_opener
        register_heif_opener()
    except ImportError:
        pass  # HEIC support not available

    try:
        # Remove data URL prefix if present (e.g., "data:image/png;base64,...")
        if "," in image_data:
            # Get the base64 part after the comma
            image_data = image_data.split(",", 1)[1]

        # Remove any whitespace that might have been introduced
        image_data = image_data.strip().replace(" ", "+").replace("\n", "").replace("\r", "")

        # Add padding if needed (base64 should be multiple of 4)
        padding = 4 - (len(image_data) % 4)
        if padding != 4:
            image_data += "=" * padding

        # Decode base64
        image_bytes = base64.b64decode(image_data)

        # Check if we got any data
        if len(image_bytes) == 0:
            raise ValueError("Empty image data after base64 decode")

        # Convert to numpy array using PIL
        buffer = io.BytesIO(image_bytes)
        image = Image.open(buffer)

        # Extract EXIF metadata
        metadata = extract_image_metadata(image)

        # Convert to RGB if needed (handles RGBA, grayscale, etc.)
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGB')

        return np.array(image), metadata
    except base64.binascii.Error as e:
        raise ValueError(f"Invalid base64 encoding: {str(e)}")
    except Image.UnidentifiedImageError:
        raise ValueError("Cannot identify image format. Supported formats: PNG, JPEG, GIF, BMP, WebP")
    except Exception as e:
        raise ValueError(f"Failed to decode image: {str(e)}")


def extract_image_metadata(image) -> dict:
    """Extract EXIF and other metadata from PIL Image."""
    from PIL.ExifTags import TAGS, GPSTAGS, IFD
    from datetime import datetime

    metadata = {
        "date_taken": None,
        "date_taken_raw": None,
        "camera_make": None,
        "camera_model": None,
        "gps_latitude": None,
        "gps_longitude": None,
        "orientation": None,
        "width": image.width,
        "height": image.height,
    }

    try:
        # Try getexif() first (works for HEIC and newer formats)
        exif_data = image.getexif()
        if not exif_data:
            # Fallback to _getexif() for older JPEG handling
            try:
                exif_data = image._getexif()
            except AttributeError:
                exif_data = None

        if exif_data:
            # Map tag IDs to names
            exif = {}
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                exif[tag] = value

            # Try to get EXIF IFD for DateTimeOriginal
            try:
                exif_ifd = exif_data.get_ifd(IFD.Exif)
                if exif_ifd:
                    for tag_id, value in exif_ifd.items():
                        tag = TAGS.get(tag_id, tag_id)
                        exif[tag] = value
            except (AttributeError, KeyError):
                pass

            # Date taken (try multiple fields)
            for date_field in ['DateTimeOriginal', 'DateTime', 'DateTimeDigitized']:
                if date_field in exif:
                    date_str = exif[date_field]
                    metadata["date_taken_raw"] = str(date_str)
                    try:
                        # Parse EXIF date format: "2024:01:15 14:30:00"
                        dt = datetime.strptime(str(date_str), "%Y:%m:%d %H:%M:%S")
                        metadata["date_taken"] = dt.isoformat()
                    except (ValueError, TypeError):
                        pass
                    break

            # Camera info
            metadata["camera_make"] = str(exif.get("Make", "")) or None
            metadata["camera_model"] = str(exif.get("Model", "")) or None
            metadata["orientation"] = exif.get("Orientation")

            # GPS data - try get_ifd for GPS
            gps_info = None
            try:
                gps_info = exif_data.get_ifd(IFD.GPSInfo)
            except (AttributeError, KeyError):
                gps_info = exif.get("GPSInfo")

            if gps_info:
                gps = {}
                for key, val in gps_info.items():
                    gps_tag = GPSTAGS.get(key, key)
                    gps[gps_tag] = val

                # Convert GPS coordinates
                if "GPSLatitude" in gps and "GPSLatitudeRef" in gps:
                    lat = _convert_gps_to_decimal(gps["GPSLatitude"])
                    if lat is not None and gps["GPSLatitudeRef"] == "S":
                        lat = -lat
                    metadata["gps_latitude"] = lat

                if "GPSLongitude" in gps and "GPSLongitudeRef" in gps:
                    lon = _convert_gps_to_decimal(gps["GPSLongitude"])
                    if lon is not None and gps["GPSLongitudeRef"] == "W":
                        lon = -lon
                    metadata["gps_longitude"] = lon

    except Exception as e:
        pass  # EXIF extraction failed, return what we have

    return metadata


def _convert_gps_to_decimal(gps_coords) -> float:
    """Convert GPS coordinates from degrees/minutes/seconds to decimal."""
    try:
        d, m, s = gps_coords
        # Handle IFDRational objects
        if hasattr(d, 'numerator'):
            d = d.numerator / d.denominator
        if hasattr(m, 'numerator'):
            m = m.numerator / m.denominator
        if hasattr(s, 'numerator'):
            s = s.numerator / s.denominator
        return d + m / 60 + s / 3600
    except Exception:
        return None


def face_detection_to_dict(det: "FaceDetection") -> Dict[str, Any]:
    """Convert FaceDetection to serializable dict."""
    result = {
        "confidence": det.confidence,
        "bounding_box": det.bounding_box,
        "track_id": det.track_id,
        # Expression signals
        "valence": det.valence,
        "arousal": det.arousal,
        "smile_intensity": det.smile_intensity,
        # Head pose
        "head_yaw": det.head_yaw,
        "head_pitch": det.head_pitch,
        "head_roll": det.head_roll,
        # Eye features
        "left_eye_openness": getattr(det, "left_eye_openness", None),
        "right_eye_openness": getattr(det, "right_eye_openness", None),
        "gaze_direction": getattr(det, "gaze_direction", None),
        # Mouth features
        "mouth_openness": getattr(det, "mouth_openness", None),
        "jaw_open": getattr(det, "jaw_open", None),
        # Full blendshapes (52 Action Units from MediaPipe)
        "blendshapes": getattr(det, "blendshapes", None),
    }
    # Convert gaze_direction tuple to list for JSON
    if result["gaze_direction"] is not None:
        result["gaze_direction"] = list(result["gaze_direction"])
    return result


def pose_detection_to_dict(det: "PoseDetection") -> Dict[str, Any]:
    """Convert PoseDetection to serializable dict."""
    # Convert keypoints tuples to lists for JSON serialization
    keypoints = {k: list(v) for k, v in det.keypoints.items()}
    return {
        "confidence": det.confidence,
        "bounding_box": det.bounding_box,
        "track_id": det.track_id,
        "keypoints": keypoints,
        "posture_openness": det.posture_openness,
        "movement_energy": det.movement_energy,
    }


def scene_features_to_dict(scene: "SceneFeatures") -> Dict[str, Any]:
    """Convert SceneFeatures to serializable dict."""
    return {
        "confidence": scene.confidence,
        "illumination": scene.illumination,
        "blur_level": scene.blur_level,
        "camera_motion": scene.camera_motion,
        "scene_type_probs": scene.scene_type_probs,
    }


def generate_observable_summary(faces: list, poses: list) -> Dict[str, Any]:
    """
    Generate a narrative summary of observable signals.
    Describes what is observed without interpreting meaning.
    """
    observations = []
    face_details = []

    for i, face in enumerate(faces):
        face_obs = []

        # Smile
        if face.smile_intensity is not None:
            if face.smile_intensity > 0.7:
                face_obs.append("mouth corners raised significantly (strong smile pattern)")
            elif face.smile_intensity > 0.4:
                face_obs.append("mouth corners moderately raised (smile pattern)")
            elif face.smile_intensity > 0.2:
                face_obs.append("slight upward curve at mouth corners")
            else:
                face_obs.append("neutral mouth position")

        # Eye openness
        left_eye = getattr(face, "left_eye_openness", None)
        right_eye = getattr(face, "right_eye_openness", None)
        if left_eye is not None and right_eye is not None:
            avg_eye = (left_eye + right_eye) / 2
            if avg_eye < 0.3:
                face_obs.append("eyes nearly closed or squinting")
            elif avg_eye > 0.8:
                face_obs.append("eyes wide open")

        # Gaze
        gaze = getattr(face, "gaze_direction", None)
        if gaze is not None:
            gx, gy = gaze
            if abs(gx) < 0.1 and abs(gy) < 0.1:
                face_obs.append("gaze directed toward camera")
            elif gx > 0.2:
                face_obs.append("gaze directed to the right")
            elif gx < -0.2:
                face_obs.append("gaze directed to the left")
            if gy > 0.2:
                face_obs.append("gaze directed downward")
            elif gy < -0.2:
                face_obs.append("gaze directed upward")

        # Head orientation
        if face.head_yaw is not None:
            import math
            yaw_deg = math.degrees(face.head_yaw)
            if abs(yaw_deg) > 20:
                direction = "right" if yaw_deg > 0 else "left"
                face_obs.append(f"head turned {direction} ({abs(yaw_deg):.0f}°)")

        if face.head_pitch is not None:
            import math
            pitch_deg = math.degrees(face.head_pitch)
            if pitch_deg > 15:
                face_obs.append("head tilted back")
            elif pitch_deg < -15:
                face_obs.append("head tilted forward")

        # Mouth
        mouth = getattr(face, "mouth_openness", None)
        if mouth is not None and mouth > 0.3:
            face_obs.append("mouth open")

        # Blendshapes highlights
        blendshapes = getattr(face, "blendshapes", None)
        if blendshapes:
            # Check for notable expressions
            brow_down = max(
                blendshapes.get("browDownLeft", 0),
                blendshapes.get("browDownRight", 0)
            )
            brow_up = max(
                blendshapes.get("browInnerUp", 0),
                blendshapes.get("browOuterUpLeft", 0),
                blendshapes.get("browOuterUpRight", 0)
            )
            if brow_down > 0.4:
                face_obs.append("eyebrows lowered/furrowed")
            elif brow_up > 0.4:
                face_obs.append("eyebrows raised")

            cheek_squint = max(
                blendshapes.get("cheekSquintLeft", 0),
                blendshapes.get("cheekSquintRight", 0)
            )
            if cheek_squint > 0.4:
                face_obs.append("cheeks raised (eye crinkle)")

        face_details.append({
            "face_index": i,
            "observations": face_obs,
            "summary": "; ".join(face_obs) if face_obs else "neutral expression"
        })

    # Pose observations
    pose_details = []
    for i, pose in enumerate(poses):
        pose_obs = []

        if pose.posture_openness is not None:
            if pose.posture_openness > 0.7:
                pose_obs.append("arms spread wide (open posture)")
            elif pose.posture_openness > 0.4:
                pose_obs.append("moderately open arm position")
            else:
                pose_obs.append("arms close to body (closed posture)")

        pose_details.append({
            "pose_index": i,
            "observations": pose_obs,
            "summary": "; ".join(pose_obs) if pose_obs else "standard standing position"
        })

    return {
        "faces": face_details,
        "poses": pose_details,
        "overall": f"Detected {len(faces)} face(s) and {len(poses)} body pose(s)."
    }


def analyze_image(image: np.ndarray, metadata: Optional[dict] = None) -> Dict[str, Any]:
    """Analyze a single image using taocore-human extractors."""
    if metadata is None:
        metadata = {}

    if not TAOCORE_AVAILABLE:
        return {
            "error": "taocore-human not available",
            "message": "The analysis library is not installed on this server."
        }

    # Use MediaPipe for real face/pose detection
    if MEDIAPIPE_AVAILABLE:
        extractor = MediaPipeExtractor()
        faces = extractor.face.extract(image)
        poses = extractor.pose.extract(image)
    else:
        stub = StubExtractor(seed=42)
        faces = stub.face.extract(image)
        poses = stub.pose.extract(image)

    # Use CLIP for scene classification, fall back to stub
    if CLIP_AVAILABLE:
        scene_extractor = CLIPSceneExtractor()
        scene = scene_extractor.extract(image)
    else:
        stub = StubExtractor(seed=42)
        scene = stub.scene.extract(image)

    # Generate observable summary (narrative descriptions)
    observable_summary = generate_observable_summary(faces, poses)

    # Build result
    result = {
        "status": "success",
        "disclaimer": (
            "These are geometric signals and behavioral patterns, not interpretations. "
            "The numbers describe what was detected, not what it means. "
            "Context, culture, and individual variation affect meaning."
        ),
        "image_info": {
            "shape": list(image.shape),
            "dtype": str(image.dtype),
            "date_taken": metadata.get("date_taken"),
            "camera_make": metadata.get("camera_make"),
            "camera_model": metadata.get("camera_model"),
            "gps_latitude": metadata.get("gps_latitude"),
            "gps_longitude": metadata.get("gps_longitude"),
        },
        "observable_summary": observable_summary,
        "faces": {
            "count": len(faces),
            "detections": [face_detection_to_dict(f) for f in faces],
            "note": "Faces detected with geometric features. Expression signals (valence, arousal) are statistical patterns, not definitive emotions.",
        },
        "poses": {
            "count": len(poses),
            "detections": [pose_detection_to_dict(p) for p in poses],
            "note": "Body pose keypoints. Posture features are geometric measurements.",
        },
        "scene": {
            "features": scene_features_to_dict(scene),
            "note": "Scene-level technical quality indicators.",
        },
        "cannot_determine": [
            "What anyone is actually feeling",
            "Intent or motivation",
            "Whether expressions are genuine",
            "Relationship types between people",
            "Cultural context",
            "What happened before or after this moment",
        ],
    }

    return result


class handler(BaseHTTPRequestHandler):
    """Vercel serverless function handler."""

    def do_POST(self):
        """Handle POST request with image data."""
        try:
            # Check API key
            api_key = self.headers.get("X-API-Key")
            if not verify_api_key(api_key):
                self._send_error(401, "Invalid or missing API key")
                return

            # Read request body
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            # Parse JSON body
            try:
                data = json.loads(body.decode("utf-8"))
            except json.JSONDecodeError:
                self._send_error(400, "Invalid JSON in request body")
                return

            # Get image data
            image_data = data.get("image")
            if not image_data:
                self._send_error(400, "No 'image' field in request body")
                return

            # Decode image
            try:
                image, metadata = decode_image(image_data)
            except ValueError as e:
                self._send_error(400, str(e))
                return

            # Analyze image
            result = analyze_image(image, metadata)

            # Send response
            self._send_json(200, result)

        except Exception as e:
            self._send_error(500, f"Internal server error: {str(e)}")

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self._set_cors_headers()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _send_json(self, status: int, data: Dict[str, Any]):
        """Send JSON response."""
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self._set_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, status: int, message: str):
        """Send error response."""
        self._send_json(status, {"error": message})

    def _set_cors_headers(self):
        """Set CORS headers for browser requests."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-API-Key")
