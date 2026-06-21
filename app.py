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
    import os
    # Platforms inject a specific PORT environment variable dynamically
    port = int(os.environ.get("PORT", 5000))
    # Bind to 0.0.0.0 so the server accepts public traffic requests
    app.run(host='0.0.0.0', port=port, debug=False)