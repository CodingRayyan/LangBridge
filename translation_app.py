import streamlit as st
from langdetect import detect
from transformers import pipeline
from difflib import get_close_matches

# Language mapping
lang_codes = {
    "english": "en", "french": "fr", "german": "de",
    "spanish": "es", "italian": "it", "hindi": "hi", "arabic": "ar"
}

st.title("🌍 Language Translator App")

# User input
text = st.text_area("Enter your text here:", "")

if text:
    try:
        src_lang = detect(text)
        st.write(f"**Detected Source Language Code:** `{src_lang}`")
    except Exception as e:
        st.error("Could not detect source language. Please enter more text.")

    # Target language input
    user_input = st.text_input("Enter target language (e.g. Arabic, French):")

    if user_input:
        matches = get_close_matches(user_input.lower(), lang_codes.keys(), n=1, cutoff=0.6)

        if matches:
            tar_lang_ff_corr = matches[0]
            tar_lang = lang_codes[tar_lang_ff_corr]

            st.write(f"**Target Language:** `{tar_lang_ff_corr}`")

            try:
                model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tar_lang}"
                translator = pipeline("translation", model=model_name)
                translation = translator(text)[0]['translation_text']
                st.success(f"**Translation:** {translation}")
            except Exception as e:
                st.error(f"Error loading model or translating: {e}")

        else:
            st.error("Target language not recognized. Please try again.")
