import json
import os
from kafka import KafkaConsumer

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_CONSUMER_GROUP = "streamlit-consume"

def kafka_consume_json(topic_to_consume):
    consumer = KafkaConsumer(topic_to_consume, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, api_version=(0,11,5), auto_offset_reset='latest', group_id=KAFKA_CONSUMER_GROUP, 
                                value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    
    os.makedirs('/data', exist_ok=True)

    for message in consumer:
        print(str(message.value) + 'consume_json', flush=True)
        with open('/data/processed_messages.jsonl', 'a') as file:
            file.write(json.dumps(message.value) + '\n')

def main():
    kafka_consume_json('processed_topic')