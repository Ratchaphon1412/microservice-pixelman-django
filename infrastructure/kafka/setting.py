from django.conf import settings

CONF_KAFKA = {
    'bootstrap.servers': settings.SECRETE_KEY_SERVICE['data']['data']['KAFKA_URI'],
    'auto.offset.reset': 'smallest',
    'group.id': settings.SECRETE_KEY_SERVICE['data']['data']['KAFKA_GROUP_ID'],
}
