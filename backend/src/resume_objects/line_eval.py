"""

the line_eval function scores every item passed in
takes in a list of requirements (string) and a list of items (Item class)
currently, no cache is used, could be a function for the future
"""

import os
import threading
from pathlib import Path
from dotenv import load_dotenv
import numpy as np
import gc
import torch

from sentence_transformers import SentenceTransformer

# backend/src/resume_objects/line_eval.py -> repository root
REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_LOCAL_MODEL_DIR = REPO_ROOT / "models" / "all-mpnet-base-v2"
DEFAULT_MODEL_ID = "sentence-transformers/all-mpnet-base-v2"

# Cosine similarity range mapped onto the 0-10 score scale. Sentence-transformer
# similarities for unrelated text sit near 0; a strong match is around 0.6-0.7.
SIMILARITY_FLOOR = 0.05
SIMILARITY_CEILING = 0.65
# The optimizer only picks items whose score improves the total, so a line must
# never score exactly zero or an entirely off-topic resume would render empty.
SCORE_FLOOR = 0.5

_MODEL_CACHE: dict[tuple[str, bool], SentenceTransformer] = {}
_MODEL_LOCK = threading.Lock()


def load_model(model_path: str, local_files_only: bool) -> SentenceTransformer:
    """Load the sentence-transformer once per process and reuse it.

    Loading takes seconds, and it used to happen on every single request.
    """
    key = (model_path, local_files_only)
    with _MODEL_LOCK:
        model = _MODEL_CACHE.get(key)
        if model is None:
            model = SentenceTransformer(model_path, local_files_only=local_files_only)
            _MODEL_CACHE[key] = model
        return model


def _cached_vectors(lines: list, dim: int):
    """Stack previously cached embeddings, or None if they cannot all be used."""
    vectors = []
    for line in lines:
        aux = getattr(line, "aux_info", None)
        if not isinstance(aux, dict):
            return None
        vec = aux.get("vec")
        if vec is None:
            return None
        array = np.asarray(vec, dtype=np.float32)
        if array.ndim != 1 or array.shape[0] != dim:
            return None
        vectors.append(array)
    return np.vstack(vectors) if vectors else None


def resolve_model_source() -> tuple[str, bool]:
    """
    Decide which sentence-transformer to load and whether it is already on disk.

    Order: OPT_MODEL_PATH > models/all-mpnet-base-v2 > public model id.
    Returns (source, local_files_only); a non-local source is downloaded once
    and then served from the Hugging Face cache.
    """
    configured = (os.getenv("OPT_MODEL_PATH") or "").strip()
    if configured:
        path = Path(configured).expanduser()
        if not path.is_absolute():
            path = REPO_ROOT / path
        if path.exists():
            return str(path), True
        return configured, False

    if DEFAULT_LOCAL_MODEL_DIR.exists():
        return str(DEFAULT_LOCAL_MODEL_DIR), True

    return DEFAULT_MODEL_ID, False


def line_eval(requirements: list[str], lines: list, no_cache: bool = False) -> bool:
    """
    Evaluates each Line in `lines` against the set of `requirements` and
    writes back a normalized score in line.score (0–10 scale).

    Args:
      requirements: list of requirement‐sentences (3–10 items).
      lines:        list of objects, each must have:
                      - `line.content_str` : the string to score
                      - `line.score`: will be overwritten with a float

    Side effects:
      Modifies each line in `lines`:
        line.score = normalized_score  # float in [0,10]

    Returns:
      True if scoring completed successfully, False otherwise.
    """

    requirements = [
        requirement.strip()
        for requirement in requirements
        if isinstance(requirement, str) and requirement.strip()
    ]
    if not requirements:
        print("WARNING: no requirements extracted; using neutral line scores")
        for line in lines:
            line.score = 10.0
        return True
    load_dotenv()
    model_path, local_files_only = resolve_model_source()
    try:
        model = load_model(model_path, local_files_only)
        req_vecs = model.encode(
            requirements, normalize_embeddings=True, show_progress_bar=False
        )  # shape (R, D)
        dim = req_vecs.shape[1]

        # 2) reuse cached line vectors when every line has one of the right size
        cached = None
        if not no_cache:
            cached = _cached_vectors(lines, dim)
        if cached is None:
            texts = [line.content_str for line in lines]
            line_vecs = model.encode(
                texts, normalize_embeddings=True, show_progress_bar=False
            )  # shape (N, D)
            for ln, vec in zip(lines, line_vecs):
                if not hasattr(ln, "aux_info") or not isinstance(ln.aux_info, dict):
                    ln.aux_info = {}
                ln.aux_info["vec"] = vec
        else:
            line_vecs = cached

        # 3) compute sim‐matrix (N_lines × N_requirements)
        sim_matrix = line_vecs @ req_vecs.T

        # 4) for each line take the max‐over‐requirements
        raw_scores = sim_matrix.max(axis=1)  # shape (N,), cosine similarity in [-1, 1]

        # 5) map similarity onto a fixed 0…10 scale.
        # An absolute scale keeps scores comparable between resumes and between
        # job descriptions. Min-max normalising here instead would force the
        # weakest line of every resume to 0 and the strongest to 10, however
        # relevant they actually are.
        scaled = (raw_scores - SIMILARITY_FLOOR) / (SIMILARITY_CEILING - SIMILARITY_FLOOR)
        norm_scores = SCORE_FLOOR + np.clip(scaled, 0.0, 1.0) * (10.0 - SCORE_FLOOR)

        # 6) write back into each line.score
        for line, sc in zip(lines, norm_scores):
            line.score = float(sc)

        try:
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except (RuntimeError, AssertionError):
            pass
        gc.collect()
        return True

    except Exception as e:
        print("ERROR: line_eval failed:", e)
        return False
