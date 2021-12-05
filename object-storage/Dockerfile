FROM python:3.9.1

WORKDIR /app

COPY object-storage/main.py /app/main.py
COPY data /app/data
COPY object-storage/requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT python main.py