---
id: SYS-LEAF-docusage
type: LEAF
tree: system
layer: L4
status: ACTIVE
parent: SYS-BRANCH-meta
created: 2026-04-30
heartbeat: '2026-05-05'
priority: HIGH
owner: claude-code
originSessionId: 439d65d5-aade-426e-807f-de0013c8a345
---
# 文档使用引导（Claude Code 专用）

## 首要规则：记忆森林优先

本文档系统是**记忆森林**的 `system-tree` 子树。一切操作遵循森林优先级：

```
forest-root (L4, ABSOLUTE)
    ↓
MF-SPEC + MF-RUNTIME (L4, 森林宪法)
    ↓
system-tree (L4, 本文档所属树)
    ↓
projects-tree (L2, 任务记忆)
    ↓
experiences-tree (L4, 核心经验)
```

## 会话启动序列（已更新）

```
1. forest-root.md            绝对第一入口 — 身份、森林状态
2. MF-RUNTIME.md             执行垃圾回收、心跳检查
3. system-tree/ROOT.md       系统配置树索引
4. 按任务类型加载系统分支     (见下表)
5. projects-tree/ROOT.md     当前项目上下文
```

## 规范文件索引（隶属 system-tree）

| 分支 | 规范文件 | 触发时机 |
|------|---------|----------|
| config | `role-definition.md` | 每次会话建立身份认知 |
| config | `dev-overview.md` | 每次会话理解环境上下文 |
| methodology | `tech-methodology.md` | 代码审查、设计审查、Bug 分析 |
| methodology | `debug-methodology.md` | Bug 定位与修复时 |
| methodology | `design-standards.md` | 实现前判断是否进入计划模式 |
| quality | `dev-standards.md` | 每次编写代码时 |
| quality | `doc-standards.md` | 产出任何文档/Markdown 时 |
| quality | `module-standards.md` | 创建/修改任何模块文件时 |
| quality | `tool-standards.md` | 每次选择工具调用方式时 |
| quality | `selfcheck-standards.md` | 完成代码修改后、多组件协作时 |
| quality | `baseline-verification.md` | 报告任务完成前 |
| safety | `system-ops-safety.md` | 系统级操作（apt/systemctl/内核）前 |
| meta | `project-init.md` | 创建新项目时 |
| meta | `doc-revision.md` | 修订任何规范时 |
| meta | `doc-relationship.md` | 理解规范间关系时 |
| meta | 本文档 | 定位规范时 |

## 规范冲突解决顺序

```
记忆森林宪法  >  安全红线  >  功能正确性  >  用户明确指令  >  设计规范  >  代码风格  >  文档格式
```

## 记忆更新策略

- 遵循 `MF-SPEC.md` 的节点生命周期管理
- 规范修订遵循 `doc-revision.md`
- 新规范创建需在 `system-tree/ROOT.md` 注册
- 所有更新后执行心跳冒泡

## 与用户沟通模式

- 简短更新：一句话告知当前步骤
- 结果优先：先说结论，再说细节
- 不追问已授权的事：用户说"允许 bash/git"，后续同类操作直接执行
- 主动声明风险：破坏性操作、不可逆操作执行前必须明确警告
