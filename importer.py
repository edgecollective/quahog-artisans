import ujson as jsonimport urequests as requestsimport timeimport dhtimport machinefrom machine import Pinfrom machine import SPIimport ssd1306from machine import I2Cimport sdcard, osimport sysindex=0i2c = I2C(-1, Pin(14), Pin(2))oled = ssd1306.SSD1306_I2C(128, 64, i2c)done_pin=Pin(13,Pin.OUT)done_pin.value(0)oled.fill(0)oled.text("  Q U A H O G",0,0)oled.text("Starting up ...",0,30)oled.show()	try:    sck=Pin(16)    mosi=Pin(4)    miso=Pin(17)    cs = Pin(15, Pin.OUT)    spi2=SPI(2,baudrate=5000000,sck=sck,mosi=mosi,miso=miso)    sd = sdcard.SDCard(spi2, cs)    vfs=os.VfsFat(sd)    os.mount(vfs,"/sd")    sys.path.append("/sd")    print(sys.path)    import farmos_dth22_onewireexcept Exception as e:print(e)oled.text(str(e),0,40)oled.show()