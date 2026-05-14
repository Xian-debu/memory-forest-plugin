# 记忆森林 — 入口索引

## 森林入口（最高优先级，先于一切）
- [前置检查清单](PREFLIGHT.md) — **L5 硬性步骤**，每次诊断/修改前必须逐条核对，跳过任一步=输出不可靠
- [广义指导思想](PHILOSOPHY.md) — **L5 绝对底层哲学根**，会话启动第一加载，一切规范之源头
- [记忆森林根源](forest-root.md) — 记忆管理框架入口，受哲学层约束
- [记忆森林规范](MF-SPEC.md) — 森林架构、节点类型、分层、心跳、垃圾回收
- [记忆森林运行时](MF-RUNTIME.md) — 会话生命周期、加载决策树、防溢出机制

## 记忆树索引

### system-tree — 系统配置
- [系统树根](system-tree/ROOT.md) — 所有开发规范、方法论、安全边界的集合
- [核心配置分支](system-tree/branch-config.md) — 角色定义 + 环境画像
- [方法论分支](system-tree/branch-methodology.md) — 技术方法论 + 调试 + 设计
- [质量标准分支](system-tree/branch-quality.md) — 开发/文档/模块/工具/自检/验证
- [安全分支](system-tree/branch-safety.md) — 系统操作安全边界
- [元规范分支](system-tree/branch-meta.md) — 文档引导/关系/修订/项目初始化

