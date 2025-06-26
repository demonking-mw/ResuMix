"""

the line_eval function scores every item passed in
takes in a list of requirements (string) and a list of items (Item class)
currently, no cache is used, could be a function for the future
"""

import os
from dotenv import load_dotenv
import numpy as np

from sentence_transformers import SentenceTransformer


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

    load_dotenv()
    model_path = os.getenv("OPT_MODEL_PATH")
    try:
        # 1) load & encode requirements once, with L2‐norm
        model = SentenceTransformer(model_path)
        req_vecs = model.encode(
            requirements, normalize_embeddings=True, show_progress_bar=False
        )  # shape (R, D)

        # 2.0) use cache if possible
        if no_cache or not hasattr(lines[0], "aux_info") or "vec" not in lines[0].aux_info:
            print("DEBUG: Re-generating vectors")
            # no cache, encode everything
            # 2) pull out all texts and embed in one batch
            texts = [line.content_str for line in lines]
            line_vecs = model.encode(
                texts, normalize_embeddings=True, show_progress_bar=False
            )  # shape (N, D)
            # put that shit back in
            for ln, vec in zip(lines, line_vecs):
                if not hasattr(ln, "aux_info"):
                    print("DEBUG: BAD AUX INFO")
                    ln.aux_info = {}
                ln.aux_info["vec"] = vec
        else:
            line_vecs = np.vstack([ln.aux_info["vec"] for ln in lines])

        # 3) compute sim‐matrix (N_lines × N_requirements)
        sim_matrix = line_vecs @ req_vecs.T

        # 4) for each line take the max‐over‐requirements
        raw_scores = sim_matrix.max(axis=1)  # shape (N,)

        # 5) normalize raw_scores → 0…10
        mn, mx = raw_scores.min(), raw_scores.max()
        if mx > mn:
            norm_scores = (raw_scores - mn) / (mx - mn) * 10.0
        else:
            # all lines identical similarity ⇒ give them full marks
            norm_scores = np.ones_like(raw_scores) * 10.0

        # 6) write back into each line.score
        for line, sc in zip(lines, norm_scores):
            line.score = float(sc)

        return True

    except Exception as e:
        print("DEBUG: line_eval failure. Error:", e)
        # you could log e here if you want more diagnostics
        return False
