FROM python:3.7
WORKDIR /code
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ARG WEEDCOCO_VERSION=master
# Overridable so CI on a fork installs weedcoco from the fork's commit.
ARG WEEDCOCO_REPO=Weed-AI/Weed-AI
ADD "https://github.com/"$WEEDCOCO_REPO"/archive/"$WEEDCOCO_VERSION".zip" /tmp/weedcoco.zip
RUN pip install /tmp/weedcoco.zip
RUN pip install gunicorn
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY ./ .