### experiences-tree — 核心经验
- [经验池根](experiences-tree/ROOT.md) — L3 跨项目模式 + L4 核心原则
- [多源聚合搜索](experiences-tree/patterns/multi-source-search.md) — 当通用搜索引擎不可用时的并行API聚合模式
- [带宽测试方法](experiences-tree/patterns/bandwidth-test.md) — WSL2 测速: speedtest-cli 不可用时的 curl 多源替代方案
- [训练进度诊断](experiences-tree/patterns/training-progress-diagnosis.md) — /proc/PID + nvidia-smi 非侵入式判断训练阶段, 不中断训练
- [中文AI API逆向](experiences-tree/patterns/api-reverse-pattern.md) — 豆包/元宝 API-First 逆向策略: Cookie注入→网络拦截→evaluate调API→格式暴力测试
- [论文审稿甄别](experiences-tree/patterns/thesis-review-甄别.md) — 三轮AI审稿教训: 审旧PDF→误判, 不读代码→捏造, 捏造引用→迎合
- [TikZ画图能力体系](experiences-tree/patterns/tikz-drawing-mastery.md) — 推理→TikZ代码三步翻译法 + RAG知识库入口 + 数据驱动画图流程
- [数据驱动TeX画图铁律](feedback/data-driven-tex-figures.md) — 画图前必须先理解代码和数据，禁止硬编码虚构数据；图/表/正文三位一体同源
- [论文写作方法论](feedback/thesis-writing-methodology.md) — 所有数据必须来自实测，禁止臆想；数据→管道→图/表→文本单向可追溯
- [论文数据管道](reference/thesis-data-pipeline.md) — Excel→full.csv→.dat→图/表的完整转换系统，含ESP32代码目录
- [盲眼验证LaTeX编译](experiences-tree/patterns/latex-blind-verification.md) — 无法看图时用 pdftotext + pdftoppm 间接验证编译结果
- [架构图重设计方法论](experiences-tree/patterns/architecture-diagram-redesign.md) — 诊断→原则→方案→实现四步流程 + 六条铁律
- [wkhtmltopdf page-height 精确匹配](feedback/wkhtmltopdf-page-height.md) — --page-height 必须二分搜索匹配内容, 过大导致caption被挤出页面
- [架构图设计铁律](feedback/architecture-diagram-principles.md) — 抽象层级/形状语义/颜色克制/少即多 + 常见反模式
- [OOM DataLoader诊断](experiences-tree/patterns/oom-dataloader-diagnosis.md) — 五步诊断法: dmesg→内存缺口→找放大器→查数据量→查累积效应
- [HTML→PDF→LaTeX图表工具链](experiences-tree/patterns/html-pdf-latex-figures.md) — TikZ困境的替代方案: wkhtmltopdf + flexbox + \includegraphics + page-height精确匹配
- [批量训练OOM修复](feedback/oom-dataloader-fork-bomb.md) — num_workers=2 + ipc_collect() + 跨cell缓存清理
- [VS Code 中文IME失效修复](feedback/vscode-ime-native-titlebar.md) — custom title bar → native, IME候选窗口定位恢复
- [natbib 参考文献缩进](feedback/natbib-bibliography-indent.md) — 6种内部方案失败, 仅 adjustwidth 外层约束生效
- [浏览器UI自动化替代API](experiences-tree/patterns/browser-ui-fallback.md) — REST API被风控时用Playwright CDP连接已登录浏览器, DOM交互绕过反爬 (2026-05-10)
- [v20 ABE Cookie解密死胡同](experiences-tree/patterns/v20-abe-cookie-dead-end.md) — Chromium 127+ App-Bound Encryption, 离线解密不可能, 唯一路径是CDP (2026-05-10)
- [ws替代WebSearch/WebFetch](feedback/use-ws-instead-of-websearch.md) — 不用内置搜索; ws --text --quick 快速搜索; ws --text 全源深度搜索; 禁止background (2026-05-14)
- [自动提议GitHub推送](feedback/auto-propose-github-push.md) — 代码修改+测试全绿+unpushed → 主动提议推送 (2026-05-14)
- [SPA聊天回复提取铁律](feedback/chat-response-extraction.md) — DOM行计数区分用户/助手消息, 禁止文本搜索, 发送前必须先记录行数 (2026-05-10)
- [运行时DOM探测](experiences-tree/patterns/runtime-ui-probing.md) — SPA功能发现不能靠静态分析, 必须触发交互后重新扫描DOM, AB配置≠UI实现 (2026-05-10)
- [豆包自动化框架 Phase 2-4](projects-tree/doubao-framework/ROOT.md) — 完整框架: 20模块, 90+6 tests, 23 CLI命令, 文件上传+KB桥接+智能问答 (2026-05-11)
- [LLM深度问答会话管理](experiences-tree/patterns/llm-qa-session-management.md) — 每轮前读DOM对话历史, 70%词重叠去重, 6轮自动新对话, echo质量判定 (2026-05-11)
- [GitHub推送完整工作流](reference/github-push-workflow.md) — 自提示→本地测试→连通检测→多方法推送(含API回退)→远程验证→同步, 完备容错 (2026-05-14)
- [开源项目敏感信息清除](experiences-tree/patterns/open-source-sanitization.md) — 硬编码→env vars, 选择器保留, cookie/ID零容忍, README排错提示词 (2026-05-11)
- [AI视觉评审分层信任](experiences-tree/patterns/ai-review-layered-trust.md) — 确定性>概率性>主观性, AI评审=ADVISORY ONLY, 人类最终裁决 (2026-05-13)
- [AI视觉评审仅供参考](feedback/ai-visual-review-advisory-only.md) — 豆包/任何AI视觉评审不可全信, 程序化检查权重高于AI (2026-05-13)
- [PPT制作知识体系](experiences-tree/patterns/ppt-creation-mastery.md) — 修改失败→创建成功; XML深克隆字体继承; Zone/Deco/Color/Space/Font方法论; 豆包评审权重规则; 自优化引擎 (2026-05-14)
- [PPT Creator v3](/root/.claude/scripts/ppt_create.py) — JSON驱动参数+三层Zone+装饰层+自检, 命令: pptc
- [PPT Optimizer](/root/.claude/scripts/ppt_optimizer.py) — N轮自优化引擎: 构建→PPTX上传→解析反馈→对比提示词→震荡检测→收敛 (2026-05-14)
- [CDP Manager](/root/.claude/scripts/cdp_manager.py) — Edge CDP健康检查+自动重启, WSL2→Windows桥接 (2026-05-14)
- [DoubaoCLI Launcher](reference/ppt-controller-tool.md) — 跨平台CDP浏览器自动启动, 已提交GitHub (2026-05-14)
- [AIGC降重范式](experiences-tree/patterns/aigc-decheck-paradigm.md) — 五轮迭代验证的七规则+收敛分析+理论地板, 74.15%→20.41% (2026-05-12)
- [Windows-WSL2 NPU 桥接](experiences-tree/patterns/windows-wsl2-npu-bridge.md) — WSL2无法直通宿主NPU时的HTTP API桥接模式: PowerShell探测→OpenVINO服务→WSL2网关IP调用 (2026-05-13)
- [NPU OpenVINO 部署全流程](experiences-tree/patterns/npu-openvino-deployment.md) — 模型选型→转换→静态形状陷阱→故障排查→RAG集成, L6→bge-m3实战 (2026-05-13)
- [NPU Embedding Pooling修复](feedback/npu-embedding-pooling-fix.md) — bge-m3简单mean pooling把padding噪声计入→无关文本sim~0.65; attention-mask-weighted pooling修复 (2026-05-14)
- [OpenVINO ConstOutput API陷阱](feedback/openvino-constoutput-api.md) — compiled_model返回ConstOutput非numpy; get_embed_fn忽略--device标志 (2026-05-14)
- [KB中文检索改进](experiences-tree/patterns/kb-chinese-search-improvement.md) — bigram分词+多词LIKE+候选池扩大, 关键词命中0%→67% (2026-05-14)
- [bge-m3指令无re-index无效](experiences-tree/patterns/bge-m3-instruction-without-reindex.md) — 实测6种指令变体, 不加文档侧重建时query前缀不改善分离度 (2026-05-14)
- [先诊断再修改](feedback/diagnose-before-modify.md) — NPU误诊教训: 看到cos=0.55以为是bug, 实际是bge-m3已知基线; 修改代码前必须先查记忆 (2026-05-14)
- [验收脚本防呆模式](feedback/validate-driven-guardrail.md) — 高风险项目建立validate脚本, 嵌入基线知识, LLM下次跑全PASS就不会乱修 (2026-05-14)
- [WSL2 GPU故障排除](experiences-tree/patterns/wsl2-gpu-troubleshooting.md) — dmesg dxg错误诊断; GPU显存振荡≠计算; nvidia-smi需从Windows侧调用 (2026-05-14)
- [Validate防呆矩阵](experiences-tree/patterns/validate-guardrail-matrix.md) — 基线嵌入代码模式: 高风险模块=validate脚本, 输出自带解释, LLM不再误诊 (2026-05-14)
- [SessionStart机械PREFLIGHT](experiences-tree/patterns/session-start-mechanical-preflight.md) — 前置注入方法论: 规则→机械注入, 不依赖LLM自觉 (2026-05-14)
- [PreToolUse模块护栏](experiences-tree/patterns/pretooluse-module-guardrail.md) — Edit/Write前自动验证: 模块validate PASS→警告+记录violation (2026-05-14)

