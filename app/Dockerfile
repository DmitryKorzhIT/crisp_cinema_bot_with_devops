#docker build --build-arg app_bot_token=your_telegram_bot_token --build-arg kinopoisk_api_key=your_kinopoisk_api_key -t app:1 .    <--- command to make a docker build. Use it!
#docker run --env TOKEN=<...> bot    <--- this is my own command. You don't have to use it!


FROM python:3.8

# set environment variables
ARG app_bot_token
ARG kinopoisk_api_key
ENV APP_BOT_TOKEN=$app_bot_token
ENV KINOPOISK_API_KEY=$kinopoisk_api_key

# show environment variables while docker build
RUN env | grep "APP_"
RUN env | grep "KINOPOISK_API_KEY"

# set work directory
WORKDIR /usr/src/app/

# copy project
COPY . /usr/src/app/

# install dependencies
RUN pip install -r ./requirements.txt

# run app
CMD ["python", "main.py"]


