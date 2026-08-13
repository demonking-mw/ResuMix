"""
Password hashing for local accounts.

Uses PBKDF2-HMAC-SHA256 from the standard library, so there is nothing extra to
install. Stored format:

    pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex>

Accounts created before hashing existed still hold the raw password. verify()
recognises those, and callers upgrade them to a hash on the next successful
login (see UserAuth.login_up).
"""

import hashlib
import hmac
import secrets

ALGORITHM = "pbkdf2_sha256"
ITERATIONS = 240_000
SALT_BYTES = 16


def hash_password(password: str) -> str:
    """Return an encoded hash for a plaintext password."""
    salt = secrets.token_bytes(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return f"{ALGORITHM}${ITERATIONS}${salt.hex()}${digest.hex()}"


def is_hashed(stored: str) -> bool:
    """True when the stored value is an encoded hash rather than a raw password."""
    return isinstance(stored, str) and stored.startswith(f"{ALGORITHM}$")


def verify_password(password: str, stored: str) -> bool:
    """Constant-time check of a plaintext password against the stored value."""
    if not isinstance(stored, str) or not isinstance(password, str):
        return False

    if not is_hashed(stored):
        # Legacy plaintext row; callers re-hash after a successful login.
        return hmac.compare_digest(password, stored)

    try:
        _, iterations, salt_hex, digest_hex = stored.split("$", 3)
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(iterations)
        )
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(digest.hex(), digest_hex)
