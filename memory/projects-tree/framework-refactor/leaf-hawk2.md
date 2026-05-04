---
id: PROJ-FWREF-0007
name: hawk2-multi-domain-features
description: Hawk-II: 多域多尺度特征提取 + GPU XGBoost，从 NILM 瞬态检测适配到轴承故障周期冲击诊断
type: LEAF
tree: projects
layer: L2
status: COMPLETED
created: 2026-05-03
heartbeat: '2026-05-03'
priority: HIGH
owner: claude-code
parent: PROJ-FWREF-0000
originSessionId: CURRENT
tags:
- hawk2
- xgboost
- multi-domain
- envelope-demodulation
- hilbert
- multi-scale
- feature-engineering
- gpu
---

# Hawk-II: 多域多尺度特征提取 + XGBoost

## 动机
Hawk (FFT-differential + XGBoost) 直接复刻到轴承场景效果不理想。
核心原因: NILM 关注瞬态阶跃，轴承故障关注周期冲击调制。
保留 Hawk 的多尺度分解哲学，重新设计面向轴承物理的特征集。

## 设计演进

| 维度 | Hawk (NILM) | Hawk-II (轴承) |
|------|------------|---------------|
| 分解方式 | 差分 only (8 gaps) | 差分 + 滑动平均, raw + envelope 双分支 |
| 频域分析 | FFT abs/imag/real | 谱统计矩 (质心/扩展/偏度/峰度) |
| 包络解调 | 无 | Hilbert 变换 → 暴露故障调制 |
| Gap 范围 | 2-50 (0.03-0.78ms) | 2-L/4 (覆盖 BPFI/BSF 周期) |
| 特征维度 | 30 (固定) | ~335 (时域6+频域4 per scale, +交叉+全局) |
| 物理先验 | 无 | 峰度检测冲击, 包络谱检测故障周期, SNR估计 |

## 数学依据
1. **包络解调**: 故障冲击调制供电频率 → Hilbert包络 → 故障频率成为基频而非边带
2. **谱峰度**: 正常轴承频谱平坦(高熵), 故障轴承冲击产生尖锐峰值(高峰度)
3. **多尺度对准**: 不同 gap 对应不同故障周期 — BPFI(~0.8ms)用细尺度, BPFO(~11ms)用粗尺度

## 架构
```
(B,C,L) → per-channel Hilbert envelope
        → raw scales (diff[5gaps] + MA[2kernels] + id)
        → env scales  (diff[5gaps] + MA[2kernels] + id)
        → per-scale: time(6) + freq(4) = 10 features
        → cross-scale: RMS比 + 峰度比 + fine/coarse比
        → global: 通道能量/主导频率/SNR/互相关
        → XGBoost (GPU, ~335d → num_classes)
```

## 文件
- net_define_hawk2.py (Hawk2FeatureExtractor + Hawk2XGBModel + 4-func interface)
- experiment_framework/models/examples.py (Hawk2Adapter)

## 验证
- 自测: 特征提取(无NaN/Inf, 确定性), 前向传播, builder, vis extractor, 多形状兼容
- 框架集成: 16模型可发现, GPU XGBoost训练正常

## Phase 10 GPU 兼容性热修复 (2026-05-03)
- forward() 中 `self.extractor(x).numpy()` → `.cpu().numpy()` (CUDA tensor 兼容)
- xgb_fit() 训练/验证特征提取 `.numpy()` → `.cpu().numpy()`
- 域偏移诊断: tsne_umap.py 添加 XGBoost extractor 直接调用分支 (绕过 nn.Linear 查找)
- 修复涉及: net_define_hawk2.py (3处), tsne_umap.py
