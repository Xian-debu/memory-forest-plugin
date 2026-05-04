---
id: EXP-PAT-0015
name: xgboost-gpu-pytorch-compatibility
description: XGBoost GPU 集成在 PyTorch 框架中的完整兼容性方案 — 显存管理 + CPU迁移后的推理/特征提取陷阱
type: PATTERN
tree: experiences
layer: L3
status: ACTIVE
created: 2026-05-03
heartbeat: '2026-05-05'
priority: HIGH
owner: claude-code
parent: EXP-ROOT-0000
originSessionId: CURRENT
tags:
- xgboost
- cuda
- gpu-memory
- dataloader
- optuna
- pytorch
- feature-extraction
- numpy
---
# XGBoost GPU 集成 + PyTorch 兼容性完整方案

## Part A: GPU 显存累积泄漏 → cudaErrorInitializationError

### 根因
XGBoost 用 `device='cuda'` 训练后，`XGBClassifier` 对象（含内部 booster CUDA buffer）一直留在 GPU 上。
多 trial × 多 fold 循环后 GPU 显存碎片化，后续 trial 的 XGBoost 无法分配连续 GPU 内存，抛出:

```
cudaErrorInitializationError: initialization error
  at host_device_vector.cu:267
```

**不是 fork 问题**。Trial 0-6 用 `num_workers=4` 正常工作，Trial 7 才崩溃，说明是累积效应。

每次崩溃的 worker 进程在 WSL2 下生成 ~10GB crash dump，会快速塞满 C 盘。

### 三层修复

#### 1. Booster GPU→CPU 迁移 (根因修复)
在 `xgb_fit()` 训练完成后立即:
```python
raw = self._model.get_booster().save_raw()
self._cpu_booster = xgb.Booster(model_file=raw)
self._cpu_booster.set_param({'device': 'cpu', 'tree_method': 'hist'})
del self._model  # 释放 GPU 上的 XGBClassifier
gc.collect(); torch.cuda.empty_cache()
```

推理时用 CPU booster + `xgb.DMatrix`，XGBoost 推理在 CPU 上足够快。

#### 2. pin_memory=False (减少 CUDA 接触面)
XGBoost 的特征提取走 numpy FFT，DataLoader 产出的 tensor 立刻转 numpy。
`pin_memory=True` 没必要且让 worker 进程触碰 CUDA pinned memory。
```python
pin_mem = not _is_tree  # XGBoost: False, 神经网络: True
```

**保留 `num_workers > 0`**，I/O 并行对 267K 样本至关重要。

#### 3. Trial 间 GPU 清理 (防御层)
每个 Optuna trial 前后:
```python
torch.cuda.empty_cache()
torch.cuda.synchronize()
gc.collect()
```

## Part B: CPU 迁移后的下游兼容性陷阱

Part A 的 Booster CPU 迁移解决后，会暴露两个下游问题:

### 陷阱 1: forward() 中 .numpy() 前缺 .cpu()

推理时 `forward()` 被 K-Fold 测试评估调用：
- kfold.py 显式 `signals.to(device)` 把数据搬到 GPU
- extractor 在 GPU 上运行，返回 CUDA tensor
- `.numpy()` 直接调用 → `TypeError: can't convert cuda:0 device type tensor to numpy`

**修复**: 所有推断路径的 `.numpy()` 前加 `.cpu()`:
```python
# forward()
feats = self.extractor(x).cpu().numpy()

# xgb_fit() 训练/验证特征提取
X_train_list.append(feats.cpu().numpy())
```

`xgb_fit()` 中 DataLoader 的 `pin_memory=False` 保证 signals 是 CPU tensor，extractor 正常运行。但 `.cpu()` 对 CPU tensor 是 no-op，加上无害。

### 陷阱 2: _default_feature_extractor 找 nn.Linear → 失败

`_default_feature_extractor` 寻找最后一个 `nn.Linear` 层 hook 提取特征（用于 t-SNE/UMAP 可视化和域偏移诊断）。XGBoost 模型没有 `nn.Linear` → `ValueError: Default feature extractor requires at least one nn.Linear layer.`

**修复**: 在入口检测 XGBoost 模型，直接用 `model.extractor` 提取:
```python
is_tree = getattr(model, 'is_xgboost', False)
if is_tree and hasattr(model, 'extractor'):
    return _extract_via_model_extractor(model, dataset, device, batch_size)
```

`_extract_via_model_extractor` 直接调用 `model.extractor(signals)` → `.cpu().numpy()` 获取特征，绕过 hook 机制。

## 适用场景
- PyTorch 框架中集成 GPU XGBoost/LightGBM/cuML
- Optuna/K-Fold 循环中多次创建 GPU 模型
- WSL2 环境 (crash dump 问题更严重)
- 树模型包装为 nn.Module 后的 t-SNE/UMAP 可视化
- 域偏移诊断等依赖特征提取的辅助功能

## 本案例
Hawk/Hawk-II (XGBoost GPU, `device='cuda'`, `tree_method='hist'`):
25 trial × 5 fold CV, Trial 7 崩溃。修复涉及 `net_define_hawk.py`、`net_define_hawk2.py`、`trainer.py`、`objective.py`、`kfold.py`、`ensemble.py`、`tsne_umap.py` 共 7 个文件，分两阶段完成（Part A 修复显存泄漏，Part B 修复 CPU 迁移后的推理和特征提取路径）。
