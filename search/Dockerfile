# FROM node:10
# RUN mkdir /code
# WORKDIR /code
# COPY package.json yarn.lock /code/
# RUN ["yarn", "install"]
# EXPOSE 3000
# CMD ["yarn", "start"]

# For Production
FROM nginx:latest
RUN mkdir /app
COPY ./build /app
COPY ./nginx/react/nginx.conf /etc/nginx/nginx.conf