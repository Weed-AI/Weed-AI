FROM node:10
RUN mkdir /code
WORKDIR /code
RUN curl -o- -L https://yarnpkg.com/install.sh | bash
COPY package.json yarn.lock /code/
RUN yarn install

# replace this with your application's default port
EXPOSE 3000
CMD ["yarn", "start"]


# for production:
# COPY . /code
