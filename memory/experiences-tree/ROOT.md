---
id: EXP-ROOT-0000
type: ROOT
tree: experiences
layer: L4
status: ACTIVE
subordinate_to: PHIL-ROOT-0000
created: 2026-04-30
heartbeat: '2026-05-05'
priority: HIGH
owner: claude-code
children:
- EXP-CORE-0001
- EXP-CORE-0002
- EXP-CORE-0003
- EXP-CORE-0004
- EXP-CORE-0005
- EXP-CORE-0006
- EXP-CORE-0007
- EXP-PAT-0001
- EXP-PAT-0002
- EXP-PAT-0003
- EXP-PAT-0004
- EXP-PAT-0005
- EXP-PAT-0007
- EXP-PAT-0008
- EXP-PAT-0009
- EXP-PAT-0010
- EXP-PAT-0011
- EXP-PAT-0014
- EXP-PAT-0015
- EXP-PAT-0016
- EXP-PAT-0017
- EXP-PAT-0019
- EXP-PAT-0020
- EXP-PAT-0021
- EXP-PAT-0022
originSessionId: 439d65d5-aade-426e-807f-de0013c8a345
---
# 经验池树 — 根源节点

**本树受 PHILOSOPHY.md（L5 绝对底层）约束。所有核心行为准则与经验提炼均以八条哲学原则为最终依据。**

## 目标
存储从所有项目中提炼的核心经验，分为 L3（跨项目模式）和 L4（核心原则）。

## 核心行为准则与哲学原则映射

| 行为准则 | 对应哲学原则 |
|---------|------------|
| EXP-CORE-0001 反驳-确认模式 | 3.3 质疑与纠正 — 以事实对抗错误认知 |
| EXP-CORE-0002 三次重复自省 | 6.1 刀刃向内 — 主动发现并修正 |
| EXP-CORE-0003 五次失败停止 | 7.3 设计容错 — 对资源消耗设置硬上限 |
| EXP-CORE-0004 经验迭代合并 | 6.4 知识策展 — 积累 + 修剪 |
| EXP-CORE-0005 自我迭代提示 | 3.6 反馈转化 + 3.5 确认后执行 — 成果服务于用户 |
| EXP-CORE-0006 搜索优先偷懒 | 5.2 建立根据地 — 从已有根据地出发 |
| EXP-CORE-0007 多步骤先建节点 | 5.1 持久战 — 分阶段推进，每步可恢复 |

### 行为准则与新增哲学原则的对应

| 新增哲学原则 | 关联行为准则 | 关联 L3 模式 |
|------------|------------|------------|
| 七、环境的战争 | EXP-CORE-0003 (五次失败停止) | PAT-0017/0020/0022 (swap/wsl2/batch) |
| 八、认知纪律 | — (尚无专用行为准则) | PAT-0011/0016/0019/0010/0021 (9 个模式) |
| 三、参谋路线 (扩展) | EXP-CORE-0001/0005 (反驳/迭代) | — |
| 六、整风 (扩展: 对称认知+知识策展) | EXP-CORE-0004 (经验合并) | 所有模式的反例部分 |

## 当前状态
- 已初始化
- 7 条核心行为准则已写入 (EXP-CORE-0001 ~ 0007)
- L3 patterns 目录: 16 条 (合并 0012→0009, 0013→0002, 0006→0008, 0018→0015; +0019 +0020)
- L4 core 目录: 7 条

