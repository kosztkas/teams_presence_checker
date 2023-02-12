FROM python:3.8-slim-bullseye
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --default-timeout=1000 -r requirements.txt
COPY main.py config.json ./
ENTRYPOINT [ "python3","-u", "main.py", "config.json" ]
