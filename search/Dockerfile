FROM node:10
RUN mkdir /code
WORKDIR /code
COPY package.json yarn.lock /code/
RUN ["yarn", "install"]

# replace this with your application's default port
EXPOSE 3000
# TODO: work out how to install in build and keep node_modules despite VOLUME...
CMD ["sudo", "yarn", "start"]


# for production:
# COPY . /code
