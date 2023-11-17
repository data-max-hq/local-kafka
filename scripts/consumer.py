import logging

from kafka import KafkaConsumer

from scripts.config import TOPIC, BOOTSTRAP_SERVERS, CONSUMER_GROUP_ID

logging.basicConfig(level=logging.INFO)

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    group_id=CONSUMER_GROUP_ID
)
for msg in consumer:
    # logging.info(msg)
    logging.info(f"value: {msg.value}")
