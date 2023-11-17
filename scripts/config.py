BOOTSTRAP_SERVERS = "localhost:9092"
SR_TOPIC = "example_sr_topic"
TOPIC = "example_topic"
CONSUMER_GROUP_ID = "consumer_group"
SCHEMA_REGISTRY_URL = "http://localhost:8081"
SUBJECT = "test-subject"

SCHEMA = {
    "type": "record",
    "namespace": "com.kubertenes",
    "name": "AvroDeployment",
    "fields": [
        {
          "name": "begin",
          "type": {
            "type": "long",
            "logicalType": "timestamp-millis"
          },
          "doc": "Start time"
        },
        {"name": "image", "type": "string"},
        {"name": "replicas", "type": "int"},
        {"name": "port", "type": "int"},
    ],
}
