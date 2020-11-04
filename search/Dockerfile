# For Production
FROM nginx:latest

# build node package
RUN apt update
RUN apt install -y npm
RUN npm install -g yarn
#RUN apt install -y gnupg2
#RUN apt remove cmdtest  # see https://stackoverflow.com/questions/46013544/yarn-install-command-error-no-such-file-or-directory-install
#RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
#RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
#RUN ["apt", "install", "-y", "yarn"]
RUN mkdir /code /code/public /code/src
COPY public /code/public
COPY src /code/src
COPY package.json yarn.lock /code/
RUN cd /code && find . && yarn install && yarn run build

# TODO: uninstall node

RUN mkdir /app
RUN cp -R /code/build/* /app/

COPY ./nginx/react/nginx.conf /etc/nginx/nginx.conf
