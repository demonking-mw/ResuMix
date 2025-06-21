from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-mpnet-base-v2")  # Sentence-BERT


def get_top_k(job_description, experiences, k=3):
    all_texts = [job_description] + experiences
    embeddings = model.encode(all_texts)

    job_vec = embeddings[0]
    exp_vecs = embeddings[1:]

    similarities = np.dot(exp_vecs, job_vec) / (
        np.linalg.norm(exp_vecs, axis=1) * np.linalg.norm(job_vec)
    )

    print(similarities)
    top_k_idx = similarities.argsort()[::-1][:k]
    top_k = [experiences[i] for i in top_k_idx]

    return top_k


job_desc = "We need someone skilled in Python backend development."
experience_list = [
    "Built a frontend web app using React and Redux.",
    "Developed RESTful APIs with Flask and deployed them to Amazon Web Services.",
    "Managed a Kubernetes cluster for scalable infrastructure.",
    "Worked on image classification using PyTorch.",
    "Designed backend systems for financial services in Django.",
]

ans = get_top_k(job_desc, experience_list, k=3)
print("Top matching experiences:\n", "\n".join(ans))
