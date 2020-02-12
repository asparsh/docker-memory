# Start from the latest Long Term Support (LTS) Ubuntu version
FROM python:3.6-slim-buster

# Install pipenv
RUN apt-get update && apt-get install python3-pip -y && apt-get install curl -y && apt-get install python2.7 python-pip -y && apt-get -y install gcc

# Create the working directory
RUN set -ex && mkdir /repo
ADD requirements.txt /repo
WORKDIR /repo

# Install Python dependencies
RUN set -ex && pip3 install -r requirements.txt
# Copy only the relevant directories to the working directory
COPY . .

EXPOSE 80
# Run the web server
WORKDIR /repo
RUN ls
RUN cat /repo/start_server.sh
CMD sh /repo/start_server.sh
