FROM python:3.7.3

ARG DIR=/var/auto-relpy

RUN mkdir ${DIR} \
        &&apt-get update \
        &&apt-get -y install freetds-dev \
        &&apt-get -y install unixodbc-dev

COPY main.py ${DIR}/
COPY mongo.py ${DIR}/
COPY utils.py ${DIR}/
COPY config.ini ${DIR}/
COPY requirements.txt ${DIR}/

RUN pip install -r ${DIR}/requirements.txt -i https://pypi.douban.com/simple

WORKDIR ${DIR}

CMD ["python", "main.py"]