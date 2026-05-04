---
id: PROJ-FWREF-0000
type: ROOT
tree: projects
layer: L2
status: RUNNING
subordinate_to: PHIL-ROOT-0000
created: 2026-05-01
heartbeat: '2026-05-04'
priority: HIGH
owner: claude-code
children:
- PROJ-FWREF-0001
- PROJ-FWREF-0002
- PROJ-FWREF-0003
- PROJ-FWREF-0004
- PROJ-FWREF-0005
- PROJ-FWREF-0006
- PROJ-FWREF-0007
originSessionId: 9d8cdeb6-51eb-46dc-96dc-a88b71a77f91
---
# 框架重构项目 — 根源节点

**本项目执行受 PHILOSOPHY.md（L5 绝对底层）约束。**

## 目标
将 `/root/project/framework` 的轴承故障诊断实验框架从单体 2111 行重构为模块化包。

## 核心需求
- 添加模型 = ModelAdapter 子类 + 一行代码接入全框架
- Jupyter Lab 友好，日志留痕
- 修复：separability CPU-only、domain shift 单体、目录混乱
- 保留：ModelSpec 抽象、训练管道、Optuna 搜索

## 环境
- Docker 容器 `dev` (NVIDIA Triton Server)
- Conda 环境: `my_torch` (PyTorch 2.9.1+cu130)
- Python 路径: `/root/miniconda3/envs/my_torch/bin/python`
- 工作目录: `/root/project/framework`
- **重要**: 文件在宿主编辑后必须 `docker cp` 到容器

## 当前状态 (2026-05-02)
- **Phase 1-4 完成**: 31 模块 + 20 测试 (见 2026-05-01 历史)
- **Phase 5 完成**: net_define_examples.py 创建（自包含 4 模型实现），examples.py 适配器导入修复，run.py 云端执行脚本，clean zip 打包
- **Phase 6 完成**: silouette bug修复 + deprecated API更新 + 34新测试 (60 total)
- **Phase 6+ 完成**: P0-P5 全面修复 (data shape 归一化, inference 模块, checkpoint 元数据, pickle→JSON, 统计检验), 60/60 测试通过
- **Phase 7 完成** (2026-05-03): 10 个 TF Keras 分类器 → PyTorch 迁移 + 验证, MCNN 3 bugs 修复, 13 模型全部注册可用
- **Phase 8 完成** (2026-05-03): Hawk XGBoost + FFT-differential 集成, 训练管道支持非神经网络树模型, trainer.py is_xgboost 分支
- **Phase 9 完成** (2026-05-03): ATFF-Net 创新模型 (可学习 Gabor + 跨频带注意力, ~56K) + Hawk-II 多域多尺度特征 (Hilbert包络 + 时域/频域统计, ~335d, GPU XGBoost), 16 模型全部可用
- **Phase 10 完成** (2026-05-03): GPU 兼容性热修复 (`.cpu()` before `.numpy()` in forward/xgb_fit, domain shift XGBoost bypass) + 统一输出命名方案 (7 文件改造, io_utils.py 新增, 所有产物归入 `out/` 目录树)
- **Phase 11 完成** (2026-05-03): 无人值守批量执行改造 — JSON 路径模型隔离 (`best_hyperparams.json` → `out/kfold_models_{model}/`), net_define 文件整理入 `networks/` 目录, `--skip-load` 模块级数据集缓存 (`sys.modules` 持久化), run.py try/except/finally 容错 + `_force_cleanup()` GPU/Worker 强制清理, 72/72 测试通过
- **Phase 11 审计修复** (2026-05-03): `diagnose_domain_shift()` 签名修复 (`save_dir='figures'` → `save_root='out', model_name='model'`), `_plot_shift_figure()` 添加 `mname` 参数消除 NameError (与 kfold.py:79 变量覆盖同类的"改 body 忘改签名"bug)
- **Phase 12 批量训练** (2026-05-03 17:21 启动): 16 模型无人值守批量执行 via run.ipynb, run.py 容错 + `_force_cleanup()`. Hawk 首个启动, Jupyter kernel PID 919341, 宿主 21GiB 可用

## 关键文件结构
```
experiment_framework/         # 31 模块包
├── utils/io_utils.py         # [Phase 10-11] 路径工具 + 数据集缓存 (sanitize/make_dir/cache_datasets)
├── visualization/            # kfold_plots, tsne_umap (统一 {model}_ 前缀命名)
├── training/kfold.py         # checkpoint → {model}_foldN_best.pth
├── domain_shift/detection.py # {model}_domain_shift.png
└── optim/                    # search.py, pipeline.py 统一 save_root='out'
networks/                     # [Phase 11] 13 个 net_define_*.py 模型定义
out/                          # [Phase 10-11] 统一输出目录树
├── figures_{model}/          # 所有可视化 (tsne/umap/training/eval/optuna/domain_shift)
└── kfold_models_{model}/     # checkpoint + best_hyperparams.json + fold_results.json (模型隔离)
run.py                        # [Phase 11] 容错脚本 — try/except/finally + _force_cleanup()
run.ipynb                     # [Phase 11] 16-cell 批量执行 notebook
tests/                        # 7 测试文件, 72 tests
```

## 关键教训 (2026-05-03)

- **文件分离 + 接口统一**: 每个模型 = 独立 net_define_xxx.py，export 4 函数
  (nn.Module类 + def build_xxx + def xxx_param_space + def xxx_feature_extractor)
- **模板 = 接口契约**: net_define_examples.py 是纯伪代码模板，定义 4 函数规范，
  不包含任何可运行实现；开发新模型时 copy + 参考 net_define_freqnet.py 填充
- **Adapter → 独立文件**: examples.py 中的 Adapter 从独立的 net_define_xxx.py import
  (不是从模板文件), 确保每个文件职责清晰
- **[Phase 11] 无人值守执行的三个关键**:
  1. **try/except/finally 包裹训练管道** — 单模型崩溃不阻断后续模型
  2. **显式 del + gc.collect() + cuda.empty_cache()** — 每个 cell 退出前强制清 GPU
  3. **模块级缓存复用大数据** — `sys.modules` 持久化 dataset，避免 `%run` 间反复加载
- **[Phase 11] 模型定义整理**: 13 个 net_define_*.py → `networks/` 子目录，
  所有 import 从 `import net_define_xxx` 改为 `from networks import net_define_xxx`
