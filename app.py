import streamlit as st
import os
from chatbot import create_ollama_qa_chain, load_index, load_processed_data
from sentence_transformers import SentenceTransformer

# Page configuration
st.set_page_config(page_title='KSB Chatbot', page_icon='🤖')
st.title('KSB Product Information Chatbot')

# Language selection
language = st.selectbox('Select Language:', ['English', 'Hindi', 'Marathi'])
st.markdown('**Powered by AI and Web Scraping**')

# Embedding model
EMBEDDING_MODEL = 'paraphrase-multilingual-mpnet-base-v2'

# Load QA chain with caching
@st.cache_resource
def load_qa_chain():
    index = load_index()
    documents, filepaths = load_processed_data()
    model = SentenceTransformer(EMBEDDING_MODEL)
    if index and documents:
        return create_ollama_qa_chain(index, documents, filepaths, model)
    return None

qa_chain = load_qa_chain()

# Chat interface
if qa_chain:
    user_query = st.text_input(f'Ask me anything about KSB products in {language}:', '')
    if user_query:
        with st.spinner('🤔 Thinking...'):
            response = qa_chain.invoke({'query': user_query})
        st.markdown(f'**Chatbot:** {response["result"]}')
else:
    st.error('Error loading chatbot. Make sure embeddings are generated.')

# Footer
st.markdown('---')
st.markdown('Developed by Ksb tech team')
