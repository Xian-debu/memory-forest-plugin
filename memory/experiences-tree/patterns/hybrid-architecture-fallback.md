---
id: EXP-PAT-0008
type: EXPERIENCE
tree: experiences
layer: L3
status: ACTIVE
created: 2026-05-01
heartbeat: '2026-05-05'
priority: HIGH
owner: claude-code
tags:
- architecture
- fallback
- hybrid
- resilience
- api
- automation
source: PROJECTS-BRANCH-0001
originSessionId: a7664e14-d841-48de-acfa-f9d0da11efe2
---
# 混合架构回退策略

## 触发条件
主工具（n8n）的 webhook 功能在 API-only 管理模式下不可用，但项目仍需 webhook 端点和定时自动化。

## 根因

### 环境变量缺失
Docker 部署 n8n 时必须同时设置 `N8N_HOST` 和 `WEBHOOK_URL`，否则 webhook 路径不会被注册到内部路由表。日志仅显示 "Activated workflow" 但不激活 webhook listener:
```
N8N_HOST=localhost
WEBHOOK_URL=http://localhost:5678
```

### API-only 管理的硬限制
即使设置了环境变量，n8n v1.118.2 中通过纯 API（无 UI 交互）管理 webhook 工作流仍可能注册失败。**Webhook 注册与 UI 层面的 "Execute workflow" 按钮耦合**。Cron 触发器和手动触发器始终正常，不受此限制影响。

## 核心问题
如果坚持用单一工具解决所有需求，会导致：
- 大量时间浪费在调试不可控的框架行为上
- 交互式功能（chat/review）和自动化功能（scheduled tasks）都无法交付
- 项目的核心价值无法实现

## 行动
1. **识别工具的能力边界**: n8n API-only 管理中，Cron 触发器 ✓，Webhook ✗
2. **按能力分拆需求**:
   - n8n Cron → 定时自动化（Daily Digest, Weekly Report, Dev Tips）
   - Python stdlib webhook server → HTTP API 端点
   - Python CLI → 交互式 AI 工具
3. **统一接口层**: Shell alias (`ai`, `n8nls`, `aiserve`) 隐藏底层多样性
4. **每层独立验证**: CLI 用命令行测试，webhook server 用 curl，n8n 用 REST API
5. **不强行统一**: 三层保持独立，各自用最合适的工具，通过 alias 和文件路径约定集成

## 结果
三个独立组件在各自的边界内稳定工作：
- 4 个 n8n 定时工作流活跃运行
- AI Webhook Server 提供 5 个 REST 端点
- AI CLI 提供 4 个交互命令
- 通过 9 个 shell alias 统一访问

## 反例
- 坚持修复 n8n webhook → 无限调试框架源码，零交付
- 用 n8n HTTP Request 节点模拟 AI 调用（因为无法安装自定义节点）→ 配置复杂，调试困难
- 写一个庞大的统一框架 → 耦合度高，一个组件失败影响全局
- 放弃 webhook 需求 → 失去 HTTP API 的便利性

## 关键要点
- **边界优先**: 先确定工具的可靠边界，再在边界内做设计
- **独立可替换**: 每个组件独立工作，出问题时不影响其他组件
- **组合优于统一**: 多个简单工具的组合比一个复杂框架更健壮
- **别和框架打架**: 如果框架的某个功能在限制条件下不可用，用替代方案而非硬刚
- **最少依赖**: Python stdlib webhook server 零外部依赖，永远可用

## 适用场景
- 任何在受限环境（Docker、无 pip、无 UI）中搭建自动化系统的场景
- 主框架部分功能不可用时，快速构建互补组件
- API-only 管理模式下评估工具的实际可用性

## 来源
从 PROJECTS-BRANCH-0001 (n8n工作流系统搭建) 中架构决策提炼
