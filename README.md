# Short-linker (Docker version)
URL shortener python server. The server have an endpoint that gets the long URL and returns a short URL.

In addition, this project deals with:

### SQLite 
Local database to save short-links in
### Redis 
Cache, to reduce the load. Removes the less recently used keys when the max memory limit (100 MB) is reached
### RabbitMQ
For every new URL, produces a message rabbitmq. Then, the consumer sends mail to server admin

## Usage example:
```
x = requests.post('http://127.0.0.1:4321',
json={'url': 'https://thatscool/veryveryverylongurl'})

# x = 127.0.0.1:4321/(hashed-shortlink-key)
```

- Support for browsing the short URLs. The server redirect the user to the real URL.


## Separated containers (works via Docker Compose):
- Python server container (**web-slink**)
- Database container (**db-slink**)
- Cache container *[redis]* (**cache-slink**)
- Message producer container *[rabbitmq]* (**msg-p-slink**)
- Message consumer container *[rabbitmq]* (**msg-c-slink**)

# Preview
![Screenshot preview](https://github.com/yonka2019/web-docker-slinker/blob/master/Screenshots/preview.png)
