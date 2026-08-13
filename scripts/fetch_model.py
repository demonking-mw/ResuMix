#!/usr/bin/env python3
"""
Download the sentence-transformer used for resume scoring into models/.

Run once while online; afterwards resume generation needs no model download.
Usage:
    python scripts/fetch_model.py
    python scripts/fetch_model.py --model sentence-transformers/all-MiniLM-L6-v2
"""

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_ID = "sentence-transformers/all-mpnet-base-v2"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL_ID,
        help=f"Hugging Face model id to download (default: {DEFAULT_MODEL_ID})",
    )
    parser.add_argument(
        "--dest",
        default=None,
        help="Destination directory (default: models/<model name>)",
    )
    args = parser.parse_args()

    destination = Path(args.dest) if args.dest else REPO_ROOT / "models" / args.model.split("/")[-1]
    if destination.exists() and any(destination.iterdir()):
        print(f"Model already present at {destination}; nothing to do.")
        return 0

    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print(
            "sentence-transformers is not installed. Activate the virtualenv and run "
            "pip install -r requirements.txt first.",
            file=sys.stderr,
        )
        return 1

    print(f"Downloading {args.model} (about 420 MB for the default model)...")
    model = SentenceTransformer(args.model)
    destination.parent.mkdir(parents=True, exist_ok=True)
    model.save(str(destination))
    print(f"Saved to {destination}")
    print("Point OPT_MODEL_PATH at this directory if you move it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