## 经验索引
- [EXP-PAT-0001](patterns/plugin-publishing.md) — Claude Code Plugin/Skill 发布流水线 (已验证 2 次)
- [EXP-PAT-0002](patterns/framework-refactoring.md) — 实验框架模块化重构 + 新模型接入 3 步流程
- [EXP-PAT-0003](patterns/mcp-zero-dep.md) — MCP Server 零依赖实现 (JSON-RPC 2.0 over stdio)
- [EXP-PAT-0004](patterns/yaml-json-bridge.md) — YAML-JSON 桥接类型陷阱 (datetime.date 序列化)
- [EXP-PAT-0005](patterns/self-evolution-methodology.md) — 自我进化执行方法论 (互补先行→高价值→锦上添花)
- ~~EXP-PAT-0006~~ — 已并入 [EXP-PAT-0008](patterns/hybrid-architecture-fallback.md) (n8n webhook 环境变量是混合架构的触发条件)
- [EXP-PAT-0007](patterns/deepseek-thinking-block.md) — DeepSeek V4 Thinking Block 的 Token 消耗 (thinking 块与 text 块共享 max_tokens)
- [EXP-PAT-0008](patterns/hybrid-architecture-fallback.md) — 混合架构回退策略 (含 n8n webhook 环境变量 + API-only 限制)
- [EXP-PAT-0009](patterns/resumable-sessions.md) — 会话中断恢复模式 (任务状态 + .part 文件双重持久化保证恢复)
- [EXP-PAT-0010](patterns/data-normalize-at-source.md) — 数据源头归一化 (上游统一格式，下游删掉修复逻辑)
- [EXP-PAT-0011](patterns/verify-merge-order.md) — 配置合并顺序验证 (读代码不读注释，fixed_config 覆盖 search params)
- ~~EXP-PAT-0012~~ — 已并入 [EXP-PAT-0009](patterns/resumable-sessions.md) (低速下载策略是会话恢复的 L2 子集)
- ~~EXP-PAT-0013~~ — 已并入 [EXP-PAT-0002](patterns/framework-refactoring.md) (模型接入是框架重构第 4 节的详细展开)
- [EXP-PAT-0014](patterns/domain-adaptation-feature-engineering.md) — 跨领域特征工程迁移 (保留分解哲学，用目标领域物理重新设计特征集)
- [EXP-PAT-0015](patterns/xgboost-cuda-fork-conflict.md) — XGBoost GPU 显存管理 + PyTorch 兼容性完整方案 (含 .cpu()/.numpy() + 特征提取)
- [EXP-PAT-0016](patterns/docker-expose-vs-publish.md) — Docker EXPOSE vs -p 映射 + VS Code 自动隧道幻觉
- [EXP-PAT-0017](patterns/wsl2-swap-orphan.md) — WSL2 swap.vhdx 孤儿文件累积 (每次重启不清理旧 swap)
- [EXP-PAT-0019](patterns/stale-bytecode-cache.md) — 代码修复后错误不变: 先清 .pyc 缓存 + 重启 kernel
- [EXP-PAT-0020](patterns/batch-notebook-resilience.md) — Notebook 无人值守批量执行: try/except/finally 容错 + GPU 强制清理 + sys.modules 跨 cell 缓存
- [EXP-PAT-0021](patterns/signature-body-drift.md) — 命名重构后函数签名与函数体不一致: grep替换改body忘改签名
- [EXP-PAT-0022](patterns/wsl2-memory-cache-illusion.md) — WSL2 VM 不向 Windows 归还缓存，宿主机内存显示虚高 (文件缓存幻觉)
- ~~EXP-PAT-0018~~ — 已并入 [EXP-PAT-0015](patterns/xgboost-cuda-fork-conflict.md) (CPU 迁移后的推理+特征提取路径修复)
- [EXP-CORE-0001](core/behavior-rule-1.md) — 反驳-确认模式
- [EXP-CORE-0002](core/behavior-rule-2.md) — 三次重复即自省
- [EXP-CORE-0003](core/behavior-rule-3.md) — 五次失败即停止
- [EXP-CORE-0004](core/behavior-rule-4.md) — 经验迭代合并与垃圾识别
- [EXP-CORE-0005](core/behavior-rule-5.md) — 自我迭代与自我提示
- [EXP-CORE-0006](core/behavior-rule-6.md) — 搜索优先，不重复造车轮
- [EXP-CORE-0007](core/behavior-rule-7.md) — 多步骤任务必须先建立记忆森林子节点 (会话中断恢复)

## 经验升级规则
- L2 → L3: 项目完成时提炼
- L3 → L4: 3 个以上项目验证 或 用户确认为核心

## 容量上限
- L3 patterns: ≤ 50 条
- L4 core: ≤ 20 条
- 超限时按 (引用次数 × 最新心跳) 排序淘汰
