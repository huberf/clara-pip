import requests as r
import json

rootUrl = 'http://localhost:3000/'

while True:
    text = input('Message> ')
    response = r.post(rootUrl + 'api/v1/io/blocking/guest', { 'input': text })
    print(json.loads(response.text.replace('\n', '\\n'))['message'])
