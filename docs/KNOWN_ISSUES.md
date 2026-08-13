# Known issues

What is still outstanding, and what was fixed. Everything listed under "Fixed"
has a reproduction that now passes; see the bottom of this file for how to
re-run the checks.

---

## Outstanding

### 1. Similarity does not separate "adjacent" work from "irrelevant" work

Scoring compares each line against the requirement sentences with
`all-mpnet-base-v2`. Measured against a backend job description:

| content | mean cosine |
| --- | --- |
| on-target backend bullets | 0.507 |
| adjacent engineering (frontend, devops) | 0.189 |
| unrelated hobbies | **0.223** |

Hobbies score marginally *higher* than other engineering work. On-target
content is separated cleanly, but everything below that is noise, so when a
resume is too long for one page the optimizer's choice between "frontend
experience" and "board game evenings" is close to arbitrary. No choice of score
window changes the ordering — it is a property of sentence similarity on this
kind of text. Improving it needs a different signal, such as asking the language
model to rate relevance directly.

### 2. Item order ignores relevance

Lines are ordered best-first inside an item, but items keep their authored order
within a section (`sorted(selected_ids, key=lambda x: x[1])` in
[resume.py](../backend/src/resume_objects/resume.py)). For a skills section that
means the most relevant skills line is not necessarily first. Reordering would
be wrong for chronological experience, so this needs a per-section policy rather
than a blanket change.

### 3. Tailoring only differentiates once the resume overflows a page

The optimizer fills the page, so a master resume that already fits produces the
same content for every job — only the bullet order inside each item changes.
That is the intended "fit one page" behaviour, but it surprises people who
expect visible tailoring from a short resume.

### 4. Identity hashes differ between identical requests

`tailored_resume_hash` and `result_id` change across two identical calls,
because the language model returns slightly different requirement sentences each
time (temperature 0.1), which shifts scores by a few tenths. The hashes are
documented as proving the dict and PDF came from *the same* call, which still
holds; they are not a content fingerprint.

### 5. Old deployment credentials are still in `.env`

The repository's `.env` (gitignored, never committed) carries a Neon PostgreSQL
connection string and an OpenAI key from the hosted deployment. Local mode needs
neither. Rotate both if they are still live, and clear `DATABASE_URL` so the app
uses the local SQLite file. `scripts/inspect_db.py` refuses to connect to a
remote server unless you pass `--remote`.

### 6. Reauth tokens cannot be revoked

Expiry lives entirely in the client-held JWT (one hour, re-signed on use). There
is no session table and no `jti`, so a leaked token stays valid until it expires
and the only way to invalidate everything is to change `JWT_REAUTH_SECRET`.
Acceptable for a single-user local install; it would need a session store before
this was exposed to a network.

### 7. Google sign-in cannot work offline

It needs a client id registered with Google and a reachable Google endpoint. The
button is hidden unless `VITE_GOOGLE_CLIENT_ID` is set, so email/password is the
offline path. Accounts created through Google use the Google `sub` as their
`uid` and cannot be signed into any other way.

### 8. Stylesheets pull fonts from Google Fonts

Seven CSS files `@import` from `fonts.googleapis.com`. Offline the UI falls back
to system fonts, which shifts the layout slightly. Self-hosting the two families
would make the interface fully offline. (This affects the web UI only — the
generated PDF embeds its own fonts.)

### 9. Mixed-script PDFs use a substitute font for CJK

Latin, Cyrillic and Greek render from a system TrueType family. CJK falls back
to reportlab's built-in CID fonts, because the Noto CJK files shipped by most
distributions use PostScript outlines that reportlab cannot embed. The result is
correct but the CJK glyphs are a different typeface. Point `RESUMIX_PDF_FONT` at
a TrueType-outline CJK font for a uniform look.

### 10. The embedding cache makes the stored resume large

Caching 768 floats per line costs roughly 17 KB per bullet, so a 100-line master
resume occupies a few MB in the database and is loaded on every request. Fine
for a local single-user file; it would want a separate table at scale.

### 11. `npm install` reports vulnerable transitive packages

`npm audit` flags advisories in the Vite/ESLint toolchain. Upgrading is a
dependency bump rather than an application change and was left alone.

### 12. `UserMod` is not reachable from the API

`backend/src/class_helper/user_mod.py` can change a user's name, password and
stored dictionaries, but no route calls it — there is no `PUT /user`. The
`KeyError` it used to raise is fixed, so wiring it up is now just a matter of
adding the endpoint.

### 13. Leftovers at the repository root

`grass` (an empty marker file), `test_resume.pdf`, `test_resume2.pdf`,
`resume_test_output.pdf`, `TODO.txt`, `debug_plan.txt`, `revamp_handoff.txt` and
an empty `package.json`/`package-lock.json` pair are all build residue or stale
notes. Harmless, but they are committed.

### 14. Module names say LaTeX, the code uses reportlab

`resume_objects/latex_templates.py` and `LTemplate` render with reportlab. The
only LaTeX dependency left is `pylatex.NoEscape` in `sections.py`. Renaming
would touch a lot of call sites and was left for later.

---

## Fixed

### Security

