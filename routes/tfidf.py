# backend/routes/tfidf.py
from flask import Blueprint, request, jsonify
import spacy
import math

tfidf_bp = Blueprint('tfidf', __name__)
nlp = spacy.load("en_core_web_sm")

@tfidf_bp.route('/tfidf', methods=['POST', 'OPTIONS'])
def compute_tfidf():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.json or {}
    # Expecting an array of string documents: ["Doc 1 text...", "Doc 2 text..."]
    documents = data.get('docs', [])
    
    if not documents or not any(doc.strip() for doc in documents):
        return jsonify({"vocabulary": [], "matrix": []})

    # 1. Preprocess all documents using spaCy pipeline logic
    processed_docs = []
    all_vocab = set()
    
    for doc_text in documents:
        if not doc_text.strip():
            processed_docs.append([])
            continue
        parsed = nlp(doc_text.lower())
        tokens = [t.text for t in parsed if t.text.strip() and not t.is_stop and not t.is_punct]
        processed_docs.append(tokens)
        all_vocab.update(tokens)
        
    vocabulary = sorted(list(all_vocab))
    num_docs = len(documents)
    
    if not vocabulary:
        return jsonify({"vocabulary": [], "matrix": []})

    # 2. Compute TF-IDF Matrix Spaces
    matrix = []
    for tokens in processed_docs:
        doc_scores = []
        doc_len = len(tokens)
        
        for term in vocabulary:
            # Term Frequency (TF)
            tf = tokens.count(term) / doc_len if doc_len > 0 else 0
            
            # Inverse Document Frequency (IDF)
            docs_with_term = sum(1 for d in processed_docs if term in d)
            # Smooth IDF layout calculation to avoid divisions by zero
            idf = math.log((num_docs / (1 + docs_with_term))) + 1
            
            doc_scores.append(round(tf * idf, 4))
        matrix.append(doc_scores)

    return jsonify({
        "vocabulary": vocabulary,
        "matrix": matrix
    })