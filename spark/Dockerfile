FROM bitnami/spark:3

WORKDIR /app

COPY spark/*.py /app/
COPY spark/requirements.txt /app/requirements.txt

USER root

RUN pip install -r requirements.txt

ENTRYPOINT /opt/bitnami/spark/bin/spark-submit --master $SPARK_MASTER_URL /app/main.py