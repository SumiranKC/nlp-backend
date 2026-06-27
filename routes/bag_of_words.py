# backend/routes/bag_of_words.py
from flask import Blueprint, request, jsonify
from collections import Counter

bag_of_words_bp = Blueprint('bag_of_words', __name__)

@bag_of_words_bp.route('/bag-of-words', methods=['POST', 'OPTIONS'])
def compute_bag_of_words():
    # Handle incoming CORS preflight smoothly
    if request.method == 'OPTIONS':
        return '', 200

    data = request.json or {}
    # Expecting an array of preprocessed, tokenized words from the frontend
    tokens = data.get('tokens', [])
    
    if not tokens:
        return jsonify({"vocab": {}, "vector": []})

    # Count the raw frequencies of each token
    counts = Counter(tokens)
    
    # Sort vocabulary alphabetically to keep the vector layout consistent
    vocab = sorted(list(counts.keys()))
    
    # Generate the sequential feature vector array mapped to our vocabulary index
    vector = [counts[word] for word in vocab]
    
    return jsonify({
        "vocab": vocab,
        "vector": vector
    })