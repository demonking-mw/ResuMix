from sentence_transformers import SentenceTransformer
import os

model_path = "all-mpnet-base-v2-local"
# 1) download the model once
model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
# 2) save it to a folder
model.save(model_path)
print(f"Model saved to {model_path}")
