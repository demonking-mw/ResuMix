from sentence_transformers import SentenceTransformer

# 1) download the model once
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

# 2) save it to a folder
model.save("all-mpnet-base-v2-local")
