import logging
import random
import uuid

from kafka import KafkaProducer

from scripts.config import BOOTSTRAP_SERVERS, SR_TOPIC, TOPIC
from scripts.schema_registry_client import encode_avro, SUBJECT, SCHEMA_REGISTRY_URL

logging.basicConfig(level=logging.INFO)


def producer_without_schema():
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    logging.info("producer")
    for i in range(100):
        key = uuid.uuid4().hex.encode('utf-8')
        value = f"some_message_bytes {i}".encode('utf-8')
        logging.info(f"message {i}")
        logging.info(f"key {key}")
        producer.send(
            TOPIC,
            key=key,
            value=value
        )
    producer.flush()


def producer_with_schema():
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    logging.info("producer")
    for i in range(100):
        random_int = random.randint(0, 1000)
        # Create record
        record = {
            "image": f"test_image_{random_int}",
            "replicas": 2,
            "port": 8080
        }

        # Encode avro record with schema
        encoded_record = encode_avro(
            record=record,
            subject=SUBJECT,
            url=SCHEMA_REGISTRY_URL
        )

        # Producer send
        key = uuid.uuid4().hex.encode("utf-8")
        producer.send(
            SR_TOPIC,
            value=encoded_record,
            key=key
        )
    producer.flush()


if __name__ == "__main__":
    producer_with_schema()
