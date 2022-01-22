#docker build --build-arg app_bot_token=your_telegram_bot_token -t app:1 .    <--- command to make a docker build

FROM python:3.8

ARG app_bot_token
ENV APP_BOT_TOKEN=$app_bot_token

# show environment variables while docker build
RUN env | grep "APP_"

# set work directory
WORKDIR /usr/src/app/

# copy project
COPY . /usr/src/app/

# install dependencies
RUN pip install -r ./requirements.txt

# run app
CMD ["python", "main.py"]


