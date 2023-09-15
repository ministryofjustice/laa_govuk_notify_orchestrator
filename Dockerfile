FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./notify_orchestrator /code/notify_orchestrator

CMD ["uvicorn", "notify_orchestrator.main:app", "--host", "0.0.0.0", "--port", "2500"]