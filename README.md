# 🤖 KSB Web-Product Information Chatbot

An **AI-powered multilingual chatbot** designed to provide accurate and context-aware answers about **KSB products and services**.  
This project integrates **web scraping, NLP preprocessing, embeddings, FAISS vector search, and Ollama LLM** with a **Streamlit-based chatbot interface**.  

---

## 🚀 Features
- 🌐 **Web Scraping**: Extracts product information from the KSB website.  
- 🧹 **Preprocessing**: Cleans and tokenizes multilingual text (English, Hindi, Marathi).  
- 🌍 **Multilingual Support**: Handles English, Hindi, and Marathi queries.  
- 🔍 **Semantic Search**: Embeddings + FAISS for fast similarity search.  
- 🧠 **LLM Integration**: Uses **Ollama models (e.g., Mistral)** for answer generation.  
- 💬 **Streamlit Chatbot**: User-friendly UI for interactive product Q&A.  

---

## 🛠️ Tech Stack
- **Python**  
- **BeautifulSoup, Requests** (web scraping)  
- **NLTK, IndicNLP** (preprocessing, tokenization)  
- **LangChain** + **Ollama** (LLM pipeline)  
- **SentenceTransformers** (multilingual embeddings)  
- **FAISS** (vector similarity search)  
- **Streamlit** (chatbot interface)  

---

## 📂 Project Structure


---

## ⚡ Workflow
1. **Scrape** → Extract product data from KSB’s website using `scraper.py`.  
2. **Preprocess** → Clean & tokenize the text with `preprocessing.py`.  
3. **Detect Language** → Identify and process English, Hindi, and Marathi text.  
4. **Embed + Index** → Generate embeddings and store them in FAISS using `embedding.py`.  
5. **Chatbot** → Query embeddings + LLM (`chatbot.py`).  
6. **Streamlit UI** → Launch chatbot with `app.py`.  

---

## ▶️ How to Run
### 1. Clone the Repository
```bash
git clone https://github.com/PriyankaThole1905/ksb-product-chatbot.git
cd ksb-product-chatbot

streamlit run app.py


