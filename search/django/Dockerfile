FROM python:3.7
WORKDIR /code
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ARG WEEDCOCO_VERSION=master
# Overridable so CI on a fork installs weedcoco from the fork's commit.
ARG WEEDCOCO_REPO=Weed-AI/Weed-AI
ADD "https://github.com/"$WEEDCOCO_REPO"/archive/"$WEEDCOCO_VERSION".zip" /tmp/weedcoco.zip
# Pins duplicated from setup.py because the default weedcoco source
# (upstream master) doesn't carry them:
#  - bagit<1.9: 1.9.0 can't be built on Python 3.7 (needs setuptools-scm>=8)
#  - ocfl-py<2: 2.x removed ocfl.Store, used by weedcoco.repo.deposit
RUN pip install "bagit<1.9" "ocfl-py<2" /tmp/weedcoco.zip
RUN pip install gunicorn
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY ./ .
