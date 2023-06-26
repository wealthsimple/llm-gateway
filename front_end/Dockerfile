FROM node:16.13.1
LABEL maintainer="Data Science & Engineering @ Wealthsimple <data@wealthsimple.com>"

WORKDIR /usr/src/app
COPY package.json yarn.lock .eslintrc.json tsconfig.json ./
RUN yarn install
