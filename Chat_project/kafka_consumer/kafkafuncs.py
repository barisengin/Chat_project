import json
from kafka import KafkaConsumer, KafkaProducer
import sqlite3
import json
from datetime import datetime

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
FASTAPI_CONSUMER_GROUP = "kafka-consume"

def kafka_send(message, topic_to_send):
    producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, api_version=(0,11,5), value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send(topic_to_send, value=message)

def process_message(message):
    save_message(message['nick'], message['content'])
    return message

def kafka_consumer(topic_to_consume):
    consumer = KafkaConsumer(topic_to_consume, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, api_version=(0,11,5), auto_offset_reset='earliest', group_id=FASTAPI_CONSUMER_GROUP,
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    
    for message in consumer:
        data =  message.value
        processed_data = process_message(data)
        print(str(processed_data) + 'consume', flush=True)
        kafka_send(processed_data, 'processed_topic')


def initialize_database():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                      (timestamp TEXT, nickname TEXT, message TEXT)
''')
    conn.commit()
    conn.close()

def save_message(nickname, message):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO messages VALUES (?, ?, ?)", (timestamp, nickname, message))
    conn.commit()
    conn.close()

def main():
    kafka_consumer('to_process')

