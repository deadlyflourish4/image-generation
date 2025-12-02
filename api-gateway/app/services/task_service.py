import time 
from app.utils.id_generator import generate_task_id

def create_task(req):
    task_id = generate_task_id()

    upload_url = generate_signed_upload_url(task_id)

    task_data = build_initial_task_data(
        task_id=task_id,
        task_prompt=req.prompt,
        task_model=req.model,
        input_url=upload_url
    )

    save_task(task_id, task_data)

    publish_job(task_data)

    return {
        "task_id": task_id,
        "upload_url": upload_url
    }
