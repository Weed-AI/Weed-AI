FROM node:10
RUN mkdir /code
WORKDIR /code
RUN mkdir /node_modules
COPY package.json package-lock.json /code/
RUN ["npm", "install"]

# replace this with your application's default port
EXPOSE 3000
# TODO: work out how to install in build and keep node_modules despite VOLUME...
CMD ["npm", "start"]


# for production:
# COPY . /code
