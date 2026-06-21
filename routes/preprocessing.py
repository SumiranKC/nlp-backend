# backend/routes/preprocessing.py
from flask import Blueprint, request, jsonify
import re
import spacy

preprocessing_bp = Blueprint('preprocessing', __name__)

# Load the comprehensive, industry-standard English language model pipeline
# It automatically bundles extensive stopword files and context-aware lemma maps
nlp = spacy.load("en_core_web_sm")

# @preprocessing_bp.route('/api/preprocess', methods=['POST'])
@preprocessing_bp.route('/preprocess', methods=['POST', 'OPTIONS'])
def preprocess_text():
    data = request.json or {}
    raw_text = data.get('text', '')
    
    # --- STAGE 1: ADVANCED NORMALIZATION ---
    # Strip Email Addresses using clean regex boundaries
    text_no_emails = re.sub(r'\S+@\S+\.\S+', '', raw_text)
    # Strip URL Hyperlinks
    text_no_urls = re.sub(r'https?://\S+|www\.\S+', '', text_no_emails)
    # Cast to lowercase and clear structural punctuation marks
    lowercased = text_no_urls.lower()
    cleaned_string = re.sub(r'[^\w\s]', '', lowercased)
    
    # Run the cleaned text through spaCy's language model processing pipeline
    # spaCy instantly parses parts of speech, dependencies, and core lemmas
    doc = nlp(cleaned_string)
    
    # --- STAGE 2: TOKENIZATION ---
    # Extract structural text strings while filtering any residual whitespace blocks
    tokens = [token.text for token in doc if token.text.strip()]
    
    # --- STAGE 3: STOPWORD REMOVAL ---
    # Use spaCy's built-in statistical stopword evaluator flag (.is_stop)
    filtered_tokens = [token.text for token in doc if not token.is_stop and token.text.strip()]
    
    # --- STAGE 4: LEMMATIZATION ---
    # Grab the true base contextual dictionary root using spaCy's native attribute (.lemma_)
    lemmatized_tokens = [token.lemma_ for token in doc if not token.is_stop and token.text.strip()]
    
    return jsonify({
        "cleaned_text": cleaned_string.strip(),
        "tokens": tokens,
        "filtered_tokens": filtered_tokens,
        "lemmatized_tokens": lemmatized_tokens
    })