import streamlit as st
from streamlit_server_state import *
import json
import time
import os
from kafka import KafkaProducer
import pandas as pd

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'], api_version=(0,11,5),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

JSON_PATH = '/data/processed_messages.jsonl'

nickname = st.text_input("Nick name")
if not nickname:
    st.stop()

def send_message():
    new_message_text = st.session_state["mess_input"]
    if not new_message_text:
        return

    new_message_packet = {
        "role": "user",
        "nick": nickname,
        "content": new_message_text,
    }
    
    if(new_message_packet["content"] != None):
        producer.send('to_process', value=new_message_packet)
    
    processed_message_packet = {}
    
    time.sleep(1)
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'r') as file:
            last_line = file.readlines()[-1]
            data = pd.read_json(last_line, lines=True)
            processed_message_packet = data.to_dict(orient='records')

    with server_state_lock.chat_messages:
        server_state.chat_messages = server_state.chat_messages + [processed_message_packet]

def delete_history():
    server_state.chat_messages = []

st.button("Clear chat history", key="del_his", on_click=delete_history)

st.chat_input(placeholder='Enter a message.', key="mess_input", on_submit=send_message)

with server_state_lock.chat_messages:
    if "chat_messages" not in server_state:
        server_state.chat_messages = []

for message in server_state.chat_messages:
    with st.chat_message(message[0]["role"]):
        st.markdown(message[0]["nick"] + ": " + message[0]["content"])



