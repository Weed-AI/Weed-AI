FROM python:3.7
WORKDIR /code
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ARG WEEDCOCO_VERSION=master
ADD "http://github.com/Weed-AI/Weed-AI/archive/"$WEEDCOCO_VERSION".zip" /tmp/weedcoco.zip
RUN pip install /tmp/weedcoco.zip
RUN pip install gunicorn
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY ./ .
