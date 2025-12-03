import time

def build_initial_task_data(task_id, prompt, model, input_url):
    return {
        "task_id": task_id,
        "status": "PENDING",

        "prompt": prompt,
        "model": model,
        "model_version": None,

        "input_url": input_url, 
        "output_url": None, 

        "error_message": None,

        "created_at": int(time.time()), 
        "updated_at": int(time.time()),

        "worker_version": None,
        "progress": 0
    }