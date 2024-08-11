from flask import Flask, request, jsonify
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('consumer-service')


app = Flask(__name__)
PORT = 8080
host = '0.0.0.0'


@app.route('/messages', methods=['GET'])
def handle_get_message():
    message = request.args.get('message')
    if message:
        logger.info(f"Received message via GET: {message}")
        return jsonify({"status": "success", "message": message}), 200
    else:
        logger.error("No message received in GET request.")
        return jsonify({"status": "error", "message": "No message provided"}), 400


@app.route('/messages', methods=['POST'])
def handle_post_message():
    data = request.get_json()
    message = data.get('message') if data else None
    if message:
        logger.info(f"Received message via POST: {message}")
        return jsonify({"status": "success", "message": message}), 200
    else:
        logger.error("No message received in POST request.")
        return jsonify({"status": "error", "message": "No message provided"}), 400


if __name__ == '__main__':
    app.run(host=host, port=PORT)
