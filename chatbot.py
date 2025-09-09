# chatbot.py
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from language_detection import detect_language
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
import nltk

INDEX_FILE = "website_embeddings.faiss"
PROCESSED_DIR = "processed_data"
EMBEDDING_MODEL = "paraphrase-multilingual-mpnet-base-v2"
OLLAMA_MODEL = "mistral"  # Or any other multilingual model you have on Ollama

nltk.download('punkt')

def load_index(index_file=INDEX_FILE):
    if os.path.exists(index_file):
        return faiss.read_index(index_file)
    return None

def load_processed_data(processed_dir=PROCESSED_DIR):
    documents = []
    filepaths = []
    for filename in os.listdir(processed_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(processed_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                documents.append(f.read())
                filepaths.append(filepath)
    return documents, filepaths

def search_index(index, query, model, top_k=3):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding).astype('float32'), top_k)
    return D[0], I[0]

class FAISSRetriever(BaseRetriever):
    index: faiss.Index
    documents: list[str]
    filepaths: list[str]
    model: SentenceTransformer
    top_k: int = 3

    def _get_relevant_documents(self, query: str) -> list[Document]:
        query_embedding = self.model.encode([query])
        D, I = self.index.search(np.array(query_embedding).astype('float32'), self.top_k)
        relevant_docs = []
        for i in I[0]:
            relevant_docs.append(Document(page_content=self.documents[i], metadata={"source": self.filepaths[i]}))
        return relevant_docs

from langchain_ollama import OllamaLLM


def create_ollama_qa_chain(index, documents, filepaths, model, ollama_model_name=OLLAMA_MODEL):
    llm = OllamaLLM(model=ollama_model_name)

    prompt_template = """Answer the following question based on the context provided. If you cannot find the answer in the context, just say "I don't know."

    Context:
    {context}

    Question:
    {question}

    Answer:"""
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    retriever = FAISSRetriever(index=index, documents=documents, filepaths=filepaths, model=model, top_k=3)
    return RetrievalQA.from_llm(llm=llm, retriever=retriever, prompt=PROMPT)

if __name__ == "__main__":
    index = load_index()
    documents, filepaths = load_processed_data()
    model = SentenceTransformer(EMBEDDING_MODEL)

    if index and documents:
        qa_chain = create_ollama_qa_chain(index, documents, filepaths, model)
        while True:
            user_query = input("You: ")
            if user_query.lower() == 'exit':
                break
            response = qa_chain.invoke({"query": user_query})
            print("Chatbot:", response['result'])
    else:
        print("Please ensure the index file and processed data are available. Run embedding.py first.")