---
id: PROJ-FWREF-0005
name: hawk-xgboost-integration
description: Hawk XGBoost + FFT-differential 分类器接入框架，扩展训练管道支持非神经网络树模型
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
- hawk
- xgboost
- tree-model
- fft-differential
- non-neural
- trainer-extension
---
# Hawk XGBoost 分类器集成

## 目标
将 Hawk SenSys 论文的 XGBoost + FFT-differential 分类器 1:1 复刻到框架，并扩展训练管道支持非神经网络模型。

## Hawk 原始架构（来自 /root/Hawk/）
```
raw_current[t] → diff(curr[t+gap] - curr[t]) / 26214 → FFT(10 bins) →
[abs|imag|real] → concat(30-dim) → XGBClassifier(default params) → 37 classes
```

## 适配后的架构
```
(B,C,L) window → per-gap diff(x[:,:,gap:]-x[:,:,:-gap]) → FFT(10 bins) →
[abs|imag|real] → concat(C * n_gaps * fft_bins * 3 dim) → XGBClassifier → num_classes
```

## 新增/修改文件

### 新建
- **net_define_hawk.py**: HawkFeatureExtractor + HawkXGBModel(nn.Module) + 4-func interface
  - is_xgboost = True 信号触发 trainer 分叉
  - xgb_fit(): 收集 DataLoader → numpy → XGBClassifier.fit() → 返回标准 result dict
  - state_dict/load_state_dict 覆盖防止 PyTorch 误存 XGBoost 内部

### 修改
- **training/trainer.py**: train_one_fold_generic 开头添加 `if is_xgboost` 分支
  - 检测 → 委托 xgb_fit() → 跳过 PyTorch 训练循环
  - 返回格式兼容 kfold/Optuna 上层
- **models/examples.py**: 添加 HawkAdapter (@register_adapter)
  - fixed_config: gap_list=(2,6,10,16,20,30,40,50), fft_bins=10
  - param_space: n_estimators, max_depth, learning_rate, subsample, colsample_bytree, gamma, reg_alpha, reg_lambda

## Hawk 1:1 复刻要点
- XGBClassifier() 默认参数（与 Hawk 代码中的无参调用一致）
- 8 个差分间隔 [2,6,10,16,20,30,40,50]
- FFT 10 bins, abs+imag+real 拼接（但不做 DC 合并，因为轴承信号不需）
- 无 early_stopping（与 Hawk 原始训练一致）

## 适配差异
| 项目 | Hawk 原版 | 框架适配 |
|------|----------|---------|
| 输入 | 原始电流信号 16KHz | (B,C,L) 窗口化时间序列 |
| 归一化 | /26214 (ADC量程) | 不做（窗口已标准化） |
| DC合并 | bin0+=bin1, bin10+=bin11, bin20+=bin21 | 不做（保留全频信息） |
| 后处理 | 阈值事件检测 (NILM专用) | 直接用 predict() 输出 |
| 输出 | 36+1=37类 | num_classes (可配置) |

## 验证
- import + forward pass + xgb_fit 通过
- Adapter 注册 + get_model_spec 通过
- train_one_fold_generic XGBoost 分支通过
- 60/60 测试无回归
- 14 模型全部可发现

## Phase 10 GPU 兼容性热修复 (2026-05-03)
- **Part A** (EXP-PAT-0015): Booster GPU→CPU 迁移防显存泄漏, pin_memory=False, trial 间 GPU 清理
- **Part B**: forward()/xgb_fit() 中 `.numpy()` 前加 `.cpu()` 防 CUDA tensor 错误; tsne_umap.py `_default_feature_extractor` 加 XGBoost 检测分支 (无 nn.Linear → 直接用 model.extractor)
- 修复涉及: net_define_hawk.py (3处), tsne_umap.py (2处), kfold.py

## 环境
- XGBoost 3.2.0 (pip install xgboost in my_torch env)
