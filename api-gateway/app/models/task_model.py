import time

def build_initial_task_data(task_id, prompt, model, task_type, input_url=None):
    return {
        "task_id": task_id,
        "task_type": task_type,
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