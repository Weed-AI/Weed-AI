# FROM node:10
# RUN mkdir /code
# WORKDIR /code
# COPY package.json yarn.lock /code/
# RUN ["yarn", "install"]
# COPY . /code
# RUN ["yarn", "run", "build"]

# replace this with your application's default port
# EXPOSE 3000
# TODO: work out how to install in build and keep node_modules despite VOLUME...
# CMD ["yarn", "start"]

# for production:
# COPY . /code

FROM nginx:latest
RUN mkdir /app
COPY ./build /app
COPY ./react_nginx/nginx.conf /etc/nginx/nginx.conf