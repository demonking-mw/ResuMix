from sentence_transformers import SentenceTransformer
import os

model_path = "all-mpnet-base-v2-local"
if not os.path.exists(model_path):
    # 1) download the model once
    model = SentenceTransformer("all-MiniLM-L12-v2")
    # 2) save it to a folder
    model.save(model_path)
