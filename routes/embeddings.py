from flask import Blueprint, request, jsonify
import math

embeddings_bp = Blueprint('embeddings', __name__)

# Static simulated 2D space coordinate mappings registry
WORD_VECTORS = {
    "king": {"x": 0.80, "y": 0.85},
    "queen": {"x": 0.82, "y": 0.70},
    "man": {"x": 0.20, "y": 0.85},
    "woman": {"x": 0.22, "y": 0.70},
    "apple": {"x": 0.45, "y": 0.20},
    "orange": {"x": 0.50, "y": 0.15},
    "computer": {"x": 0.85, "y": 0.35},
    "coding": {"x": 0.90, "y": 0.30}
}

@embeddings_bp.route('/api/embeddings', methods=['POST'])
def word_embeddings():
    data = request.json or {}
    word_a = data.get('wordA', '')
    word_b = data.get('wordB', '')
    
    vec_a = WORD_VECTORS.get(word_a, {"x": 0.0, "y": 0.0})
    vec_b = WORD_VECTORS.get(word_b, {"x": 0.0, "y": 0.0})
    
    # Euclidean distance computation formula vector loop
    dx = vec_b['x'] - vec_a['x']
    dy = vec_b['y'] - vec_a['y']
    euclidean_distance = math.sqrt(dx*dx + dy*dy)
    
    return jsonify({
        "vecA": vec_a,
        "vecB": vec_b,
        "distance": euclidean_distance
    })