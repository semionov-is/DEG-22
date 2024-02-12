FROM continuumio/miniconda3:latest
WORKDIR /app
COPY 1.sh /app/1.sh
RUN chmod +x /app/1.sh
RUN conda install -y mlflow boto3 pymysql
CMD  ["/bin/bash", "/app/1.sh"]