| Was | Now |
| --- | --- |
| Five queries in `user_auth.py` interpolated `uid`/`pwd`/`email` with f-strings | every statement uses bound parameters |
| Passwords stored and compared in plaintext | PBKDF2-HMAC-SHA256 with a per-user salt (`general_helper/passwords.py`); existing plaintext rows are re-hashed on the owner's next login |
| Login sent `uid` and `pwd` in the query string, so they reached the access log | the UI signs in with `POST /user`; `GET` still works for compatibility |
| Account deletion trusted the fields in the `WHERE` clause | `delete_eup` verifies the password hash and email before deleting |
| Responses echoed the stored password back to the client | the `pwd` field is stripped from every response |
| `alice@` and `ALICE@` were two accounts | emails are normalised before storage and comparison |
| Any password was accepted, including `""` | minimum length is enforced and the email must contain `@` |
| A token with no `exp` claim raised `KeyError` → 500 | missing `exp` is handled |
| Reauth compared `utcnow()` with a local-time `fromtimestamp()` | both sides are timezone-aware UTC |
| Werkzeug's interactive debugger was on by default | `FLASK_ENV=development` must be set explicitly |

Cross-user isolation was already sound and still is: `login_jwt` compares the
token's `uid` with the request's, so one account cannot read, overwrite,
generate from or delete another's data.

### Crashes and wrong status codes

| Was | Now |
| --- | --- |
| A section with no items raised `ValueError` → **500 on every generation**, and "+ Add New Section" always creates one | empty sections are skipped, and are not printed in the PDF |
| `/api/generate-resume-full` always 500'd (`ndarray is not JSON serializable`) | shared `json_safe` helper converts numpy values |
| Any `/resume*` request without a JSON content type returned 415 | a tolerant `Request` subclass lets reqparse read the query string |
| Auth failure on `POST /resume` returned 500 (`cannot unpack non-iterable bool`) | returns 401 |
| Validation failure on `POST /resume` returned 500 | returns 400 |
| Language-model failures surfaced as a bare 500 or an HTML error page | typed `ResumeGenerationError` → 400 with an actionable message |
| A failed database write was reported as `200 "Resume updated successfully"` | `DatabaseUnavailable` propagates → 503, no silent data loss |
| `UserMod.modify()` raised `KeyError: 'uid'` | uses `self.uid` |
| The resume-save fallback used a key that is never set | uses `args["uid"]` |
| Importing anything from `segment_tests` ran the script, called the model and wrote PDFs | the bodies are behind `if __name__ == "__main__"`, and `test_resume_dict` is importable |
| `backend/test_db.py` could not run at all | replaced by `scripts/inspect_db.py` |
| `python -m unittest discover -s backend/tests` failed | `backend/tests/__init__.py` added |

### Output quality

| Was | Now |
| --- | --- |
| Scores were min-max normalised, so the worst line always got 0.00 and the best 10.00 no matter how relevant | absolute scale mapped from cosine similarity: an irrelevant resume scores 0.5–0.9, a relevant one 7.5–10.0 |
| Bullets rendered weakest-first — the 0.00 line led, the 10.00 line came last | best first |
| `line.score` was never persisted or returned | stored in the resume and included in the tailored dict |
| An empty job description silently produced an untailored resume | rejected with `job_description_too_short` |
| Sections whose items were all dropped still printed their heading | skipped |
| `<div>`, `<10ms` and similar text was silently deleted by reportlab's markup parser | escaped, while balanced `<b>`, `<i>` and `<a href=…>` still format as documented |
| Cyrillic, Greek, CJK and emoji rendered as ■ | a Unicode TrueType family is registered automatically, with CID fonts for CJK |
| The UI let you add unlimited title fields; more than four rendered mangled | the button stops at four |

### Usability

| Was | Now |
| --- | --- |
| Generation was blocked until you changed a weight or bias slider, with the message "Please complete the previous steps" | only blocked when the resume has no items, and the message says exactly what to add |
| A wrong password reset the login form with no message, because the 401 interceptor reloaded the page | the error is shown; the interceptor only redirects when a real session expires, and then says so |
| "Status Overview" read "Will be implemented later" | shows resume state, tweak state and item count |
| "Forgot Password?" linked to a route that does not exist | removed |
| `/resume-form` and `/demo` were unfinished pages reachable in a normal session | removed, along with the duplicate wiki component |
| The sentence-transformer was reloaded on every request | cached per process |
| Cached line embeddings were never reused (the check tested attributes that never exist) | reused when they match the model, which is roughly a 3x speedup on scoring |
| Constructing any `Resume` or `Line` required a configured language model | the client is created on first use |
| `test_api.sh` slept 18 seconds then ran `pkill -f`, and reformatted the repo | polls `/health` and kills only its own child |

### Found in a second exploration pass

| Was | Now |
| --- | --- |
| A generation started before an edit wrote the pre-edit resume back when it finished, silently discarding the edit | the write-back re-checks the stored resume and skips if it changed while generating |
| Saving the master resume threw away every cached embedding, because the editor never receives them | vectors are carried over for lines whose text did not change; only edited lines are re-embedded |
| Generation read the resume from the auth payload, which `vec_rip` had already stripped, so the cache was never reused | the stored row is read directly, falling back to the auth payload |
| `/resume/optimize/full` returned 768 floats per line to the client (142 KB response) | embeddings are stripped from the response (59 KB) |
| A JSON body that was an array or a number crashed reqparse with a `TypeError` → 500 | rejected with 400 |
| `%s` inside a SQL string literal was rewritten as `?`, so `LIKE '%stuff%'` silently matched nothing and `'50%s off'` was stored as `'50? off'` | translation skips quoted literals and only runs when parameters are supplied |
| `SQLITE:///path` (uppercase scheme) silently fell back to the default database file | scheme matching is case-insensitive |

---

## Re-running the checks

```bash
source venv/bin/activate

# unit tests
python -m unittest discover -s backend/tests -t .

# a full local round trip
./scripts/start.sh
```

The behaviours in the tables above were verified against a running local stack
(SQLite, a local OpenAI-compatible endpoint, `all-mpnet-base-v2` from `models/`),
including a browser run through signup → master resume → generate → download.
