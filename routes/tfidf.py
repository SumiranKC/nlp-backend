# backend/routes/tfidf.py
from flask import Blueprint, request, jsonify
import re
import math

tfidf_bp = Blueprint('tfidf', __name__)

def get_tokens(text):
    lowercased_clean = re.sub(r'[^\w\s]', '', text.lower())
    return [t for t in lowercased_clean.split() if t]

@tfidf_bp.route('/api/tfidf', methods=['POST'])
def tfidf_matrix():
    data = request.json or {}
    docs = data.get('docs', [])
    
    # Isolate active text entries and skip completely blank fields
    valid_docs = [d for d in docs if d.strip()]
    num_docs = len(valid_docs)
    
    if num_docs == 0:
        return jsonify({"matrix": []})
        
    # Process text matrix maps for every singular text segment uploaded
    all_tokens = [get_tokens(doc) for doc in valid_docs]
    
    # Gather a flat, distinct collection of keywords found across all logs
    vocabulary = sorted(list(set([token for doc_tokens in all_tokens for token in doc_tokens])))
    
    matrix_data = []
    for word in vocabulary:
        # Evaluate term occurrences for every document container separately
        tfs = [doc_tokens.count(word) for doc_tokens in all_tokens]
        
        # Count how many total documents contain this target token
        df = sum(1 for doc_tokens in all_tokens if word in doc_tokens)
        
        # Smooth scaling evaluation: log(Total Documents / Document Frequency) + 1
        idf = math.log(num_docs / df) + 1 if df > 0 else 1
        
        # Calculate individual matrix scores
        tfidfs = [tf * idf for tf in tfs]
        
        matrix_data.append({
            "word": word,
            "tfs": tfs,
            "df": df,
            "idf": idf,
            "tfidfs": tfidfs
        })
        
    return jsonify({"matrix": matrix_data})