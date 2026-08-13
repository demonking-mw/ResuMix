#!/usr/bin/env bash
#
# Run ResuMix locally: Flask API + Vite dev server.
#
#   ./scripts/start.sh             # both
#   ./scripts/start.sh backend     # API only
#   ./scripts/start.sh frontend    # UI only
#
# Ctrl-C stops everything.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

TARGET="${1:-all}"

if [[ ! -d venv ]]; then
    echo "venv/ not found. Run ./scripts/setup.sh first." >&2
    exit 1
fi

pids=()

cleanup() {
    trap - INT TERM EXIT
    for pid in "${pids[@]:-}"; do
        kill "$pid" 2>/dev/null || true
    done
    wait 2>/dev/null || true
}
trap cleanup INT TERM EXIT

start_backend() {
    echo "Starting backend on http://127.0.0.1:${BACKEND_PORT:-5001}"
    # shellcheck disable=SC1091
    source venv/bin/activate
    python -m backend.api.api_1 &
    pids+=("$!")
}

start_frontend() {
    if [[ ! -d frontend/node_modules ]]; then
        echo "frontend/node_modules not found. Run ./scripts/setup.sh first." >&2
        exit 1
    fi
    echo "Starting frontend on http://localhost:3000"
    (cd frontend && npm run dev) &
    pids+=("$!")
}

case "$TARGET" in
    all)      start_backend; start_frontend ;;
    backend)  start_backend ;;
    frontend) start_frontend ;;
    *) echo "Usage: $0 [all|backend|frontend]" >&2; exit 1 ;;
esac

wait
