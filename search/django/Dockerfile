FROM python:3.7
WORKDIR /code
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ARG WEEDCOCO_VERSION=master
# Overridable so CI on a fork installs weedcoco from the fork's commit.
ARG WEEDCOCO_REPO=Weed-AI/Weed-AI
ADD "https://github.com/"$WEEDCOCO_REPO"/archive/"$WEEDCOCO_VERSION".zip" /tmp/weedcoco.zip
# bagit<1.9: 1.9.0 can't be built on Python 3.7 (needs setuptools-scm>=8).
# Pinned here too because the default weedcoco source (upstream master)
# doesn't carry the setup.py fix.
RUN pip install "bagit<1.9" /tmp/weedcoco.zip
RUN pip install gunicorn
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY ./ .
