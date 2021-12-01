# For Production
FROM nginx:latest

# build node package
RUN apt update
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash
RUN apt install -y nodejs
RUN npm install -g yarn
RUN mkdir /code /code/public /code/src
COPY public /code/public
COPY src /code/src
COPY package.json yarn.lock /code/
RUN cd /code && find . && yarn install && yarn run build

# TODO: uninstall node

RUN mkdir /app
RUN cp -R /code/build/* /app/

COPY ./nginx/react/nginx.conf /etc/nginx/nginx.conf
