import json
import sys
import threading
from confluent_kafka import Consumer
from confluent_kafka import KafkaError
from confluent_kafka import KafkaException
from infrastructure.kafka.setting import *


class ConsumerKafka(threading.Thread):
    def __init__(self, topic, func):
        threading.Thread.__init__(self)
        self.topic = topic
        self.func = func
        self.consumer = Consumer(CONF_KAFKA)

    def run(self):
        print("Start Consumer "+self.topic)

        try:
            self.consumer.subscribe([self.topic])
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        sys.stderr.write(
                            "%% %s [%d] reached end at offset %d\n" %
                            (msg.topic(), msg.partition(), msg.offset()))
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    print('%% %s [%d] at offset %d with key %s:\n' %
                          (msg.topic(), msg.partition(), msg.offset(),
                           str(msg.key())))
                    print(msg.value())
                    data = json.loads(msg.value())
                    # print(data['email'])
                    print(type(msg.topic()),msg.topic())
                    self.func(msg.topic(),msg.key().decode("utf-8"),data)
        finally:
            self.consumer.close()
