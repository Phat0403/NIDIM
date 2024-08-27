from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/api/users", methods=['GET'])

def users():
    textQuery = request.args.get('textQuery')
    print(textQuery)
    return jsonify(
        {
            "users":[
                textQuery
            ]
        }
    )
if  __name__ == "__main__":
    app.run(debug=True, port=8080)