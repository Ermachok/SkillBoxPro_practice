import time
import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('producer-service')

URL_API = "https://techy-api.vercel.app/api/json"
PORT = 8080
host = 'localhost'


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


def send_to_consumer_service(message):
    try:
        url = f"http://{host}:{PORT}/messages"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json={"message": message}, headers=headers)
        if response.status_code == 200:
            logger.info("Message sent successfully to consumer-service.")
        else:
            logger.error(f"Failed to send message to consumer-service. Status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Exception occurred while sending message: {e}")


def producer_service(run_forever: bool = True, max_iterations: int = 100):
    iteration = 0
    pause_time = 1  # seconds
    while run_forever or iteration < max_iterations:
        phrase = generate_techy_phrase()
        if phrase:
            logger.info(f"Sending generated phrase: {phrase}")
            send_to_consumer_service(phrase)
        iteration += 1
        time.sleep(pause_time)

    logger.info("Producer service finished generating phrases.")


if __name__ == "__main__":
    producer_service(run_forever=False, max_iterations=100)
