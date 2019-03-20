FROM node:alpine as builder

WORKDIR /tmp/view

COPY ./my-app/package.json .

RUN npm install

COPY ./my-app/ .

RUN npm run build

FROM nginx

EXPOSE 3000

COPY --from=builder tmp/view/build/ /usr/share/nginx/html

COPY ./server/default.conf /etc/nginx/conf.d/default.conf
