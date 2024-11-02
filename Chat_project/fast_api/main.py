from fastapi import FastAPI, HTTPException
import time
import os
import pandas as pd

app = FastAPI(title='Chatapp API')

JSON_PATH = '/data/processed_messages.jsonl'

@app.get('/')
async def root():
    return {'Distributed_systems': 'Chat_project'}

@app.get('/health')
def health_check():
    return {'message': 'Up and Running'}

@app.get('/messages/')
async def get_received_messages():
    try:
        time.sleep(1)
        if os.path.exists(JSON_PATH):
            data = pd.read_json(JSON_PATH, lines=True)
            dict_data = data.to_dict(orient='records')
        return dict_data
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=str(e))