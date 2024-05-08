from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
import logging
from redis import Redis, ConnectionPool
import os
from urllib.parse import urlparse
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)

# enable_redis_forwarding = os.getenv('ENABLE_REDIS_FORWARDING', 'false').lower() in ['true', '1']
enable_redis_forwarding = True

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
def options_handler():
    headers = dict(request.headers)
    print(f"Received OPTIONS request with headers: {headers}")

    response = jsonify({"message": "OPTIONS request acknowledged"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    return response, 200

@app.route('/', methods=['POST'])
def log_post():
    if request.is_json:
        data = request.get_json()
        app.logger.info(f"Received POST request with JSON data: {data}")
    else:
        data = request.form.to_dict()
        app.logger.info(f"Received POST request with form data: {data}")

    if 'enable_redis_forwarding' in request.args:
        try:
            # Check if the received data is a list of events
            if isinstance(data, list):
                for event in data:
                    # Add the current timestamp to the event
                    event['timestamp'] = datetime.now().isoformat()

                    # Convert the event to JSON string
                    event_json = json.dumps(event)

                    # Push the event JSON to the Redis list
                    redis_client.rpush(events_key, event_json)

                app.logger.info(f"Events sent to Redis. Key: {events_key}")
                return jsonify({"message": f"Events pushed to {events_key}"}), 200
            else:
                # Add the current timestamp to the event
                data['timestamp'] = datetime.now().isoformat()

                # Convert the event to JSON string
                data_json = json.dumps(data)

                # Push the event JSON to the Redis list
                redis_client.rpush(events_key, data_json)

                app.logger.info(f"Event sent to Redis. Key: {events_key}")
                return jsonify({"message": f"Event pushed to {events_key}"}), 200
        except redis.RedisError as e:
            app.logger.error(f"Failed to save event(s) to Redis: {e}")
            return jsonify({"message": "Failed to save event(s) to Redis", "error": str(e)}), 500
        except Exception as e:
            app.logger.error(f"An error occurred: {e}")
            return jsonify({"message": "An error occurred", "error": str(e)}), 500
    else:
        return jsonify({"message": "Event(s) received but not pushed to Redis"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
