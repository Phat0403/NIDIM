from flask import Flask, request, jsonify
from flask_cors import CORS
import query
import os
import xl



app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/api/query/text", methods=['GET'])
def getTextQuery():
    dataQuery = request.args.get('query')
    resultQuery = query.textQuery(dataQuery)
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

@app.route('/getlink', methods=['POST'])
def getLink():
    data = request.get_json().get('data')
    data=xl.gom_laij(data)
    return jsonify({'data':data})


@app.route('/getname', methods=['POST'])
def getName():
    data = request.get_json().get('data')
    return jsonify({'data':xl.get_title(data)})





if  __name__ == "__main__":
    app.run(debug=True, port=8080)