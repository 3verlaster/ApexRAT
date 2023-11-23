from urllib import request

url = 'http://api.ipify.org'

# Отправка GET-запроса
with request.urlopen(url) as response:
    ip_address = response.read().decode('utf-8')

print("Общедоступный IP-адрес:", ip_address)