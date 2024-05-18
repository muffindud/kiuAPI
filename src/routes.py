from flask import jsonify, request

from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token

from __main__ import app, env_values, jwt

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
