from django.core.management.base import BaseCommand

from infrastructure.kafka.consumer import ConsumerKafka
from infrastructure.event.updateUser import updateVerifyEmail, updateOmiseKey


class Command(BaseCommand):
    help = 'Launches Listener for all message : Kafka'

    def handle(self, *args, **options):
        consumer_user_verify = ConsumerKafka('user_verify', updateVerifyEmail)
        consumer_user_verify.start()
        consumer_user_create_omise = ConsumerKafka(
            'user_create_omise', updateOmiseKey)
        consumer_user_create_omise.start()
