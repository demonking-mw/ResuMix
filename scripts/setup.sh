#!/usr/bin/env bash
#
# One-command local setup for ResuMix.
#
#   ./scripts/setup.sh                 # backend venv + frontend deps + local DB
#   ./scripts/setup.sh --with-model    # also pre-download the embedding model
#
# Everything it creates stays inside the repository: venv/, data/, node_modules/.
# No database server, cloud account or deployment step is involved.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

WITH_MODEL=0
for arg in "$@"; do
    case "$arg" in
        --with-model) WITH_MODEL=1 ;;
        -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
        *) echo "Unknown option: $arg" >&2; exit 1 ;;
    esac
done

step() { printf '\n==> %s\n' "$1"; }

# --------------------------------------------------------------- prerequisites
step "Checking prerequisites"
if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 is required (3.10 or newer)." >&2
    exit 1
fi
python3 - <<'PY'
import sys
if sys.version_info < (3, 10):
    sys.exit(f"Python 3.10+ required, found {sys.version.split()[0]}")
print(f"Python {sys.version.split()[0]}")
PY

if ! command -v npm >/dev/null 2>&1; then
    echo "npm is required for the frontend (install Node.js 18 or newer)." >&2
    exit 1
fi
echo "Node $(node --version), npm $(npm --version)"

# ------------------------------------------------------------------ python env
step "Creating the Python virtualenv (venv/)"
if [[ ! -d venv ]]; then
    python3 -m venv venv
else
    echo "venv/ already exists, reusing it"
fi
# shellcheck disable=SC1091
source venv/bin/activate

step "Installing Python dependencies (this downloads PyTorch, a few hundred MB)"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# ------------------------------------------------------------------------- env
step "Preparing .env"
if [[ ! -f .env ]]; then
    cp .env.example .env
    SECRET="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
    python - "$SECRET" <<'PY'
import pathlib
import sys

secret = sys.argv[1]
path = pathlib.Path(".env")
text = path.read_text(encoding="utf-8")
path.write_text(
    text.replace("JWT_REAUTH_SECRET=", f"JWT_REAUTH_SECRET={secret}", 1),
    encoding="utf-8",
)
PY
    echo "Created .env with a freshly generated JWT_REAUTH_SECRET"
else
    echo ".env already exists, leaving it untouched"
fi

if [[ ! -f frontend/.env ]]; then
    cp frontend/.env.example frontend/.env
    echo "Created frontend/.env"
else
    echo "frontend/.env already exists, leaving it untouched"
fi

# -------------------------------------------------------------------- database
step "Initialising the local database"
python scripts/init_db.py

# ----------------------------------------------------------------------- model
if [[ "$WITH_MODEL" -eq 1 ]]; then
    step "Downloading the embedding model into models/"
    python scripts/fetch_model.py
else
    step "Skipping model download"
    echo "The embedding model is fetched automatically on first use."
    echo "To pre-download it now: python scripts/fetch_model.py"
fi

# -------------------------------------------------------------------- frontend
step "Installing frontend dependencies"
cd frontend
npm install
cd "$REPO_ROOT"

# ----------------------------------------------------------------------- done
step "Setup complete"
cat <<'EOF'
Next steps:
  1. Add a language-model setting to .env (OPENAI_KEY, or OPENAI_BASE_URL for a
     local Ollama / LM Studio server). Resume generation needs one of these.
  2. Start everything:  ./scripts/start.sh
  3. Open http://localhost:3000
EOF
