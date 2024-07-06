FROM python:3.11.4-slim
WORKDIR /app
COPY requirements.txt requirements.txt
ENV TZ=Europe/Moscow
RUN apt-get update & pip3 install --upgrade setuptools & pip3 install  -r requirements.txt && apt-get install --no-install-recommends -y tzdata\
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY . /app


CMD ["python", "main.py"]