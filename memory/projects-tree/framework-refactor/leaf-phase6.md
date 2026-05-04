---
id: PROJ-FWREF-0003
type: LEAF
tree: projects
layer: L2
status: COMPLETED
created: 2026-05-02
heartbeat: '2026-05-02'
priority: HIGH
owner: claude-code
parent: PROJ-FWREF-0000
originSessionId: 0f9a3b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
---
# Phase 6: Clean 版本审查与修复

## 审查范围
容器内 `/root/project/experiment_framework_clean/` 的全部 31 模块 + 顶层文件。

## 已修复的 Bug

### 严重
- **silhouette_score intra_mask 共享 mutation**: `intra_mask = mask_k.clone()` 在 per-class 循环外，同一类所有样本共用累积修改的 mask，导致当 batch_size ≥ n 时 a_vals 恒为 0，silhouette 始终返回 1.0。修复：将 clone 移入 per-sample 循环。

### 中等
- **torch.cuda.amp 弃用**: trainer.py 中 `torch.cuda.amp.GradScaler` → `torch.amp.GradScaler('cuda', ...)`，`torch.cuda.amp.autocast` → `torch.amp.autocast('cuda', ...)`
- **重复 _optuna_prune**: trainer.py 和 objective.py 各有一份同等定义，改为 objective.py 从 trainer.py import
- **_format_trial_params 不可达 else 分支**: 三路 if-elif-else 的 else 永远不可达，简化为二路

### 轻微
- **bare import net_define_freqnet**: examples.py 中的 import 依赖 sys.path 魔术，添加了显式 sys.path 插入兜底
- **未使用 import**: config.py (gc, numpy, os, time, json → 全删), resources.py (os, time, json → 删), objective.py (assemble_config → 删)
- **垃圾文件**: __pycache__/ 和 .ipynb_checkpoints/ 从宿主机和容器清理

## 新测试覆盖 (34 tests)

| 文件 | Tests | 覆盖模块 |
|------|-------|----------|
| test_adapter.py | 14 | ModelAdapter ABC (build_model, param_space, extract_features, to_spec, fixed_config) |
| test_registry.py | 10 | register_adapter, list_models, get_model_spec, discover |
| test_separability.py | 16 | davies_bouldin_index, silhouette_score, silhouette_score_sampled, all_metrics |

## 测试总计: 60 tests (20 旧 + 34 新 + 6 新)

## Phase 6+ 延续修复 (round 2, 2026-05-02)

### P0: 数据 shape 不一致 (splits.py + dataset.py)
- **问题**: `_process_and_window` 多通道产出 `[C, L]`，单通道产出 `[L, 1]`；`__getitem__` 每次 squeeze/transpose 修复
- **修复**: splits.py 统一产出 `[C, L]` (multichannel) 或 `[L]` (single-channel)；dataset.py `__getitem__` 移除全部 shape 修复逻辑

### P1: net_define_examples.py 错误注释
- **问题**: "param_space 返回的值会覆盖 fixed_config" — 实际行为正相反
- **修复**: 修正为 "fixed_config 会覆盖 param_space 搜索值"

### P2: 推理函数缺失
- **新建** `utils/inference.py`: `predict_from_checkpoint()` + `predict_single()`
- 导出到 `__init__.py`

### P3: checkpoint 保存元数据
- **修复**: kfold.py 保存 `{state_dict, config, val_acc, num_params}` 而非裸 state_dict
- detection.py + inference.py 兼容新旧两种 checkpoint 格式

### P4: pickle → JSON
- **修复**: `io_utils.py` `save_fold_results`/`load_fold_results` 改用 JSON，numpy → `.tolist()`

### P5: 统计显著性检验
- **新增**: `paired_ttest()` helper + `compare_models_separability_kfold()` 在 separability/analysis.py
- 对最佳模型做 K-Fold 配对 t 检验，输出 p 值

## 已知未修复 (低优先级)
- pin_memory 弃用警告 → PyTorch DataLoader 内部行为，非本项目代码
- 多处 bare except: pass → 在 cleanup/gc 路径中可接受
- NCMHead.predict 显式循环 → 性能优化非正确性问题
- 无 setup.py/pyproject.toml → 用户明确需要的是文件级导入方式
