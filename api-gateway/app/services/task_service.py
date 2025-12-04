import time 
from app.utils.id_generator import generate_task_id
from app.models.task_model import build_initial_task_data
from app.models.request_model import GenerateRequest
from app.cores.redis_db import save_task
from app.services.queue_service import publish_job
from app.services.storage_service import generate_signed_upload_url
def create_task(req: GenerateRequest):
    task_id = generate_task_id()
    task_type = "image"

    upload_url = generate_signed_upload_url(task_id)

    task_data = build_initial_task_data(
        task_id=task_id,
        task_prompt=req.prompt,
        task_model=req.model,
        input_url=upload_url,
        task_type=task_type
    )

    save_task(task_id, task_data)

    publish_job(task_data)

    return {
        "task_id": task_id,
        "upload_url": upload_url
    }
