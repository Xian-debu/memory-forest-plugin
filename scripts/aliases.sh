# ── Memory Forest CLI aliases ──────────────────────────────────
alias mf='python3 /root/.claude/scripts/mf.py'
alias mfs='mf status'
alias mfh='mf health'
alias mfgc='mf gc'

# ── Docker shortcuts (container: dev) ──────────────────────────
alias dexec='docker exec dev'
alias dcp='docker cp'
alias dcpin='docker cp'      # dcpin <local> dev:<container>
alias dcpout='docker cp'     # dcpout dev:<container> <local>
alias dps='docker ps'
alias dimg='docker images'
alias dlogs='docker logs'

# ── Claude Code shortcuts ──────────────────────────────────────
alias cc='claude'
alias ccc='claude -c'
alias ccp='claude -p'

# ── AI CLI shortcuts ───────────────────────────────────────────
alias ai='python3 /root/.claude/scripts/ai_cli.py'
alias aichat='ai chat'
alias aireview='ai review'
alias aisum='ai summarize'
alias aitrans='ai translate'
alias aiserve='python3 /root/.claude/scripts/ai_webhook_server.py'

# ── Local AI (Ollama models) ─────────────────────────────────────
alias local-ai='python3 /root/.claude/scripts/local_ai.py'
alias lai='python3 /root/.claude/scripts/local_ai.py'
alias lais='lai search'
alias lair='lai review'

# ── n8n management ─────────────────────────────────────────────
alias n8nw='python3 /root/.claude/scripts/n8n_manager.py'
alias n8nls='n8nw list'
alias n8nstat='n8nw status'

# ── Common paths ───────────────────────────────────────────────
export MF_ROOT="$HOME/.claude/projects/-root/memory"
export CLAUDE_SCRIPTS="$HOME/.claude/scripts"
