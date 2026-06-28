# backend/routes/bag_of_words.py
from flask import Blueprint, request, jsonify
import spacy
from collections import Counter

bag_of_words_bp = Blueprint('bag_of_words', __name__)

# Load the NLP language model pipeline
nlp = spacy.load("en_core_web_sm")

@bag_of_words_bp.route('/bag-of-words', methods=['POST', 'OPTIONS'])
def compute_bag_of_words():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.json or {}
    # Capture the raw text string directly from the frontend text area
    raw_text = data.get('text', '')
    
    if not raw_text.strip():
        return jsonify({"vocab": {}, "vector": []})

    # 1. Run the full text pipeline through spaCy
    doc = nlp(raw_text.lower())
    
    # 2. Extract clean, meaningful tokens (identical to Section 1 logic)
    clean_tokens = [
        token.text for token in doc 
        if token.text.strip() and not token.is_stop and not token.is_punct
    ]

    if not clean_tokens:
        return jsonify({"vocab": [], "vector": []})

    # 3. Calculate frequencies and build the indexed feature matrices
    counts = Counter(clean_tokens)
    vocab = sorted(list(counts.keys()))
    vector = [counts[word] for word in vocab]
    
    return jsonify({
        "vocab": vocab,
        "vector": vector
    })