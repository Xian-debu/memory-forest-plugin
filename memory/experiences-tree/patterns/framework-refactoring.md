---
id: EXP-PAT-0002
type: PATTERN
tree: experiences
layer: L3
status: ACTIVE
created: 2026-05-01
heartbeat: '2026-05-05'
priority: MEDIUM
owner: claude-code
originSessionId: 9d8cdeb6-51eb-46dc-96dc-a88b71a77f91
---
# 单体实验框架模块化重构模式

## 场景
Python 深度学习实验框架从单文件 2000+ 行重构为模块化包。

## 模式

### 1. 拆分顺序：从依赖最少的叶子节点开始
先拆纯函数工具（config, resources），再拆训练器，最后拆编排层（pipeline）。
**Why**: 编排层导入所有子模块，拆早了会因循环依赖失败。

### 2. Docker 容器内开发的宿主编辑模式
文件在宿主编辑，通过 `docker cp` 同步到容器测试。批量操作时写脚本避免遗漏。
**Why**: 容器内无编辑器，宿主同步后必须回测。

### 3. Auto-generated 文件陷阱
自动提取工具会把文件级导入误塞进函数 docstring 内，导致运行时 NameError。
**诊断方法**: grep 搜索 `from ..` 出现在 `"""` 和 `"""` 之间。
**Why**: 正则提取器不区分 docstring 和 import 语句。

### 4. ABC 适配器模式解耦外部模型
ModelAdapter 让外部模型文件（如 net_define_freqnet.py）无需修改就能接入框架。
**Why**: 用户只需实现 build_model → 框架接管 Optuna 搜索、K-Fold 训练、可视化。

**新模型接入标准流程 (3 步)**:
1. 复制 `net_define_<name>.py` 到框架根目录
2. 在 `experiment_framework/models/examples.py` 添加 `@register_adapter` 类:
   ```python
   @register_adapter
   class MyModelAdapter(ModelAdapter):
       @property
       def name(self) -> str: return "MyModel"
       def build_model(self, config): ...
       def param_space(self, trial, n_splits): ...
       def extract_features(self, model, dataset, device=None, batch_size=256): ...
       @property
       def description(self) -> str: return "one-line description"
   ```
3. `python run.py --model MyModel` 一键切换

**fixed_config 陷阱**: 架构参数要么放 fixed_config（固定值），要么放 param_space（Optuna 搜索），不能两边都放。`assemble_config` 合并顺序是 `{**study_best_params, **fixed_config}`，fixed_config 会覆盖搜索最优参数。

### 5. 训练代码去重策略
Optuna 搜索和正式训练共享同一个 train_one_fold_generic，通过可选参数（trial, scheduler_type）切换行为。
**Why**: 避免搜索和训练两套训练循环分叉导致 bug。

### 6. GPU 集成推理双路径
快路径：所有 K 个模型一次性 load 到 GPU。OOM 回退：逐批 swap。
**Why**: 小模型推理快 2-3x，大模型不崩。

### 7. 数据集模块化四件套
单体 Dataset (1300+ 行) → preprocessing / splits / caching / dataset 四模块拆分。
用 DataConfig dataclass 封装所有配置，三种划分策略各一独立函数。
**Why**: 新增数据源只需写 splits 函数，preprocessing 和 caching 直接复用。

### 8. 磁盘缓存策略
SHA256 哈希所有配置参数 → 16-char 键，缓存预处理后的 .npy + meta.json。
检查 `data_root_abs` 防目录移动。326x 加速第二次加载。
**Why**: 预处理（滤波/重采样/归一化）是瓶颈，缓存后窗口切分是纯 numpy 切片。

### 9. Notebook %run → import 迁移
逐步替换：保留 2 行 shim 文件（`from new_module import *`）向后兼容，notebook cell 逐个改为 import，最后删除 shim。
**Why**: 用户可能同时在多个 notebook 中使用旧 API，shim 给过渡窗口。

### 10. 重构后立即建单元测试
重构完成后立即在 `tests/` 下建 `conftest.py` + pytest 测试，覆盖核心抽象（ModelSpec）、配置合并、训练循环。
合成数据（随机 numpy）做最小集成测试，不依赖真实数据集。
**Why**: 重构最容易引入回归 bug，测试越早建越能及时捕获。

## 适用场景
- DL/ML 实验框架模块化
- Notebook → package 迁移
- 需要保持向后兼容的重构
- 数据集加载管道的模块化拆分
