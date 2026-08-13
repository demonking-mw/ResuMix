# Local setup

Step-by-step instructions for running ResuMix on your own machine, plus what to
do when something goes wrong. For the short version see the
[README](../README.md).

---

## 1. Prerequisites

- **Python 3.10 or newer** — `python3 --version`
- **Node.js 18 or newer** — `node --version`
- **~3 GB free disk** — PyTorch (~1 GB) plus the embedding model (~420 MB)

Not required: PostgreSQL, Docker, LaTeX, a cloud account.

### Linux / macOS

```bash
python3 --version && node --version
```

If Python is missing, install it with your package manager (`apt install
python3 python3-venv`, `brew install python`). Node comes from
[nodejs.org](https://nodejs.org) or your package manager.

### Windows

Use WSL2 or Git Bash for the shell scripts. Without a Bash shell, follow the
manual steps in section 3.

---

## 2. Automated setup

```bash
git clone <repo-url> ResuMix
cd ResuMix
./scripts/setup.sh
```

The script:

1. checks Python and Node versions,
2. creates `venv/` and installs `requirements.txt`,
3. copies `.env.example` to `.env` and generates a random `JWT_REAUTH_SECRET`,
4. copies `frontend/.env.example` to `frontend/.env`,
5. creates `data/resumix.db` with the schema,
6. installs `frontend/node_modules`.

It never overwrites an existing `.env`, and it downloads the embedding model
only when you pass `--with-model`.

---

## 3. Manual setup

If you would rather not run the script:

```bash
# backend
python3 -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(48))"   # paste into JWT_REAUTH_SECRET
python scripts/init_db.py

# frontend
cp frontend/.env.example frontend/.env
cd frontend && npm install && cd ..
```

---

## 4. Choose a language model

Job descriptions are turned into requirement sentences by an OpenAI-compatible
chat API. Resume generation does not work until one of these is configured.

### Option A — OpenAI

```bash
# .env
OPENAI_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

### Option B — a model on your own machine

Any server that speaks the OpenAI chat-completions API works.

**Ollama**

```bash
ollama serve
ollama pull llama3.1
```

```bash
# .env
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_MODEL=llama3.1
# OPENAI_KEY can stay empty
```

**LM Studio** — start the local server, then set
`OPENAI_BASE_URL=http://localhost:1234/v1` and `OPENAI_MODEL` to the loaded
model.

The model is asked to return a plain Python list of requirement sentences and
gets three attempts to produce parseable output. Very small models sometimes
fail all three; if resume generation reports a parse failure, try a larger one.

---

## 5. The embedding model

Line scoring uses `sentence-transformers/all-mpnet-base-v2` and runs entirely on
your machine (CPU is fine).

Resolution order:

1. `OPT_MODEL_PATH` if it points at an existing directory — used offline.
2. `OPT_MODEL_PATH` as a Hugging Face model id if the path does not exist.
3. `models/all-mpnet-base-v2` if it exists.
4. `sentence-transformers/all-mpnet-base-v2`, downloaded once into the Hugging
   Face cache (`~/.cache/huggingface`).

Pre-download so the first resume generation is not slow:

```bash
python scripts/fetch_model.py
# smaller and faster, slightly lower quality:
python scripts/fetch_model.py --model sentence-transformers/all-MiniLM-L6-v2
```

---

## 6. Running

```bash
./scripts/start.sh              # backend + frontend
./scripts/start.sh backend      # backend only
./scripts/start.sh frontend     # frontend only
```

Or manually:

```bash
source venv/bin/activate
python -m backend.api.api_1     # http://127.0.0.1:5001

cd frontend && npm run dev      # http://localhost:3000
```

Check the API is alive:

```bash
curl http://127.0.0.1:5001/health
# {"ok":true}
```

---

## 7. Your data

Everything is under the repository directory:

| Path | Contents |
| --- | --- |
| `data/resumix.db` | accounts, master resumes, cached line embeddings |
| `models/` | downloaded sentence-transformer, if you pre-fetched it |
| `.env`, `frontend/.env` | local settings and keys |

All are gitignored.

```bash
cp data/resumix.db ~/backups/resumix-$(date +%F).db   # back up
rm data/resumix.db && python scripts/init_db.py       # start over
python scripts/inspect_db.py                          # list accounts
```

Passwords are stored as PBKDF2-HMAC-SHA256 hashes. An account created before
hashing existed keeps its plaintext value until its owner next logs in, at which
point it is re-hashed automatically.

---

## 8. Optional: PostgreSQL instead of SQLite

Only needed if you deliberately want a server-backed database.

```bash
pip install "psycopg[binary]" psycopg-pool
```

```bash
# .env
DATABASE_URL=postgresql://user:password@host:5432/dbname
DATABASE_SSLMODE=require        # use "disable" for a local server
```

Create the table yourself:

```sql
CREATE TABLE data (
    uid VARCHAR(256) PRIMARY KEY,
    user_name VARCHAR(64),
    pwd VARCHAR(255),
    email VARCHAR(256) NOT NULL UNIQUE,
    auth_type VARCHAR(16),
    userinfo JSONB,
    resumeInfo JSONB
);
```

`pwd` holds a PBKDF2 hash of about 110 characters, so it needs more room than
the original `VARCHAR(64)`.

Clearing `DATABASE_URL` switches straight back to the local SQLite file.

---

## 9. Troubleshooting

**`JWT_REAUTH_SECRET must be a string`**
`.env` is missing or the value is empty. `cp .env.example .env` and set it, or
re-run `./scripts/setup.sh`.

**`OpenAI API key not found in .env file`**
Set `OPENAI_KEY`, or set `OPENAI_BASE_URL` to a local server.

**`openai.APIConnectionError`**
`OPENAI_BASE_URL` points at a server that is not running. Start it, or clear the
variable and use `OPENAI_KEY`.

**First generation takes a while**
The embedding model is downloading and loading. Pre-fetch it (section 5). After
the first request the model stays in memory and line embeddings are cached in
your resume, so later runs spend most of their time waiting on the language
model rather than on scoring.

**Non-Latin characters look wrong in the PDF**
ResuMix registers a Unicode system font automatically and falls back to built-in
CID fonts for Chinese, Japanese and Korean. To control the typeface yourself,
set `RESUMIX_PDF_FONT` to a `.ttf` file (or a directory containing Regular/Bold/
Italic faces).

**`Address already in use` on 5001**
Change `BACKEND_PORT` in `.env` and `VITE_API_BASE_URL` in `frontend/.env`.

**Browser console shows a CORS error**
Add the origin to `CORS_ORIGINS` in `.env` (comma separated) and restart the
backend.

**The UI loads but every API call fails**
The backend is not running, or `VITE_API_BASE_URL` does not match
`BACKEND_HOST`/`BACKEND_PORT`. Vite only reads `.env` at startup — restart
`npm run dev` after editing it.

**No "Sign in with Google" button**
Expected: it is hidden unless `VITE_GOOGLE_CLIENT_ID` is set. Use email and
password.

**`pip install` fails building a package**
Your Python may be newer than the wheels available for PyTorch. Create the venv
with a slightly older interpreter, e.g. `python3.12 -m venv venv`.

**The app seems to be using a remote database**
`DATABASE_URL` in `.env` is a `postgresql://` URL. Clear it.
