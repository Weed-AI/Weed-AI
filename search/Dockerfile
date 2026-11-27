# For Production
# Multi-stage build: compile the React app on a Node image, then serve it from
# a pinned, patched nginx. (The old single-stage build installed Node 12 from
# the deprecated NodeSource script on top of nginx:latest, which is fragile and
# left Node in the runtime image.)
FROM node:12-bullseye AS build
WORKDIR /code
COPY package.json yarn.lock /code/
RUN yarn install
COPY public /code/public
COPY src /code/src
RUN yarn run build

FROM nginx:1.30
RUN mkdir /app
COPY --from=build /code/build/ /app/
COPY ./nginx/react/nginx.conf /etc/nginx/nginx.conf
