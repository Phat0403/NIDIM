from flask import Flask, request, jsonify
from flask_cors import CORS
import query


app = Flask(__name__)
CORS(app)

@app.route("/api/users", methods=['GET'])

def users():
    textQuery = request.args.get('textQuery')
    resultTextQuery = query.textQuery(textQuery)
    return jsonify(
        {
            "users": resultTextQuery
        }
    )
if  __name__ == "__main__":
    app.run(debug=True, port=8080)