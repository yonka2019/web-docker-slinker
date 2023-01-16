FROM python

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# for web connection
EXPOSE 4321

CMD ["python", "server.py"]
