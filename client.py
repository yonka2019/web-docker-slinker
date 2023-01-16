import requests

HOST = "127.0.0.1"
PORT = "4321"


def main():

    x = requests.post(f'http://{HOST}:{PORT}',
                      json={'url': 'https://yyes'})
    print(x.text)


if __name__ == '__main__':
    main()
