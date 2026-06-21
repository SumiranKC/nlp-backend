# backend/app.py
from flask import Flask
from flask_cors import CORS

# Import your modular blueprint instances straight from the routes subfolder
from routes.preprocessing import preprocessing_bp
from routes.bag_of_words import bag_of_words_bp
from routes.tfidf import tfidf_bp
from routes.embeddings import embeddings_bp

app = Flask(__name__)

# Apply comprehensive CORS policies to verify local web app handshakes securely
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# Register the independent module Blueprints into the live operational engine
app.register_blueprint(preprocessing_bp)
app.register_blueprint(bag_of_words_bp)
app.register_blueprint(tfidf_bp)
app.register_blueprint(embeddings_bp)

if __name__ == '__main__':
    # Initialize development server environment looping on port 5000
    app.run(host='127.0.0.1', port=5000, debug=True)