FROM python

WORKDIR /app

COPY . /app

RUN pip install requests

EXPOSE 4321

CMD ["python", "server.py"]