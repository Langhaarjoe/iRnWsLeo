from flask import Flask, render_template, jsonify, abort, request
import search_backend
from search_backend.create_index import index_files
app = Flask(__name__)

index = index_files()

@app.route("/")
def root():
    return render_template('index.html')


@app.route('/search', methods=["POST"])
def search():
    json = request.get_json()
    if not json or json.get('query') is None:
        abort(400)

    query = str(json['query']).strip()
    return jsonify(
        results=search_backend.search(query, index)
    )


if __name__ == "__main__":
    app.run()
