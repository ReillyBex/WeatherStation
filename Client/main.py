import urequests
import mm_wlan
import time
import json

# get connected to WiFi
ssid = 'enter ssid here'
password = 'enter password here'
mm_wlan.connect_to_network(ssid, password)

# create the requests object and get the json response
response = urequests.request(method='GET', url='the url of your webserver')
response = json.loads(response.text)
# code the key into the webserver so that you can pull it out here. I chose "Temp"
print(response["Temp"])
