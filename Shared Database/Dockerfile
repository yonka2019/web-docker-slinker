FROM ubuntu

RUN apt-get update && apt-get install -y sqlite3
# to convert file from win version to unix version to make them version
# https://askubuntu.com/questions/304999/not-able-to-execute-a-sh-file-bin-bashm-bad-interpreters
RUN apt-get install -y dos2unix

WORKDIR /app

COPY . /app

