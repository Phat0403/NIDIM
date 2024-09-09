from flask import Flask, request, jsonify
from flask_cors import CORS
import query
import os


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/api/query/text", methods=['GET'])
def getTextQuery():
    queries = request.args.to_dict(flat=False)
    ids = queries.get('queries[id]', [])
    values = queries.get('queries[value]', [])
    data = []
    for id, value in zip(ids, values):
        data.append({'id': id, 'value': value})
    resultQuery = query.textQuery(data)
    return jsonify(
        {
            "data": resultQuery
        }
    )
@app.route("/api/query/image", methods=['POST'])
def postImageQuery():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file:
            filename = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            return jsonify({'message': 'File successfully uploaded', 'file_path': file_path}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route("/api/query/image", methods=['GET'])
def getImageQuery():
    resultQuery = query.imageQuery()
    return jsonify(
        {
            "data": resultQuery
        }
    )


if  __name__ == "__main__":
    app.run(debug=True, port=8080)