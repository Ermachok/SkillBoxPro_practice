# Producer-Consumer Project

Два микросервиса: `producer_service` и `consumer_service`, взаимодействующих через RabbitMQ.

## Требования

- Python 3.10+
- Docker (для запуска RabbitMQ)
- pip (Python package manager)

## Установка зависимостей

Установите необходимые Python-библиотеки:

    ```bash
    pip install -r requirements.txt
    ```

## Запуск RabbitMQ

Проект использует RabbitMQ для обмена сообщениями между `producer_service` и `consumer_service`. Чтобы запустить RabbitMQ локально с использованием Docker, выполните следующие шаги:

1. Запустите RabbitMQ с помощью Docker:

    ```bash
    docker run -d --hostname my-rabbit --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
    ```

2. Проверьте, что RabbitMQ успешно запущен, перейдя в [RabbitMQ Management Interface](http://localhost:15672/). log/pass `guest`.

## Запуск микросервисов

### Запуск `consumer_service`

1. Убедитесь, что RabbitMQ запущен.
2. Запустите `consumer_service`, который будет слушать очередь RabbitMQ и обрабатывать сообщения:

    ```bash
    python consumer.py
    ```

### Запуск `producer_service`

1. Убедитесь, что `consumer_service` запущен.
2. Запустите `producer_service`, который будет генерировать и отправлять сообщения в RabbitMQ:

    ```bash
    python producer.py
    ```


