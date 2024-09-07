@app.route('/getlink', methods=['GET'])
def get_link():
    data = request.get_json()
    url = data.get('url')
    # Ví dụ: trả về link cho url (có thể thay đổi theo cách bạn lưu trữ dữ liệu)
    link = xl.gom_laij(url)
    return jsonify({'link': link})
