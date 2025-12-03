import redis
from app.cores.config import *
import json

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)

def save_task(task_id: str, task_data: dict, ttl: int = 86400):
    key = f"task:{task_id}"
    redis_client.set(key, json.dumps(task_data), ex=ttl)
    return True

def get_task(task_id):
    key = f"task:{task_id}"
    data = redis_client.get(key)

    if data is None:
        return None
    
    return json.loads(data)