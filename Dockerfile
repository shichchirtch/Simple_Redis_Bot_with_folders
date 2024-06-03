FROM python:3.11.7

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

WORKDIR /app

COPY ./app /app/

CMD ["python", "/app/main.py"]