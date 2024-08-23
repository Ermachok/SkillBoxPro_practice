from flask import Flask, request, jsonify
import logging
import threading
import pika
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('consumer-service')

app = Flask(__name__)
APP_PORT: int = 8080
RABBIT_HOST: str = 'rabbitmq'
RABBIT_PORT: int = 5672


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


def wait_for_rabbitmq(host: str, port: int = 5672, timeout: int = 30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
            connection.close()
            logger.info("RabbitNQ is available")
            return True
        except Exception as e:
            logger.info(f"Waiting for RabbitMQ, exception = {e}")
            time.sleep(3)
    logger.error("RabbitMQ didn't become available")
    return False


def consume_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT))
    channel = connection.channel()
    channel.queue_declare(queue='queue')

    channel.basic_consume(queue='queue', on_message_callback=callback, auto_ack=True)

    logger.info('Started consuming from RabbitMQ queue...')
    channel.start_consuming()


if __name__ == '__main__':
    if wait_for_rabbitmq(host=RABBIT_HOST, port=RABBIT_PORT):
        rabbitmq_thread = threading.Thread(target=consume_rabbitmq, daemon=True)
        rabbitmq_thread.start()

        app.run(host='0.0.0.0', port=APP_PORT)
    else:
        logger.error("Exiting because RabbitMq isn't alive")
