import json

from flask import jsonify, request

from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token

from __main__ import app, env_values, jwt
from src.data_manager import DataManager


data_manager = DataManager()

@app.route('/api/v1/token', methods=['POST'])
def token():
    try:
        data = request.get_json()

        permissions = ""

        if "read" in data and data['read']:
            permissions += "R"
        if "write" in data and data['write']:
            permissions += "W"
        if "delete" in data and data['delete']:
            permissions += "D"
        if "update" in data and data['update']:
            permissions += "U"

        if "password" in data.keys() and data['password'] == env_values['PASSWORD']:
            return jsonify({
                'access_token': create_access_token(identity=permissions),
                'refresh_token': create_refresh_token(identity=permissions),
                'permissions': permissions
            }), 200
        else:
            return jsonify({'msg': 'Unauthorized'}), 401

    except Exception as e:
        print(e)
        return jsonify({'msg': 'Bad Request'}), 400


@app.route('/api/v1/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    return jsonify({
        'access_token': create_access_token(identity=current_user),
        'permissions': current_user
    }), 200


@app.route('/api/v1/queue', methods=['GET', 'POST', 'PUT'])
@jwt_required()
def queue():
    current_user = get_jwt_identity()

    try:
        if request.method == 'GET':
            if "R" in current_user:
                response = {}

                start_id = request.args.get('start_id')
                end_id = request.args.get('end_id')
                id = request.args.get('id')

                if start_id and end_id and not id:
                    start_id = int(start_id)
                    response['start_id'] = start_id

                    end_id = int(end_id)
                    response['end_id'] = end_id

                    if start_id > end_id:
                        return jsonify({'msg': 'start_id should be smaller or equal than end_id'}), 400

                    response = data_manager.get_data(keys=[str(i) for i in range(start_id, end_id + 1)])

                elif id and not start_id and not end_id:
                    id = json.loads(id)
                    
                    if type(id) is not list:
                        id = [str(id)]
                    else:
                        id = [str(i) for i in id]

                    response = data_manager.get_data(keys=id)

                    if response == {}:
                        return jsonify({'msg': 'No data found'}), 404

                elif id and start_id and end_id:
                    return jsonify({'msg': 'You should use either id or start_id and end_id'}), 400
            
                elif not id and not start_id and not end_id:
                    response = data_manager.get_data()

                return jsonify(response), 200
            
            else:
                return jsonify({'msg': 'Unauthorized'}), 401

        elif request.method == 'POST':
            if "W" in current_user:
                try:
                    data = request.get_json()

                    for key in data.keys(): 
                        if "description" not in data[key] or "name" not in data[key] or "queue_list" not in data[key] or len(data[key].keys()) != 3:
                            return jsonify({'msg': 'Bad Request'}), 400

                    if data_manager.add_data(data) == -1:
                        return jsonify({'msg': 'Data already exists'}), 409

                    return jsonify({'msg': 'Data added'}), 201
                except Exception as e:
                    print(e)
                    return jsonify({'msg': 'Bad Request'}), 400
            else:
                return jsonify({'msg': 'Unauthorized'}), 401

        elif request.method == 'PUT':
            if "U" in current_user:
                try:
                    data = request.get_json()

                    for key in data.keys():
                        if "description" not in data[key] or "name" not in data[key] or "queue_list" not in data[key] or len(data[key].keys()) != 3:
                            return jsonify({'msg': 'Bad Request'}), 400

                    data_manager.add_data(data, update=True)

                    return jsonify({'msg': 'Data updated'}), 200
                except Exception as e:
                    print(e)
                    return jsonify({'msg': 'Bad Request'}), 400
            else:
                return jsonify({'msg': 'Unauthorized'}), 401

    except Exception as e:
        print(e)
        print(data_manager)
        return jsonify({'msg': 'Bad Request'}), 400