### projects-tree — 项目记忆
- [项目树根](projects-tree/ROOT.md) — 所有项目任务记忆的集合
- [逆向工程技能体系](projects-tree/reverse-engineering/ROOT.md) — 2026-05-06 深度学习: P0-P2 技能分层 + 工具链 + LLM API 逆向范式
- [逆向工具链](projects-tree/reverse-engineering/toolchain.md) — 完整工具清单: 流量拦截/移动端/JS反混淆/二进制/浏览器反检测
- [豆包元宝逆向诊断](projects-tree/reverse-engineering/doubao-yuanbao-analysis.md) — 现有代码问题诊断 + 元宝401根因 + 三种修复方案
- [框架重构](projects-tree/framework-refactor/ROOT.md) — 实验框架模块化重构 (Phase 1-16 批量训练中, Encoder 7/16 完成)
- [毕设论文](projects-tree/thesis-writing/ROOT.md) — 本科毕业论文 (LaTeX, MCSA电机故障诊断, 已完成, 52页, 26引用, 三轮审稿修复)
- [架构图工具链](projects-tree/thesis-writing/leaf-arch-diagram-toolchain.md) — torchview DOT → pydot 折叠重复分支 → graphviz 渲染 PNG/SVG
- [LaTeX编译操作](projects-tree/thesis-writing/leaf-latex-ops.md) — latex-dev 容器编译, ctx 别名陷阱, pdftotext 验证
- [参考文献格式修正](projects-tree/thesis-writing/leaf-ref-format.md) — GB/T 7714-2015 文献类型标识, @inproceedings vs @article, .bbl 验证
- [RAG知识库导入](projects-tree/rag-kb-import.md) — RAG kb 三块材料导入 (152+44+0 文件, 144 文档, 4727 chunks)
- [ATFF-Net](projects-tree/framework-refactor/leaf-atff-net.md) — 可学习 Gabor 滤波器组 + 跨频带注意力 + 多尺度扩张卷积 (~56K)
- [Hawk-II](projects-tree/framework-refactor/leaf-hawk2.md) — 多域多尺度特征提取 + GPU XGBoost + CUDA 兼容性修复 (Hilbert 包络, ~335d)
- [首次自我进化](projects-tree/evolution-1-self-evolution.md) — Stop Hook + mf CLI + MCP Server + SessionStart + 权限优化 (2026-05-01 完成)
- [第二次自我进化](projects-tree/evolution-2-self-evolution.md) — 系统审计+WSL2调优+Git版本化+交叉工具整合+EXP-CORE-0008 (2026-05-12 完成)
- [第三次自我进化](projects-tree/evolution-3-self-evolution.md) — 防呆机械体系: validate矩阵+SessionStart PREFLIGHT+共振32/27规则+PreToolUse护栏 (2026-05-14 完成)
- [WebSearch替代工具](projects-tree/websearch-tool.md) — 多源聚合搜索 (GitHub+SO+HN+PyPI+Bing) 替代失效的WebSearch/WebFetch (2026-05-06 完成)
- [LLM Browser POC](projects-tree/llm-browser-poc.md) — Playwright浏览器自动化 + 人类级速率控制 + 多云LLM协同 (Kimi就绪, Phase 2: cookie导入)
- [Steel Browser 保留](projects-tree/steel-browser-subproject.md) — FROZEN: 3.67GB Docker镜像, fingerprint bug修复后启用
- [豆包自动化框架](projects-tree/doubao-framework/ROOT.md) — 7模块Playwright CDP框架, 浏览器UI+API双路径, 58单元+6集成测试 (2026-05-10 完成)
- [AIGC降重工作流](projects-tree/aigc-decheck-workflow.md) — 五轮迭代方法论, 论文AI率74%→20%, GitHub开源 (2026-05-12 完成)
- [AEGIS 整合系统](projects-tree/aegis-project.md) — 三层桥接架构整合 Guardian+Forest+KB, 11 tests, GitHub开源 (2026-05-13 完成)
- [Intel NPU 加速栈](projects-tree/PROJECTS-LEAF-0001.md) — Ultra 7 255HX, BAAI/bge-m3 (1024-dim) on NPU, RAG KB已集成, 5 t/s, 9/9 tests, 旧L6已清理 (2026-05-13 STABLE)

