# FROM node:10
# RUN mkdir /code
# WORKDIR /code
# COPY package.json yarn.lock /code/
# RUN ["yarn", "install"]
# EXPOSE 3000
# CMD ["yarn", "start"]

# For Production
FROM nginx:latest

# build node package
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN ["apt", "install", "yarn"]
COPY . /tmp/code
RUN ["cd", "/tmp/code", "&&", "yarn", "install", "&&", "yarn", "run", "build"]

# TODO: uninstall node

RUN mkdir /app

COPY ./nginx/react/nginx.conf /etc/nginx/nginx.conf
