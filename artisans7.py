import ujson as jsonimport urequests as requestsimport timeimport dhtimport machinefrom machine import Pinimport ssd1306from machine import I2Cimport onewire, ds18x20index=0f=open('/sd/wifi_config.csv')c=f.read()essid=c.split(',')[0].strip()psswd=c.split(',')[1].strip()f.close()f=open('/sd/farmos_config.csv')c=f.read()public_key=c.split(',')[0].strip()private_key=c.split(',')[1].strip()f.close()base_url='https://wolfesneck.farmos.net/farm/sensor/listener/'url = base_url+public_key+'?private_key='+private_keyheaders = {'Content-type':'application/json', 'Accept':'application/json'}print(essid,psswd)print(public_key,private_key)# SENSOR SETUPdat = machine.Pin(5)d = dht.DHT22(machine.Pin(18))ds = ds18x20.DS18X20(onewire.OneWire(dat))roms = ds.scan()print('found devices:', roms)adc = machine.ADC(machine.Pin(35))time.sleep(2)def post_data(payload):    try:    	r = requests.post(url,data=json.dumps(payload),headers=headers)    except Exception as e:	print(e)	#r.close()	return "timeout"    else:	r.close()	print('Status', r.status_code)   	return r.status_codedef do_connect(essid,psswd):    import network    sta_if = network.WLAN(network.STA_IF)    if not sta_if.isconnected():        print('connecting to network...')        sta_if.active(False)        sta_if.active(True)        sta_if.connect(essid, psswd)        while not sta_if.isconnected():            pass    print('network config:', sta_if.ifconfig())#dht22:d.measure()t=d.temperature()h=d.humidity()# onewire:ds.convert_temp()time.sleep_ms(750)rom=roms[0]t1=ds.read_temp(rom)# adcadc_val=adc.read()#payload ={"temp": t,"humidity":h,"adc_val":adc_val}payload ={"temp_ambient": t,"humidity_ambient":h,"temp_onewire":t1,"adc_val":adc_val}print(payload)oled.fill(0)oled.text("  Q U A H O G",0,0)oled.text("t="+str(t)+";h="+str(h),0,20)oled.text("tp="+str(t1)+";a="+str(adc_val),0,30)oled.show()do_connect(essid,psswd)oled.text("Posting...",0,40)oled.show()status=post_data(payload)oled.text(str(status),0,50)oled.show()oled.show()time.sleep(1)done_pin.value(1)index+=1time.sleep(5)