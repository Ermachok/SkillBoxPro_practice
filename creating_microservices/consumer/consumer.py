from flask import Flask, request, jsonify
import logging
import threading
import pika

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('consumer-service')

app = Flask(__name__)
PORT = 5672
RABBIT_HOST = 'rabbitmq'


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


def callback(ch, method, properties, body):
    message = body.decode()
    logger.info(f"Received message from RabbitMQ: {message}")


def consume_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST))
    channel = connection.channel()
    channel.queue_declare(queue='queue')

    channel.basic_consume(queue='queue', on_message_callback=callback, auto_ack=True)

    logger.info('Started consuming from RabbitMQ queue...')
    channel.start_consuming()


if __name__ == '__main__':
    rabbitmq_thread = threading.Thread(target=consume_rabbitmq, daemon=True)
    rabbitmq_thread.start()

    app.run(host='0.0.0.0', port=PORT)
