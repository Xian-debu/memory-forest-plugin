---
id: PROJ-FWREF-0004
name: phase7-classifier-migration
description: 10 个 TF Keras 分类器翻译为 PyTorch net_define + ModelAdapter, 逐个翻译逐个验证
type: LEAF
tree: projects
layer: L2
status: ACTIVE
created: 2026-05-03
heartbeat: '2026-05-05'
priority: HIGH
owner: claude-code
parent: PROJ-FWREF-0000
originSessionId: 7ad82639-4dd4-4646-adf1-113d50b7d503
resumeSessionId: CURRENT
tags:
- classifier-migration
- tf2torch
- model-adapter
- MCNN-bugfix
---
# Phase 7: TF Keras 分类器 → PyTorch 迁移

## 目标
将 `/root/classifiers/` 下 10 个 TF/Keras 分类器逐个翻译为 PyTorch 实现，生成 `net_define_*.py` + `@register_adapter`，保证结构一致。

## 源文件: /root/classifiers/*.py (TF Keras)
## 目标: /root/project/framework/net_define_*.py (PyTorch) + experiment_framework/models/examples.py

## 迁移状态 (2026-05-03)

| # | 分类器 | 文件 | 方式 | 状态 | 备注 |
|---|--------|------|------|------|------|
| 1 | MLP | net_define_mlp → inline | inline | ✅ 完成 | 3-layer Dense(500)+Dropout |
| 2 | FCN | net_define_fcn → inline | inline | ✅ 完成 | Conv1D(128→256→128)+GAP |
| 3 | CNN | net_define_cnn → inline | inline | ✅ 完成 | 2 Conv1D(sigmoid)+AvgPool |
| 4 | ResNet | net_define_resnet.py | standalone | ✅ 完成 | 3 residual blocks 64→128→128 |
| 5 | Inception | net_define_inception.py | standalone | ✅ 完成 | InceptionTime multi-scale |
| 6 | Encoder | net_define_encoder.py | standalone | ✅ 完成 | CNN+Channel Attention |
| 7 | MCDCNN | net_define_mcdcnn.py | standalone | ✅ 完成 | Per-channel dual Conv1D(8,5) |
| 8 | MCNN | net_define_mcnn.py | standalone | ✅ 完成 | Multi-scale (raw+MA+DS) → 修复 3 bugs |
| 9 | TLENET | net_define_tlenet.py | standalone | ✅ 完成 | Conv1D(5→20)+MaxPool+Dense(500) |
| 10 | TWIESN | net_define_twiesn.py | standalone | ✅ 完成 | Echo State Network reservoir+Ridge |

## MCNN 修复 (2026-05-03)
容器版 net_define_mcnn.py 存在 3 个 bug:
1. **k2 计算错误**: `k2 = min(kernel_size, pool1_size)` 误用 pool 核大小(425) 而非分支输出长度(~pool_factor)
2. **pool2_size 计算错误**: 同样误用了 pool1_size
3. **Classifier 输入维度硬编码**: `Linear(256, 256)` 未考虑 Flatten 后的实际维度

修复: k2 = min(kernel_size, branch_out_len, 3), pool2 = max(1, branch_out_len // pool_factor),
_classifier_in = 256 * _final_len (含 PyTorch even-kernel same-padding 补偿)

## 验证方法
- 每个分类器: import + build_model + forward pass (多种config)
- 结构对比: TF Keras build_model() vs PyTorch __init__() 逐层对照
- 全量测试: `pytest tests/ -v` → 60/60 passed

## 环境
- 容器: docker exec dev
- Conda: my_torch (PyTorch 2.9.1+cu130)
- 测试路径: /root/project/experiment_framework_clean/
