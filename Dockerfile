FROM python:3.8.2-alpine


RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

COPY nginx.conf /etc/nginx/nginx.conf

RUN ln -s /var/www /www

ENV NGINX_VERSION 1.12.2-1~stretch
ENV NJS_VERSION   1.12.2.0.1.14-1~stretch


WORKDIR /www

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt


RUN pip install awscli

COPY . .

EXPOSE 80

CMD ["bash", "startup.sh"]
