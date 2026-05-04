---
id: PROJ-FWREF-0001
type: LEAF
tree: projects
layer: L2
status: ACTIVE
created: 2026-05-01
heartbeat: '2026-05-05'
priority: HIGH
owner: claude-code
parent: PROJ-FWREF-0000
originSessionId: 9d8cdeb6-51eb-46dc-96dc-a88b71a77f91
---
# Phase 1-3 完成详情

## 已完成模块

### 核心拆分 (12 文件)
- `core/model_spec.py` — ModelSpec 类（不变）
- `core/config.py` — assemble_config, _default_param_space, _format_trial_params
- `core/resources.py` — _cleanup_dataloaders, _cleanup_gpu, _infer_*
- `training/trainer.py` — train_one_fold_generic（新增 trial/scheduler_type 参数）
- `training/kfold.py` — train_kfold_generic
- `training/ensemble.py` — _soft_voting_ensemble_generic（GPU 双路径优化）
- `optim/search.py` — run_optuna（使用 make_optuna_objective，消除重复训练代码）
- `optim/pipeline.py` — bayes_to_training, run_pipeline
- `optim/objective.py` — make_optuna_objective（复用 train_one_fold_generic）
- `visualization/kfold_plots.py` — visualize_kfold_results_generic
- `visualization/tsne_umap.py` — 特征提取 + t-SNE/UMAP（已移除 pip install）
- `utils/io_utils.py` — save/load_fold_results

### 新增能力
- `models/adapter.py` — ModelAdapter ABC: name, build_model, param_space, extract_features, to_spec
- `models/registry.py` — @register_adapter, list_models(), get_model_spec(), discover()
- `models/examples.py` — 4 built-in adapters (PureCNN1D, FreqNet, ResNet1D, DualStreamAttn)
- `logging/logger.py` — ExperimentLogger（Jupyter 自动检测，HTML 表格，进度条）
- `separability/metrics.py` — GPU 加速 DBI + Silhouette（PyTorch）
- `separability/analysis.py` — 管道集成：analyze_kfold_separability, compare_models_separability
- `domain_shift/detection.py` — PCA 投影 + δ 向量 + 自动诊断报告
- `domain_shift/correction.py` — ClassShiftState, SoftAlign, ProtoAlign, NCMHead, evaluate_calibration

## 关键修复
1. **GPU 集成效率**: 所有模型一次性移 GPU（快速路径），OOM 时自动回退逐批换入换出
2. **训练代码去重**: ~140 行重复训练循环 → make_optuna_objective 复用 train_one_fold_generic
3. **pip install 移除**: tsne_umap.py 中的 `subprocess.check_call(["pip", "install"])` 改为 ImportError
4. **导入修复**: 所有 auto-generated 文件的导入从 docstring 内移到文件头部

## 验证状态
- 全部 26 模块导入通过
- 23 公开 API 符号可访问
- GPU metrics (DBI/Silhouette) 功能正常
- ModelAdapter + registry + 4 adapters 工作正常

## 后续入口
- 容器: `docker exec -w /root/project/framework -it dev bash`
- Conda: `conda activate my_torch`
- Notebook: `/root/project/framework/freqnet_condition.ipynb`
- Legacy: `/root/project/framework/legacy/experiment_framework.py`
