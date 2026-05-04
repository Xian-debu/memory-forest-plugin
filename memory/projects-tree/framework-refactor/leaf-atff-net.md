---
id: PROJ-FWREF-0006
name: atff-net-innovation
description: ATFF-Net 创新网络模型 — 可学习 Gabor 滤波器组 + 跨频带注意力 + 多尺度扩张卷积 + 门控融合
type: LEAF
tree: projects
layer: L2
status: ACTIVE
created: 2026-05-03
heartbeat: '2026-05-05'
priority: HIGH
owner: claude-code
parent: PROJ-FWREF-0000
originSessionId: CURRENT
tags:
- innovation
- gabor-filter
- attention
- time-frequency
- dilated-conv
- bearing-diagnosis
---
# ATFF-Net: 自适应时频融合网络

## 设计动机
14 个已适配模型中，没有一个同时具备**可学习频率分解** + **跨频带交互建模**。
现有模型要么在时域操作 (CNN系列)，要么用固定 FFT 预处理 (FreqNet, Hawk)。

## 能力矩阵 (对比现有模型)
| 能力 | PureCNN | ResNet | Inception | FreqNet | MCNN | Hawk | ATFF |
|------|---------|--------|-----------|---------|------|------|------|
| 时域卷积 | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ |
| 频域处理 | — | — | — | 固定FFT | — | 固定FFT | **可学习** |
| 多尺度 | — | — | 固定核 | 多频段 | 固定核 | 多间隔 | **可学习扩张率** |
| 跨频带交互 | — | — | — | — | — | — | **✓** |
| 残差连接 | — | ✓ | — | — | — | — | ✓ |
| 自适应门控 | — | — | — | — | — | — | **✓** |

## 三大原创贡献
1. **可微分 Gabor 滤波器组**: 时频分析从预处理提升为网络第一层，滤波器参数端到端优化
2. **跨频带自注意力**: 显式建模轴承故障中的振幅调制效应，注意力权重可解释
3. **门控多尺度融合**: 频带级自适应特征选择，内生频谱显著性学习

## 架构概要
```
(B,C,L) → GaborFilterBank(K=16) → TemporalPool → CrossBandAttn(h=4) 
→ MultiScaleDilatedConv(d=[1,2,4,8]) → GatedFusion → Dropout → Linear
```
参数量: ~46K (与 FreqNet ~43K 同量级)

## 实现文件
- net_define_atff.py (模型 + 4-function interface)
- experiment_framework/models/examples.py (ATFFAdapter)

## 方向建议 (后续讨论)
- 精简版: 去掉跨频带注意力，保留 Gabor + 门控融合
- 增强版: 加入对比学习辅助损失
- 可解释性: 注意力权重可视化 + f_k 收敛分析
- 物理先验: 约束 f_k 初始化到轴承特征频率理论区间
