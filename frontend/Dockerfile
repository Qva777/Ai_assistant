FROM node:18-alpine

WORKDIR /app

# delete node modules
RUN rm -fr node_modules

# install node modules
COPY package.json /app/package.json

RUN npm install

COPY . .

CMD ["/bin/sh", "./start_dev.sh"]