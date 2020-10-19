FROM nginx:latest
RUN mkdir /app
COPY --from=reactbuild /code/build /app
COPY ./react_nginx/nginx.conf /etc/nginx/nginx.conf