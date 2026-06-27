from flask import Flask, render_template, request, jsonify
from engine import AfribrowseEngine

app = Flask(__name__)

# Initialize our search engine
engine = AfribrowseEngine()

@app.route("/")
def index():
    """Serves the main search engine interface."""
    return render_template("index.html")

@app.route("/search")
def search_api():
    """
    API endpoint that accepts a query parameter.
    Example: http://localhost:5000/search?q=python
    """
    query = request.args.get("q", "")
    if not query:
        return jsonify([])
    
    # Run the search via our engine
    search_results = engine.search(query)
    return jsonify(search_results)

if __name__ == "__main__":
    # Runs the server locally on http://127.0.0.1:5000
    app.run(debug=True, host="127.0.0.1", port=5000)