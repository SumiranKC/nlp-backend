# backend/app.py
from flask import Flask, make_response
from flask_cors import CORS
from routes.preprocessing import preprocessing_bp
from routes.tfidf import tfidf_bp
from routes.embeddings import embeddings_bp

app = Flask(__name__)

# 1. Enforce a bulletproof global CORS policy across all routes and sub-paths
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["POST", "GET", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

# 2. Add a global fallback interceptor specifically for browser OPTIONS requests
@app.before_request
def handle_preflight():
    from flask import request
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST,GET,OPTIONS")
        return response, 200

# 3. Register your blueprints cleanly
app.register_blueprint(preprocessing_bp, url_prefix='/api')
app.register_blueprint(tfidf_bp, url_prefix='/api')
app.register_blueprint(embeddings_bp, url_prefix='/api')

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)