### projects-tree — 项目记忆 (续)
- [n8n工作流系统](projects-tree/PROJECTS-BRANCH-0001.md) — n8n Docker + Workflow Engine (4 workflows) + Webhook Server + Claude Code hooks集成 (2026-05-13 完成)

### 自动化基础设施
- [RAG kb CLI](/root/rag-kb/scripts/kb_cli.py) — `kb` 命令，本地知识库 (search/query/status/ingest/list/delete/index-memory/expand)
- [RAG Knowledge Expander](/root/rag-kb/rag/knowledge_expander.py) — 缺口检测→web扩展→自动摄取→增强回答
- [RAG 批量导入](/root/rag-kb/scripts/batch_ingest.py) — 批量文件夹导入知识库
- [RAG MCP Server](/root/rag-kb/mcp_server.py) — 7 个 MCP 工具 (kb_ingest/search/query/status/delete/list/index_memory)
- [WebSearch多源搜索](/.claude/scripts/websearch.py) — 并行聚合搜索 (GitHub+SO+HN+PyPI+Bing)，替代失效的内置搜索
- [WebSearch CLI](/.claude/scripts/aliases.sh) — `ws` 命令，快速搜索入口: `ws "q" --text --quick` (<10s), `ws "q" --text` (全源)
- [Browser Client](/.claude/scripts/browser_client.py) — Playwright 无头浏览器封装 (导航/填表/键入/截图/提取/Cookie)
- [LLM Orchestrator](/.claude/scripts/llm_orchestrator.py) — 人类级速率多 LLM 协同编排器 (HumanPacer + 多服务查询)
- [CLI 工具](/.claude/scripts/mf.py) — mf 命令行工具 (status/heartbeat/gc/search/health/create/list/show)
- [MCP Server](/.claude/scripts/mcp_memory_forest.py) — MCP 协议服务 (8 个工具, JSON-RPC 2.0 over stdio)
- [Stop Hook](/.claude/scripts/heartbeat_hook.py) — 会话退出自动心跳
- [SessionStart Hook](/.claude/scripts/startup_hook.py) — 会话启动自检
- [AI CLI](/.claude/scripts/ai_cli.py) — 交互式 AI 工具 (chat/review/summarize/translate, DeepSeek API)
- [AI Webhook Server](/.claude/scripts/ai_webhook_server.py) — AI HTTP API 服务 (5 个端点, 零依赖)
- [n8n Manager](/.claude/scripts/n8n_manager.py) — n8n 工作流管理器 (list/show/toggle/create)
- [AI 服务启动脚本](/.claude/scripts/start_ai_services.sh) — 一键启动 n8n + AI Webhook Server
- [PPT Controller](/root/.claude/scripts/ppt_controller.py) — WSL2→Windows PowerPoint 自动化 (python-pptx + COM), 存储路径 E:\PPT\
- [PPT Controller 参考](reference/ppt-controller-tool.md) — PPT 控制器架构、CLI 命令、Python API 参考
- [工作流别名](/.claude/scripts/aliases.sh) — mf/docker/claude/n8n/ai/ppt 快捷命令
- [Validate 防呆矩阵](/.claude/scripts/validate_all.py) — 一键全系统验收 (5 modules, 70+ checks): `python3 validate_all.py --quick`
- [Validate MF](/.claude/scripts/validate_mf.py) — Memory Forest 完整性 (结构+心跳+循环引用)
- [Validate Resonance](/.claude/scripts/validate_resonance.py) — Signal Resonance 规则有效性
- [Validate Hooks](/.claude/scripts/validate_hooks.py) — Claude Code hooks 配置完整性
- [Validate Services](/.claude/scripts/validate_services.py) — 后端服务健康 (Ollama+Docker+NPU+Guardian)
- [Guardian Guard](/.claude/scripts/system_drive.py) — PreToolUse 护栏: `_guardrail_check()` 编辑前自动验证

## 加载顺序（不可变）
```
PHILOSOPHY → forest-root → MF-SPEC → MF-RUNTIME → system-tree → (当前项目树)
```
然后加载自动化脚本: SessionStart hook → mf status → (工作) → Stop hook

**PHILOSOPHY.md 位于 L5 绝对底层，是一切规范、配置、经验的最终约束。任何下层与哲学层冲突时，哲学层胜出。**
