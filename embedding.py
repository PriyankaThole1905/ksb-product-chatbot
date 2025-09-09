# embedding.py
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

PROCESSED_DIR = "processed_data"
INDEX_FILE = "website_embeddings.faiss"
EMBEDDING_MODEL = "paraphrase-multilingual-mpnet-base-v2" # A good multilingual model

def generate_embeddings(processed_dir=PROCESSED_DIR, embedding_model_name=EMBEDDING_MODEL):
    model = SentenceTransformer(embedding_model_name)
    documents = []
    filepaths = []
    for filename in os.listdir(processed_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(processed_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
                documents.append(text)
                filepaths.append(filepath)
    embeddings = model.encode(documents)
    return embeddings, filepaths

def index_embeddings(embeddings, index_file=INDEX_FILE):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension) # Consider IndexIVFFlat for larger datasets
    index.add(embeddings)
    faiss.write_index(index, index_file)
    return index

def load_index(index_file=INDEX_FILE):
    if os.path.exists(index_file):
        return faiss.read_index(index_file)
    return None

if __name__ == "__main__":
    embeddings, filepaths = generate_embeddings()
    if embeddings is not None and len(embeddings) > 0:
        index = index_embeddings(np.array(embeddings).astype('float32'))
        print(f"Embeddings generated and indexed in: {INDEX_FILE}")
    else:
        print("No processed data found to generate embeddings.")