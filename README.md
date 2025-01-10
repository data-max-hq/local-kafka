# Create and Test a local Kafka Setup

## Start the docker compose

```commandline
docker compose up -d
```

## Included components

* zookeeper - needed to run Kafka brokers
* broker - the Kafka broker
* akhq - Kafka UI
* schema_registry - Schema Registry for Kafka
* connect - Kafka Connect

## Remove everything

```commandline
docker compose down -v
```

## Included Scripts

* `scripts/consumer.py` - simple script to read a message from a Kafka topic
* `scripts/producer.py` - simple script to push a message to a Kafka topic
* `scripts/schema_registry_client.py` - simple script to create a subject in
Schema Registry and to read and write messages with schema
* `scripts/topic.py` - simple script to create a topic in Kafka

## References

* https://github.com/confluentinc/cp-all-in-one/blob/7.3.0-post/cp-all-in-one-kraft/docker-compose.yml
* https://github.com/tchiotludo/akhq/blob/dev/docker-compose.yml
* https://kafka-python.readthedocs.io/en/master/usage.html
* https://www.confluent.io/blog/kafka-listeners-explained/

Made with ❤️ by [datamax.ai](https://www.datamax.ai/).
