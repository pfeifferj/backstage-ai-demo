from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
import logging
from redis import Redis, ConnectionPool
import os
from urllib.parse import urlparse
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# auth = HTTPBasicAuth()

app.logger.setLevel(logging.DEBUG)

# hashed_password = generate_password_hash(os.getenv('BASIC_AUTH_PASS', 'secret'))
# users = {
    # os.getenv('BASIC_AUTH_USER', 'admin'): hashed_password
# }

# @auth.verify_password
# def verify_password(username, password):
    # if username in users:
        # return check_password_hash(users.get(username), password)
    # return False

enable_redis_forwarding = os.getenv('ENABLE_REDIS_FORWARDING', 'false').lower() in ['true', '1']

if enable_redis_forwarding:
    REDIS_URI = os.getenv('REDIS_URI', None)
    if REDIS_URI:
        parsed_uri = urlparse(REDIS_URI)
        redis_host = parsed_uri.hostname
        redis_port = parsed_uri.port
    else:
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        # redis_port = int(os.getenv('REDIS_PORT', 6379))
        redis_port = 6379

    redis_db = int(os.getenv('REDIS_DB', 0))
    pool = ConnectionPool(host=redis_host, port=redis_port, db=redis_db)
    redis_client = Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)


@app.route('/', methods=['OPTIONS'])
# @auth.login_required
def options_handler():
    headers = dict(request.headers)
    print(f"Received OPTIONS request with headers: {headers}")

    response = jsonify({"message": "OPTIONS request acknowledged"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    return response, 200

@app.route('/', methods=['POST'])
# @auth.login_required
def log_post():
    if request.is_json:
        data = request.get_json()
        app.logger.info(f"Received POST request with JSON data: {data}")
    else:
        data = request.form.to_dict()
        app.logger.info(f"Received POST request with form data: {data}")


    if 'enable_redis_forwarding' in request.args:
        data = request.json
        try:
            user_id = data[0]['user'].split('/')[-1]

            data_str = json.dumps(data)

            timestamp = data[0]['timestamp']
            redis_client.hset(f"user:{user_id}:events", timestamp, data_str)

            app.logger.info("Data sent to Redis.")
            return jsonify({"message": "Data successfully saved to Redis"}), 200
        except Exception as e:
            app.logger.error(f"Failed to save data to Redis: {e}")
            return jsonify({"message": "Failed to save data to Redis", "error": str(e)}), 500
        
    response = jsonify({"message": "POST request logged", "data": data})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    return response, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
