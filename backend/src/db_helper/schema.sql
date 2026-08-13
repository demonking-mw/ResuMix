-- ResuMix local database schema (SQLite).
--
-- Mirrors the PostgreSQL `data` table used by the hosted deployment.
-- JSONB columns are stored as TEXT here; the SQLite backend encodes and decodes
-- them so application code keeps seeing plain Python dicts.

CREATE TABLE IF NOT EXISTS data (
    uid       TEXT PRIMARY KEY,
    user_name TEXT,
    pwd       TEXT,          -- PBKDF2 hash, see general_helper/passwords.py
    email     TEXT NOT NULL UNIQUE,
    auth_type TEXT,
    userinfo  TEXT DEFAULT '{}',
    resumeinfo TEXT DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS data_email_idx ON data (email);
