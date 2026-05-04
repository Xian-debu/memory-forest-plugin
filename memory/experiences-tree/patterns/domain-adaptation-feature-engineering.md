---
id: EXP-PAT-0014
name: domain-adaptation-feature-engineering
description: 跨领域特征工程迁移 — 保留分解哲学，用目标领域物理重新设计特征集
type: PATTERN
tree: experiences
layer: L3
status: ACTIVE
created: 2026-05-03
heartbeat: '2026-05-05'
priority: MEDIUM
owner: claude-code
parent: EXP-ROOT-0000
originSessionId: CURRENT
tags:
- feature-engineering
- domain-adaptation
- signal-processing
- xgboost
- bearing-diagnosis
---
# 跨领域特征工程迁移模式

## 问题
将一个场景的信号处理 pipeline 直接迁移到另一个场景时，即使核心算法相同，效果也常远不如源场景。

## 根因
信号处理流程中的**每一层**都隐式嵌入了源领域的物理假设：
- 差分间隔 → 匹配源领域的事件时间尺度
- 频域分析方式 → 匹配源领域的信号特征（瞬态 vs 周期）
- 特征选择 → 匹配源领域的判别维度

直接复制 pipeline = 把源领域的物理假设强加到目标领域。

## 正确做法
1. **保留分解哲学**（如多尺度差分、频域分解），不保留具体参数
2. **用目标领域物理重新设计**：
   - 时间尺度参数 → 匹配目标信号的特征周期
   - 频域特征 → 匹配目标信号的频域结构（调制边带 vs 直接频谱）
   - 特征类型 → 匹配目标领域的诊断工具（如包络解调对轴承故障是必须的）
3. **增量验证**：先验证特征工程的有效性（XGBoost 的 val_acc），再优化模型参数

## 本案例
Hawk (NILM) → Hawk-II (轴承诊断):
- 保留: 多尺度差分 + XGBoost 分类
- 适配: gap 范围扩大 (2-50 → 2-L/4), 加入 Hilbert 包络解调, 加入谱统计矩替代直接 FFT, 加入跨尺度/全局特征
- 效果: 特征从 30 维增强到 335 维, 物理可解释, GPU 加速

## 适用场景
- 信号处理 pipeline 跨领域迁移
- 传统机器学习特征工程转移到新问题
- 论文方法复现到不同数据集
