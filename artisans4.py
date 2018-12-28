import ujson as json
import urequests as requests
import time
import dht
import machine
from machine import Pin
from machine import SPI
import ssd1306
from machine import I2C
#import machine
import onewire, ds18x20

index=0

i2c = I2C(-1, Pin(14), Pin(2))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

done_pin=Pin(13,Pin.OUT)
done_pin.value(0)

oled.fill(0)
oled.text("  Q U A H O G",0,0)
oled.text("Starting up ...",0,30)
oled.show()

time.sleep(3)



# CREDENTIALS

#WIFI_NET = 'TP-LINK_2.4GHz_9372CD'
WIFI_NET = 'Artisan\'s Asylum'
WIFI_PASSWORD = 'learn.make.teach'
#WIFI_NET = 'Don\'s iPhone'
#WIFI_PASSWORD = 'saladpunk'

base_url='https://wolfesneck.farmos.net/farm/sensor/listener/'
public_key='4ca9522aeef2d552d31754ba4e9c04b0'
private_key='682ac3fbc84e218d782e7ad355aeb624'

url = base_url+public_key+'?private_key='+private_key

headers = {'Content-type':'application/json', 'Accept':'application/json'}

# SENSOR SETUP
dat = machine.Pin(5)
d = dht.DHT22(machine.Pin(18))
ds = ds18x20.DS18X20(onewire.OneWire(dat))
roms = ds.scan()
print('found devices:', roms)



adc = machine.ADC(machine.Pin(35))


time.sleep(2)

def post_data(payload):
    try:
    	r = requests.post(url,data=json.dumps(payload),headers=headers)
    except Exception as e:
	print(e)
	#r.close()
	return "timeout"
    else:
	r.close()
	print('Status', r.status_code)
   	return r.status_code

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)	
    if not sta_if.isconnected():
        print('connecting to network...')
	sta_if.active(False)
        sta_if.active(True)
        sta_if.connect(WIFI_NET, WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

#dht22:

d.measure()
t=d.temperature()
h=d.humidity()

# onewire:

ds.convert_temp()
time.sleep_ms(750)

rom=roms[0]

t1=ds.read_temp(rom)

# adc

adc_val=adc.read()

#payload ={"temp": t,"humidity":h,"adc_val":adc_val}


payload ={"temp_ambient": t,"humidity_ambient":h,"temp_onewire":t1,"adc_val":adc_val}

print(payload)

oled.fill(0)
oled.text("  Q U A H O G",0,0)
oled.text("t="+str(t)+";h="+str(h),0,20)
oled.text("tp="+str(t1)+";a="+str(adc_val),0,30)

oled.show()

do_connect()

oled.text("Posting...",0,40)
oled.show()

status=post_data(payload)

oled.text(str(status),0,50)
oled.show()


oled.show()

time.sleep(1)

done_pin.value(1)

index+=1

time.sleep(5)


