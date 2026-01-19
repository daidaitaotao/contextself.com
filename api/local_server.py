#!/usr/bin/env python3
"""
Local development server for testing the analyze API.

Setup (using UV):
  1. uv sync                    # Install dependencies
  2. npm install                # Install Node dependencies

Run locally:
  Terminal 1: npm run dev                    # Astro on port 4321
  Terminal 2: uv run python api/local_server.py  # API on port 8000

Then open http://localhost:4321/analyze in your browser.
The page auto-detects localhost and routes to the local API server.
"""

import os
import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

# Add parent dir to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env.local
env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env.local')
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value.strip('"').strip("'")

# Import the analyze module
from analyze import analyze_image, decode_image, verify_api_key

class APIHandler(BaseHTTPRequestHandler):
    """Handle API requests locally."""

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self._set_cors_headers()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_POST(self):
        """Handle POST requests."""
        if self.path != '/api/analyze':
            self._send_error(404, "Not found")
            return

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
            import traceback
            traceback.print_exc()
            self._send_error(500, f"Internal server error: {str(e)}")

    def _send_json(self, status: int, data: dict):
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

    def log_message(self, format, *args):
        """Log HTTP requests."""
        print(f"[API] {self.address_string()} - {format % args}")


def main():
    port = int(os.environ.get('PORT', 8000))
    server = HTTPServer(('localhost', port), APIHandler)
    print(f"\n=== Local API Server ===")
    print(f"Running on http://localhost:{port}")
    print(f"API endpoint: http://localhost:{port}/api/analyze")
    print(f"API key: {os.environ.get('ANALYZE_API_KEY', '(not set)')[:10]}...")
    print(f"\nPress Ctrl+C to stop\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
