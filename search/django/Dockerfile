FROM python:3.7
WORKDIR /code
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY ./ .