import json
from confluent_kafka import Producer
import socket
from django.conf import settings

conf = {
    'bootstrap.servers': settings.SECRETE_KEY_SERVICE['data']['data']['KAFKA_URI'],
    'client.id': socket.gethostname()
}


class ProducerKafka:
    def __init__(self) -> None:
        self.producer = Producer(conf)

    def publish(self, topic, key, body):
        print('Inside UserService: Sending to Kafka: ')
        print(body)
        self.producer.produce(topic, key=key, value=json.dumps(body))
        self.producer.flush()
