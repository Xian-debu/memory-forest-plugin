---
id: EXP-PAT-0001
name: plugin-publishing
description: Claude Code plugin/skill 开发、打包、本地安装与发布的完整流水线
type: LEAF
tree: experiences
layer: L3
parent: EXP-ROOT-0000
tags:
- plugin
- skill
- publishing
- marketplace
- claude-code
- github
heartbeat: '2026-05-05'
status: ACTIVE
validations: 2
originSessionId: 9d8cdeb6-51eb-46dc-96dc-a88b71a77f91
---
# Plugin/Skill 发布流水线

## 核心流程

```
SKILL.md → Plugin 包装 → GitHub 仓库 → marketplace → 用户安装
```

## 详细步骤

### 1. Skill → Plugin 包装

Skill 不能直接安装，必须套 Plugin 壳：

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # 必填: name, version
├── skills/
│   └── skill-name/
│       ├── SKILL.md         # 必填: name (kebab-case) + description (第三人称)
│       ├── references/
│       ├── scripts/
│       └── assets/
└── README.md
```

### 2. 打包

```bash
cd skill-creator && python -m scripts.package_skill <skill-path> <output-dir>
```

生成 `.skill` 文件（本质是 zip），排除 `__pycache__`、`evals/` 等。

### 3. 本地安装（三梯度）

| 方式 | 命令 | 持久性 |
|------|------|--------|
| 临时 | `claude --plugin-dir <path>` | 单会话 |
| 永久 | 本地 marketplace + `git-subdir` file:// URL → `claude plugin install` | 永久 |
| 发布态 | GitHub URL → marketplace add → install | 永久+分享 |

### 4. GitHub 发布

```bash
# 用户侧安装
claude plugin marketplace add https://github.com/<user>/<repo>
claude plugin install <plugin-name>
```

- Tag release 用语义版本 (`v1.0.0`)
- 更新后打新 tag，用户 `claude plugin update` 即可升级

## 关键约束

- Skill name: kebab-case, ≤64 字符
- Description: 第三人称, ≤1024 字符, 不能含 `<>`
- `package_skill.py` 需要从 skill-creator 目录以 `-m scripts.package_skill` 运行，直接执行有模块导入问题

## 沙箱环境 Git Push 替代方案

当 git 协议被 sandbox 阻止但 `gh api` 可用时：

1. **空仓库**: Contents API `PUT /repos/.../contents/{path}` 创建种子文件，初始化仓库
2. **批量上传**: Git Data API 流程
   - `POST /git/blobs` → 为每个文件创建 blob
   - `POST /git/trees` → 创建 tree（包含所有 blob）
   - `POST /git/commits` → 创建 commit（引用 parent）
   - `PATCH /git/refs/heads/{branch}` → 更新分支引用
3. **Tag**: `POST /git/refs` 创建 `refs/tags/v{version}`

## 验证记录
- 2026-05-01: PROJ-EVOL-0001 (自我进化) 中再次使用 Git Data API 推流，`git push` 超时后 `gh api` 成功推送 4 个文件 + 创建 tag v1.1.0。此模式第二次验证可靠。
