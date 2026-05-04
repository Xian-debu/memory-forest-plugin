---
id: EXP-PAT-0020
name: batch-notebook-resilience
description: Jupyter notebook 无人值守批量执行 — try/except/finally 容错 + GPU 强制清理 + sys.modules
  跨 cell 缓存
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
- jupyter
- notebook
- batch-execution
- gpu-memory
- resilience
- caching
- fire-and-forget
---
# Notebook 无人值守批量执行 + 跨 Cell 数据集缓存

## 场景

在一个 Jupyter notebook 中顺序执行多个模型的训练（如 16 个模型的超参搜索 + K-Fold 训练），需要：
1. 每个模型独立搜索，跑完自动切下一个
2. 任一模型崩溃不影响后续模型
3. GPU 显存在 cell 间强制清空，不累积泄漏
4. 大数据集只加载一次，后续 cell 直接复用

## 问题

直接 `%run run.py --model X` 串联 16 个 cell 有三个致命隐患：
1. **单点崩溃阻断全链** — 第 3 个模型 OOM，第 4-16 全部跳过
2. **GPU 显存残留** — 上一个模型的 `fold_models` 列表持有 K 个 model 实例（含 GPU tensor），cell 结束时 GC 时机不确定，下一个模型可能因显存不足直接 OOM
3. **数据集重复加载** — 每个 `%run` 是独立命名空间，267K 样本 × 850 采样点 × 2 通道的数据集每个 cell 加载一次，浪费 I/O 时间

## 三层修复

### 1. try/except/finally 容错

在 `run.py` 中将训练管道（搜索 + 训练 + 可视化 + 诊断）整体包裹：

```python
fold_models = None
fold_results = None

try:
    study, best_params, _ = run_optuna(...)
    fold_models, fold_results, ensemble_results, final_config, _ = bayes_to_training(...)
    visualize_tsne_umap_generic(...)
    diagnose_domain_shift_from_checkpoint(...)
except Exception as e:
    print(f"[FAIL] {model_name} 异常中断: {type(e).__name__}: {e}")
    traceback.print_exc()
    # 不调 sys.exit() — 脚本正常返回，notebook 继续下一个 cell
finally:
    _force_cleanup(fold_models, fold_results, ensemble_results)
```

**关键**: `sys.exit(0)` vs 直接 `return` — 用 `return` 让脚本正常退出，notebook 无缝切入下一个 cell。

### 2. 显式 GPU 清理

`finally` 块中的清理必须：
- `list.clear()` + `del` 模型列表（解除 Python 层引用）
- `_cleanup_dataloaders()` 关闭残留 worker 子进程
- `gc.collect()` 触发 `DataLoader.__del__`
- `torch.cuda.empty_cache()` 释放 PyTorch 缓存分配器持有的显存
- `torch.cuda.synchronize()` 确保所有 CUDA 流完成

```python
def _force_cleanup(fold_models=None, fold_results=None, ensemble_results=None):
    for obj in (fold_models, fold_results, ensemble_results):
        if obj is not None:
            if isinstance(obj, list):
                obj.clear()
            del obj
    try:
        _cleanup_dataloaders()
    except Exception:
        pass
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
```

### 3. sys.modules 跨 cell 缓存

`%run` 每次创建独立命名空间，但 `sys.modules` 在整个 kernel 生命周期内持久存在。利用这一点：

```python
# io_utils.py — 模块级全局变量
_cached_train_set = None
_cached_test_set = None

def cache_datasets(train_set, test_set, data_root):
    global _cached_train_set, _cached_test_set
    _cached_train_set = train_set
    _cached_test_set = test_set

def get_cached_datasets(data_root):
    if _cached_train_set is None:
        raise RuntimeError("No cached datasets")
    return _cached_train_set, _cached_test_set
```

**为什么安全**: 
- `%run` 重新执行 `from io_utils import get_cached_datasets`，但 Python 发现 `io_utils` 已在 `sys.modules` 中，直接复用 — 不重新执行模块代码，全局变量保留
- 缓存的 dataset 是 CPU tensor（`PaderbornDataset` 存 numpy），不占 GPU 显存
- 类重定义不是问题：`PaderbornDataset` 类对象在 `sys.modules` 中是同一个，新旧 cell 引用一致

## Notebook 结构

```
Cell 1:  %run run.py --list-models          # 验证环境 + 预热 sys.modules
Cell 2:  %run run.py --model Hawk            # 加载数据 + 缓存 + 搜索 + 训练
Cell 3:  %run run.py --skip-load --model Hawk-II   # 复用数据
...
Cell 17: %run run.py --skip-load --model TWIESN    # 复用数据
```

Cell 1 提前触发所有 import（torch, experiment_framework, 所有 net_define），后续 cell 的 `%run` 只需绑定已缓存的模块名，启动更快。

## 适用场景

- Jupyter 中顺序执行多个独立训练任务
- 需要无人值守跑完的大型超参搜索
- 任何 `%run` 之间需要共享大对象的场景
- 数据加载耗时但多个脚本/配置共用同一份数据

## 反例

- 不包裹 try/except — 一个模型崩，整个 notebook 停
- 只调 `torch.cuda.empty_cache()` 不 `del` 模型 — 引用还在，显存不会被释放
- 每个 cell 重新 load 数据 — 16 个模型 = 16 次数据加载，每次几分钟，浪费数十分钟

## 相关经验

- [EXP-PAT-0015](xgboost-cuda-fork-conflict.md) — GPU 清理模式的底层原理 (`.cpu()`/`.numpy()` + CUDA fork 冲突)
- [EXP-PAT-0021](signature-body-drift.md) — 批量改造时的签名/函数体一致性检查
