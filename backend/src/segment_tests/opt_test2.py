from sentence_transformers import SentenceTransformer

# 1) download the model once
model = SentenceTransformer("all-mpnet-base-v2")

# 2) save it to a folder
model.save("all-mpnet-base-v2-local")
