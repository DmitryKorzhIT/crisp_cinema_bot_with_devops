#docker build --build-arg app_bot_token=your_telegram_bot_token --build-arg kinopoisk_api_key=your_kinopoisk_api_key -t app:1 .    <--- command to make a docker build. Use it!


FROM python:3.8

# set environment variables
ARG app_bot_token
ARG kinopoisk_api_key
ENV APP_BOT_TOKEN=$app_bot_token
ENV KINOPOISK_API_KEY=$kinopoisk_api_key

# show environment variables while docker build
RUN env | grep "APP_"
RUN env | grep "KINOPOISK_API_KEY"

# install python and pip
# RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python \
# && python3 -m ensurepip \
# && pip3 install --no-cache --upgrade pip setuptools

# install python and pip
# RUN apk add --update py-pip \
# && pip install --upgrade pip

# copy project
COPY . /usr/src/app/

# set work directory
WORKDIR /usr/src/app/

# install dependencies
RUN pip install -r ./requirements.txt

# port for postgresql
# ENV LISTEN_PORT 5432
# EXPOSE 5432

# run app
CMD ["python", "main.py"]


