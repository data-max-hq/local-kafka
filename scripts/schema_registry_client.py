import datetime
import logging
import os
import random
import uuid
from typing import Union, Optional

from kafka import KafkaProducer, KafkaConsumer
from schema_registry.client import SchemaRegistryClient, schema
from schema_registry.serializers import AvroMessageSerializer

from scripts.config import SCHEMA_REGISTRY_URL, SCHEMA, SUBJECT, BOOTSTRAP_SERVERS, CONSUMER_GROUP_ID, SR_TOPIC

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def register_avro_schema():
    client = SchemaRegistryClient(url=SCHEMA_REGISTRY_URL)

    avro_schema = schema.AvroSchema(SCHEMA)

    schema_id = client.register(SUBJECT, avro_schema)
    logger.info(f"Schema registered with id: {schema_id}")
    return schema_id


def encode_avro(record: any, subject: str, url: Union[str, dict]) -> bytes:
    """Encode record to avro

    Args:
        record: Record to encode
        subject: Schema subject
        url: Schema registry url

    Returns:
        Encoded record
    """
    client = SchemaRegistryClient(url=url)
    avro_message_serializer = AvroMessageSerializer(client)
    avro_schema = client.get_schema(subject=subject, version="latest")
    encoded_record = avro_message_serializer.encode_record_with_schema(
        subject=subject, schema=avro_schema.schema, record=record
    )
    return encoded_record


def decode_avro(message: Optional[bytes], url: Union[str, dict]) -> any:
    """Decode avro message

    Args:
        message: Message to decode
        url: Schema registry url

    Returns:
        Decoded message
    """
    client = SchemaRegistryClient(url=url)
    return AvroMessageSerializer(client).decode_message(message=message)


def push_message_with_schema():
    # Create producer
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    random_int = random.randint(0, 1000)
    a_datetime = datetime.datetime(2019, 10, 12, 17, 57, 42)

    # Create record
    record = {
        "begin": a_datetime,
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
    logger.info("Sending message.")
    producer.send(
        SR_TOPIC,
        value=encoded_record,
        key=key
    )
    producer.flush()
    logger.info("Finished.")


def read_message_with_schema():
    # create consumer
    # https://gitlab.com/dataalliance/products/onair-common/product/onair-common-lib/-/blob/dev/onair_common_lib/src/connect_kafka.py#L89
    consumer = KafkaConsumer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id=CONSUMER_GROUP_ID,
        auto_offset_reset="earliest",
    )
    # read message
    consumer.subscribe(topics=[SR_TOPIC])
    while True:
        try:
            # Read messages from the Kafka consumer and pass them to a thread in order to process them
            messages = consumer.poll()
            # Record the creation time of each thread for performance tracking
            if messages:
                for tp, records in messages.items():
                    for record in records:
                        # decode message
                        payload = decode_avro(message=record.value, url=SCHEMA_REGISTRY_URL)
                        key = record.key
                        key_decoded = key.decode("utf-8")
                        logger.info(f"key_decoded: {key_decoded}")
                        logger.info(f"payload: {payload}")

        except Exception as e:
            logger.error(f"Worker {os.getpid()} terminated with error {e}")


if __name__ == "__main__":
    # register_avro_schema()
    push_message_with_schema()
    read_message_with_schema()
