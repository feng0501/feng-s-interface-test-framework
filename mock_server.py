from flask import Flask, request, jsonify

app = Flask(__name__)

# 模拟一个简单的数据库，用来存放我们的宠物数据
pets_db = {
    1: {"id": 1, "name": "旺财", "status": "available"},
    2: {"id": 2, "name": "咪咪", "status": "pending"}
}

# 模拟 GET /pet/{petId} 接口：通过ID查询宠物
@app.route('/pet/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    pet = pets_db.get(pet_id)
    if pet:
        # 如果找到，返回200状态码和宠物信息
        return jsonify(pet), 200
    else:
        # 如果没找到，返回404状态码和错误信息
        return jsonify({"message": "Pet not found"}), 404

# 模拟 POST /pet 接口：新增宠物
@app.route('/pet', methods=['POST'])
def add_pet():
    # 获取请求中的JSON数据
    pet_data = request.get_json()
    pet_id = pet_data.get('id')
    # 将新宠物存入"数据库"
    pets_db[pet_id] = pet_data
    # 返回新增的宠物信息，状态码为200
    return jsonify(pet_data), 200

# 模拟 DELETE /pet/{petId} 接口：删除宠物（清理数据用）
@app.route('/pet/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    if pet_id in pets_db:
        del pets_db[pet_id]
        return '', 204  # 204状态码表示删除成功，无返回内容
    else:
        return jsonify({"message": "Pet not found"}), 404


@app.route('/pet/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    # 1. 检查宠物是否存在
    if pet_id not in pets_db:
        return jsonify({"message": "Pet not found"}), 404

    # 2. 获取客户端发来的新数据
    updated_data = request.get_json()

    # 3. 全量更新数据库中的宠物信息
    pets_db[pet_id] = updated_data

    # 4. 返回更新后的宠物信息，状态码 200
    return jsonify(updated_data), 200

if __name__ == '__main__':
    # 启动服务，host='0.0.0.0' 允许外部访问，port=5000 是端口号
    app.run(host='0.0.0.0', port=5000, debug=True)

