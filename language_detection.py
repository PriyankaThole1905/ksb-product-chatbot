# language_detection.py
from langdetect import detect

def detect_language(text):
    try:
        return detect(text)
    except:
        return 'en' # Default to English if detection fails

if __name__ == "__main__":
    text1 = "This is an English sentence."
    text2 = "यह एक हिंदी वाक्य है।"
    text3 = "हे एक मराठी वाक्य आहे."
    print(f"'{text1}' is in: {detect_language(text1)}")
    print(f"'{text2}' is in: {detect_language(text2)}")
    print(f"'{text3}' is in: {detect_language(text3)}")