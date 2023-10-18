from celery.result import AsyncResult


def get_task_info(task_id):
    """
    return task info for the given task_id
    """
    task_result = AsyncResult(task_id)
    result = {"task_id": task_id, "task_status": task_result.status, "task_result": task_result.result}
    return result


def get_celery_status(celery_app):
    inspector = celery_app.control.inspect()
    result = {
        "availability": inspector.ping(),
        "active_queues": inspector.active_queues(),
        "stats": inspector.stats(),
        "registered_tasks": inspector.registered(),
        "active_tasks": inspector.active(),
        "scheduled_tasks": inspector.scheduled(),
    }
    return result
