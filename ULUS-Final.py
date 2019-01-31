import RPi.GPIO as GPIO
import time
import board
from busio import I2C
import adafruit_bme680

# Create library object using our Bus I2C port

i2c = I2C(board.SCL, board.SDA)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1010.80
GPIO.setup(25, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

anaparasutservo = GPIO.PWM(25,100)
suruklenmeparasutu = GPIO.PWM(22,100)
irtifa = int(0)
irtifason=int(0)
durum = int(1)
bitti = int(0)
open("ilk uçuş","w")
i=1
irtifaortalama=0

irtifa=bme680.altitude

while (i<10):
    irtifaortalama=irtifaortalama+irtifa
    print(irtifaortalama)
    time.sleep(1)
    i=i+1
    
a=irtifaortalama/9

print(a)

while True:
    
    print("\nTemperature: %0.1f C" % bme680.temperature)
    print("Gas: %d ohm" % bme680.gas)
    print("Humidity: %0.1f %%" % bme680.humidity)
    print("Pressure: %0.3f hPa" % bme680.pressure)
    print("Altitude = %0.2f meters" % bme680.altitude)
    sicaklik=bme680.temperature
    gas=bme680.gas
    nem=bme680.humidity
    basinc=bme680.pressure
    irtifa = bme680.altitude-a
    
    mesafe = open("ilk uçuş","a")
    with open ("ilk uçuş","a") as mesafe:
        mesafe.write("yükselik:"+str(irtifa)+"\n"+"sicaklik"+str(sicaklik)+"\n"+"gaz"+str(gas)+"\n"+"nem:"+str(nem)+"\n"+"basinc:"+str(basinc)+"\n"+"\n") 
    mesafe.close()
    
       
   #time.sleep(30) #yay ittiröme süresi
    
    
    suruklenmeparasutu.start(10)
    time.sleep(5)
    suruklenmeparasutu.stop()
    print("üst motor kitlendi")
    anaparasutservo.start(10)
    time.sleep(5)
    anaparasutservo.stop()
    print ("alt motor kitlendi")
    
    mesafe = open("ilk uçuş","a")
    with open ("ilk uçuş","a") as mesafe:
        mesafe.write("yükselik:"+str(irtifa)+"\n"+"sicaklik"+str(sicaklik)+"\n"+"gaz"+str(gas)+"\n"+"nem:"+str(nem)+"\n"+"basinc:"+str(basinc)+"\n"+"\n") 
    mesafe.close()
    
    if irtifa > 500: #yükselirken 70 irtifayı geçti
       durum = 2 
    #yukseklik = int(bme680.altitude)
    
    if durum == 2: #sürüklenme paraşüt durumu
       irtifson=bme680.altitude # 1 saniye sonra deger okundu
       if (irtifason<irtifa): #eger bir saniyeki degeri ile bir sanyie sonraki arasında büyüklük farkı varsa
          suruklenmeparasutu.start(10)
          time.sleep(2)
          suruklenmeparasutu.stop()
          print("sürüklenme paraşütü açıldı")
          durum = 3
    if durum == 3: #anapaşüt durumu kontorl edilecek.
       while (bitti == 0):
           irtifa = bme680.altitude
           print(irtifa)
           time.sleep(1)
           if (500 > irtifa):
              anaparasutservo.start(10)
              time.sleep(5)
              anaparasutservo.stop()
              print ("Ana Parasut acıldı")
              bitti = 1
        
        
        
        
        
        #GPIO.cleanup()
        
    #print("Altitude = %0.2f meters" % bme680.altitude)
        #print(yukseklik)
     






