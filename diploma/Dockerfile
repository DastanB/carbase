
FROM python:3.7.7-alpine

# set work directory
WORKDIR /usr/src/diploma

RUN echo http://repository.fit.cvut.cz/mirrors/alpine/v3.11/main > /etc/apk/repositories; \
    echo http://repository.fit.cvut.cz/mirrors/alpine/v3.11/community >> /etc/apk/repositories
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk add zlib-dev jpeg-dev gcc musl-dev \
    && pip install Pillow 

# install dependencies
RUN pip install --upgrade pip
COPY ./req.txt /usr/src/diploma/req.txt
RUN pip install -r req.txt
# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/diploma/entrypoint.sh

# copy project
COPY . /usr/src/diploma/

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["/usr/src/diploma/entrypoint.sh"]