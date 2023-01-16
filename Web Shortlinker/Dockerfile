FROM python

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# for web connection [server.py]
EXPOSE 4321

# for sending mail (via SSL connection) [consumer.py]
EXPOSE 465

# can't run server.py and consumer.py there, if we will do two CMD command to run the both files, docker will take the
# last one, so to deal with it, I created bash script which will be executed and run the both python scripts

# consumer.py + server.py
CMD ["./start.sh"]