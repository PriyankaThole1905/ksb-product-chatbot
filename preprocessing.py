# preprocessing.py
import os
import nltk
import re
from indicnlp.tokenize import indic_tokenize
from indicnlp.morph import unsupervised_morph

nltk.download('punkt')

DATA_DIR = "scraped_data"
PROCESSED_DIR = "processed_data"

def preprocess_text(text, language='en'):
    text = re.sub(r'[^\w\s]', '', text) # Remove punctuation
    text = text.lower()
    tokens = []
    if language == 'en':
        tokens = nltk.word_tokenize(text)
        # You can add more English-specific preprocessing here (e.g., stop word removal, lemmatization)
    elif language in ['hi', 'mr']:
        for token in indic_tokenize.trivial_tokenize(text):
            tokens.append(token)
        # Trying unsupervised morphology for potential stemming
        analyzer = unsupervised_morph.UnsupervisedMorphAnalyzer(lang=language)
        stemmed_tokens = [analyzer.stem(word) for word in tokens]
        return " ".join(stemmed_tokens)
    return " ".join(tokens)

def process_scraped_data(data_dir=DATA_DIR, processed_dir=PROCESSED_DIR):
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()

            # Basic language detection (you might need a more robust method later)
            language = 'en' # Default to English, you'll need to improve this
            if re.search(r'[\u0900-\u097F]', text): # Check for Devanagari script (Hindi/Marathi)
                language = 'hi' # Assuming Hindi if Devanagari script is found for now
                # More sophisticated language detection needed here

            processed_text = preprocess_text(text, language)
            output_filepath = os.path.join(processed_dir, filename)
            with open(output_filepath, 'w', encoding='utf-8') as outfile:
                outfile.write(processed_text)

if __name__ == "__main__":
    process_scraped_data()
    print(f"Processed data saved in: {PROCESSED_DIR}")