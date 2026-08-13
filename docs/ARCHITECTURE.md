# Architecture

How ResuMix is put together now that it runs locally.

---

## Processes

```
┌────────────────────────┐        ┌──────────────────────────────┐
│ Vite dev server :3000  │  HTTP  │ Flask API 127.0.0.1:5001     │
│ React UI               ├───────►│ backend/api/api_1.py         │
└────────────────────────┘        └──────────────┬───────────────┘
                                                 │
                    ┌────────────────────────────┼────────────────────────────┐
                    ▼                            ▼                            ▼
          ┌──────────────────┐       ┌─────────────────────┐      ┌────────────────────┐
          │ data/resumix.db  │       │ sentence-transformer│      │ OPENAI_BASE_URL    │
          │ SQLite, on disk  │       │ local CPU inference │      │ OpenAI or your own │
          └──────────────────┘       └─────────────────────┘      └────────────────────┘
```

Only the last box can be remote, and only if you point it at OpenAI. Everything
else is a file or a process on your machine.

---

## Database layer

`backend/src/db_helper/` picks a backend from `DATABASE_URL`:

| File | Role |
| --- | --- |
| `dbconn.py` | `DBConn` — the only class the app uses; chooses a backend |
| `sqlite_conn.py` | local default; file-backed, schema created on first connect |
| `postgres_conn.py` | the original hosted path; `psycopg` imported lazily |
| `schema.sql` | SQLite schema |
| `errors.py` | shared `UniqueViolation` type |

```
DATABASE_URL unset / empty   -> SQLite at RESUMIX_DB_PATH or data/resumix.db
DATABASE_URL sqlite:///x.db  -> SQLite at that path
DATABASE_URL postgresql://…  -> PostgreSQL
```

The interface is unchanged: `run_sql(query, params) -> list[dict]` and
`close()`. The SQLite backend keeps callers from noticing the swap by

- rewriting `%s` placeholders to `?`,
- JSON-encoding `dict`/`list` parameters on write,
- JSON-decoding `userinfo` and `resumeinfo` on read, so callers still get plain
  dicts as psycopg returns for `JSONB`,
- raising the same `UniqueViolation` on duplicate signups.

Because of this, no SQL in `class_helper/` had to change.

---

## Request flow: generating a tailored resume

1. `POST /resume/optimize/full` with a job description and a reauth token.
2. `ResumeHandle` verifies the JWT (`JWT_REAUTH_SECRET`) and loads the master
   resume from the `data` table.
3. `Resume.make()` asks the chat model (`AIBot`, `general_helper/isa_bot.py`)
   for 1–12 requirement sentences. A job description shorter than 40 characters
   is rejected before any model call.
4. `line_eval()` embeds the requirements and every resume line with the
   sentence-transformer, mapping cosine similarity onto a fixed 0–10 scale.
   Embeddings are cached in `aux_info.vec`, reused on later runs, and written
   back to the database along with the scores.
5. `Resume.optimize()` applies per-item weights and biases, then chooses which
   items and lines fit. Sections with nothing selected are dropped.
6. `LTemplate.resume_builder()` renders the PDF with reportlab (no LaTeX
   toolchain involved, despite the module names), best-scoring bullet first.
7. The response carries the tailored dict, the base64 PDF, and hashes proving
   both came from the same optimization run.

---

## Configuration

Backend config is read from the environment (`.env` via `python-dotenv`):

| Concern | Variables |
| --- | --- |
| Storage | `DATABASE_URL`, `RESUMIX_DB_PATH`, `DATABASE_SSLMODE` |
| Auth | `JWT_REAUTH_SECRET` |
| Chat model | `OPENAI_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL` |
| Scoring model | `OPT_MODEL_PATH` |
| PDF font | `RESUMIX_PDF_FONT` |
| Server | `BACKEND_HOST`, `BACKEND_PORT`, `FLASK_ENV`, `CORS_ORIGINS` |

Frontend config is centralised in `frontend/src/config.js`, fed by
`VITE_API_BASE_URL` and `VITE_GOOGLE_CLIENT_ID`. No component holds a hardcoded
host or client id.

Defaults are local: the API binds to loopback, CORS allows only
`localhost:3000` and `localhost:5173`, and Google sign-in is off unless a client
id is supplied.

---

## Data model

One table, `data`, one row per user:

| Column | Contents |
| --- | --- |
| `uid` | user id (primary key; the Google `sub` for OAuth accounts) |
| `user_name`, `email` | profile fields, `email` unique and lower-cased |
| `pwd` | PBKDF2-HMAC-SHA256 hash for `eup` accounts |
| `auth_type` | `eup` (email/username/password) or `go` (Google) |
| `userinfo` | JSON: flags such as `email_verified` |
| `resumeinfo` | JSON: the whole master resume, including cached embeddings and scores |

The resume JSON nests as `sections -> items -> lines`, each line carrying
`content` (rendered), `content_str` (plain text used for scoring), `score`, and
`aux_info.vec` (cached embedding).

---

## What changed from the hosted version

| Was | Now |
| --- | --- |
| Neon PostgreSQL over TLS, required | SQLite file, created on first run; PostgreSQL optional |
| `DATABASE_URL` mandatory | unset means "use the local file" |
| CORS allow-list of Vercel domains | localhost origins, extendable via `CORS_ORIGINS` |
| Flask bound to `0.0.0.0` | bound to `127.0.0.1` |
| `vercel.json` rewrite configs | removed |
| Embedding model had to be vendored (`local_files_only=True`) | resolved from a local directory, or downloaded once |
| `OPENAI_BASE_URL` ignored, OpenAI only | honoured, so a local server works |
| Google client id hardcoded in two components | `VITE_GOOGLE_CLIENT_ID`, button hidden when unset |
| Exact dependency pins from the deploy image | lower bounds; dev tools split into `requirements-dev.txt` |
| No local run instructions | `scripts/setup.sh`, `scripts/start.sh`, this docs directory |

A later pass fixed the application defects found while testing that setup:
passwords are hashed, every query is parameterised, credentials moved out of URLs,
empty sections no longer break generation, scores are on an absolute scale and
bullets print best-first, non-Latin text renders, and failed database writes are
reported instead of swallowed. [KNOWN_ISSUES.md](KNOWN_ISSUES.md) lists the full
set alongside what is still outstanding.
