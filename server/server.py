from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/users", methods=['GET'])

def users():
    return jsonify(
        {
            "users":[
                'phat'
            ]
        }
    )
if  __name__ == "__main__":
    app.run(debug=True, port=8080)