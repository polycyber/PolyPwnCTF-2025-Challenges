FROM openresty/openresty:latest

RUN apt-get update && apt-get -y install \
    apache2-utils nginx-extras

COPY ./dist /usr/share/nginx/html

COPY ./nginx.conf /usr/local/openresty/nginx/conf/nginx.conf

EXPOSE 80

CMD ["openresty", "-g", "daemon off;"]
