import ujson as json
import urequests as requests
import time
import dht
import machine
from machine import Pin
import ssd1306
from machine import I2C
import onewire, ds18x20

t=3.
h=4.
adc_val=4.

# SENSOR SETUP
dat = machine.Pin(5)
d = dht.DHT22(machine.Pin(18))
ds = ds18x20.DS18X20(onewire.OneWire(dat))
roms = ds.scan()
print('found devices:', roms)

ds.convert_temp()

payload ={"temp_ambient": t,"humidity_ambient":h,"adc_val":adc_val}

index=0
for rom in roms:
    label="temp_probe_"+str(index)
    time.sleep(1)
    t_onewire=ds.read_temp(rom)
    payload[label]=t_onewire
    index=index+1
    
    
print(payload)

