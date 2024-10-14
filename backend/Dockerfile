FROM python:slim-bookworm

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt update
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
