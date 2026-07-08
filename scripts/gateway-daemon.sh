#!/usr/bin/env bash
# Lifecycle-hook fallback (devcontainer postStartCommand): make sure the gateway
# is running even when VS Code's automatic tasks are blocked (the folderOpen
# security gate, or VS Code regressions like the 1.106.x trust-error bug).
#
# Idempotent: exits immediately if a gateway already answers on 18789.
# Never fails the container start (always exits 0).
# Logs to ~/.openclaw/gateway.log — the "OpenClaw: Gateway" task tails this
# file when it finds the gateway already running.
export PATH="/usr/local/share/npm-global/bin:/usr/local/share/nvm/current/bin:${HOME:-/home/node}/.local/bin:${HOME:-/home/node}/.npm-global/bin:/usr/local/bin:/usr/bin:/bin:${PATH:-}"
set -uo pipefail
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_env.sh" 2>/dev/null || true
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p "${HOME}/.openclaw"
LOG="${HOME}/.openclaw/gateway.log"

# Already running? Nothing to do.
if curl -fsS -m 2 -o /dev/null "http://127.0.0.1:18789/healthz" 2>/dev/null \
   || timeout 1 bash -c ':</dev/tcp/127.0.0.1/18789' 2>/dev/null; then
  exit 0
fi

# Start the gateway in the background via the existing start script (it owns
# the pre-flight, install-if-missing, and config logic). Detach fully so the
# container start isn't blocked and the process survives this shell.
: > "${LOG}"
{
  echo "[gateway-daemon] $(date '+%Y-%m-%d %H:%M:%S %Z') starting gateway in background…"
  echo "[gateway-daemon] watch live:  tail -f ~/.openclaw/gateway.log   (the"
  echo "[gateway-daemon] 'OpenClaw: Gateway' and 'OpenClaw: TUI' terminals also stream this)"
} >> "${LOG}"
OPENCLAW_GATEWAY_FOREGROUND=1 nohup bash "${REPO_DIR}/scripts/start-gateway.sh" >> "${LOG}" 2>&1 < /dev/null &
echo $! > "${HOME}/.openclaw/.gateway.pid"
disown 2>/dev/null || true

exit 0
