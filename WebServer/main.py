from microdot import Microdot
import microdot
import time
import json
import mm_wlan
import machine
import onewire
import ds18x20

### set up the temp sensor ###
# the device is on GPIO6
pin = machine.Pin(6)

# create the sensor object using a onewire object
ds = ds18x20.DS18X20(onewire.OneWire(pin))

# scan for devices on the bus (take the first since we don't have multiple)
device = ds.scan()[0]

### set up wifi ###
ssid = 'enter ssid here'
password = 'enter password here'

# pass credentials to library. library is configured to request a static IP, adjust for your local network
mm_wlan.connect_to_network(ssid, password)

### create the web server ###
app = Microdot()  

# handle all "GET" requests by calling the "sendData()" function
@app.get('/')
def sendData(request):
    # prep an array for temperatures
    temps = []
    # loop 10 times and store the temperature values
    for i in range(10):
        # send the signal to our sensor that shows we want to receive temperatures
        ds.convert_temp()
        # wait for the sensor to comply
        time.sleep_ms(750)
        # read in the value
        temps.append(ds.read_temp(device))
    #average the ~10 seconds of data
    avgTemp = sum(temps) / len(temps)
    # store and send the data as json. the key used here will be used by the client to sample out the desired data
    data = {"Temp": avgTemp}
    return data

# tell the webserver to use port 80
app.run(port=80)