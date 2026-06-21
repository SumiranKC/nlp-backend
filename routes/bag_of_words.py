from flask import Blueprint, request, jsonify
import re

bag_of_words_bp = Blueprint('bag_of_words', __name__)

@bag_of_words_bp.route('/api/bag-of-words', methods=['POST', 'OPTIONS'])
def bag_of_words():
    data = request.json or {}
    raw_text = data.get('text', '')
    
    # Standard clean and split tokenization
    lowercased_clean = re.sub(r'[^\w\s]', '', raw_text.lower())
    tokens = [t for t in lowercased_clean.split() if t]
    
    # Extract alpha-sorted unique vocabulary terms
    vocabulary = sorted(list(set(tokens)))
    
    # Compute frequency frequencies mapping matrix
    frequency_map = {}
    for token in tokens:
        frequency_map[token] = frequency_map.get(token, 0) + 1
        
    vector_array = [frequency_map.get(word, 0) for word in vocabulary]
    
    return jsonify({
        "vocabulary": vocabulary,
        "frequency_map": frequency_map,
        "vector_array": vector_array
    })