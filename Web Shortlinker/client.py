import requests as requests

x = requests.post('http://127.0.0.1:4321',
                  json={'url': 'https://long.pasten.com/veryveafafryverylongurl'})
print(x.text)
