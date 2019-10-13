# our base image
FROM python:3-alpine

#RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app

RUN apk add build-base linux-headers

RUN pip install -r requirements.txt

# specify the port number the container should expose
EXPOSE 8888

# run the application
CMD ["python", "./server.py", "0.0.0.0", "8888"]
