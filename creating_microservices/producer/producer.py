import time
import logging
import pika
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('producer-service')

logging.getLogger('pika').setLevel(logging.WARNING)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

URL_API = "https://techy-api.vercel.app/api/json"
RABBITMQ_HOST = 'rabbitmq'
QUEUE_NAME = 'queue'


def generate_techy_phrase():
    try:
        response = requests.get(URL_API)
        if response.status_code == 200:
            data = response.json()
            return data.get("message", "No message received.")
        else:
            logger.error(f"Failed to fetch data from API. Status code: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        return None


def send_to_rabbitmq(message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)
        channel.basic_publish(exchange='',
                              routing_key=QUEUE_NAME,
                              body=message)
        logger.info(f"Message sent successfully to RabbitMQ: {message}")
        connection.close()
    except Exception as e:
        logger.error(f"Exception occurred while sending message to RabbitMQ: {e}")


def producer_service(run_forever: bool = True, max_iterations: int = 100):
    iteration = 0
    pause_time = 5  # seconds
    while run_forever or iteration < max_iterations:
        phrase = generate_techy_phrase()
        if phrase:
            logger.info(f"Sending generated phrase: {phrase}")
            send_to_rabbitmq(phrase)
        iteration += 1
        time.sleep(pause_time)

    logger.info("Producer service finished generating phrases.")


if __name__ == "__main__":
    producer_service(run_forever=False, max_iterations=100)
