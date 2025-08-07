from sentence_transformers import SentenceTransformer
import os

model_path = "all-mpnet-base-v2-local"
if not os.path.exists(model_path):
    # 1) download the model once
    model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")
    # 2) save it to a folder
    model.save(model_path)

