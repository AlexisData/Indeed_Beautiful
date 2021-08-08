import requests

r = requests.get('https://lumtest.com/myip.json')

print(r.text)