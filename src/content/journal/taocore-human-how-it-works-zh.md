---
title: "TaoCore‑Human 是怎么工作的（给年轻工程师看的版）"
date: 2026-04-05
description: "用很直白的话讲清楚图片/视频流程和安全规则。"
---

这篇讲 `taocore-human`，不讲花哨词，直接说它在做什么。

## 1. 一句话概括

它把照片/视频变成数字信号，建图，算稳定性，然后**不稳定就拒绝解释**。

流程图：

![TaoCore-Human pipeline](/diagrams/taocore-human-pipeline.svg)

## 2. 输入和适配器

### 照片文件夹

- 输入：一堆图片
- 适配器会按顺序读取，变成 `ImageFrame`
- 然后交给提取器算特征

简单示意：

```text
image_01.jpg → ImageFrame(index=0, data=HxWxC)
image_02.jpg → ImageFrame(index=1, data=HxWxC)
```

### 视频

- 输入：一个视频文件
- 读出每帧，转成 RGB
- 按时间切成窗口（有重叠）

窗口示意：

![Video windowing](/diagrams/video-windowing.svg)

## 3. 信号（提取器）

会输出这些数字信号：

- 人脸置信度
- 情绪相关的“代理值”（不是结论）
- 画面亮度、模糊度（质量）

默认可以用 **stub 提取器**（假的但可复现），方便测试。

## 4. 建图

### 照片流程

- 每个人 = 一个 `PersonNode`
- 同时出现就连边

示意：

```text
person_1 —— person_2
     |
  person_3
```

### 视频流程

有两层图：

1. 每个时间窗口一个小图
2. 全部窗口合成一个大图

这样可以看“时间上有没有稳定的趋势”。

## 5. 算指标

会复用 TaoCore 的指标：

- Balance：数值是否正常
- Cluster：有没有小团体
- Hub：谁更中心
- Flow（视频才有）：变化稳不稳

## 6. 稳定性判断

计算完后跑稳定性求解：

```text
x_{t+1} = f(x_t)
```

不稳定就直接拒绝。

## 7. 拒绝规则（很保守）

如果出现这些情况，就拒绝：

- 覆盖率不够
- 置信度不够
- 稳定性不收敛
- 视频波动太大

默认阈值：

- 照片：`min_images=3`，`min_coverage=0.3`，`min_confidence=0.5`
- 视频：`min_duration=10s`，`window_duration=5s`，`window_overlap=1s`

## 8. 一个小例子

假设 3 张照片：

```text
photo_1.jpg: person_1, person_2
photo_2.jpg: person_1
photo_3.jpg: person_1, person_2
```

那么：

```text
person_1 覆盖率 = 3/3
person_2 覆盖率 = 2/3
```

都通过阈值 → 允许解释。  
如果视频里波动很大，就会反过来拒绝。

## 9. 你该记住的点

- 这是“信号系统”，不是“读心术”
- 只做稳定性判断，不做确定结论
- 不稳就拒绝，这就是它的安全性

如果你想看更细的源码路径，我可以继续补充。
