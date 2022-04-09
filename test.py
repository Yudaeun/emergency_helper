import MySQLdb
import RPi.GPIO as GPIO
import sys
import time
import Adafruit_DHT
import pymysql

sensor = Adafruit_DHT.DHT11
conn = pymysql.connect(host="192.168.1.61",user="dev",passwd="pwd",db="TestDB")

GPIO.setmode(GPIO.BCM)
GPIO.setwarinings(False)

dht11_pin = 20 #온습도 센서 꽂는 핀 번호
BUTTON=4 # 스위치 꽂는 핀 번호

GPIO.setup(BUTTON,GPIO.IN)
count=0
try :
     with conn.cursor() as cur :
         # Connection으로부터 cursor 생성
        sql="insert into TempHue values(%s,%s,%s);"
        sql2 = "insert into Calltbl(call_state) values(%s);"     #Temptbl에 쿼리던지기
        while True :
            #온습도 센서 돌리고 값 db로 보냄
           humidity, temperature = Adafruit_DHT.read_retry(sensor, dht11_pin)
           if humidity is not None and temperature is not None:
              print('TEMP=%0.1f*C  Humidity=%0.1f'%(temperature, humidity))    #PI에 온습도 정보 띄움
              # 테이블에 데이터 입력
              cur.execute(sql,(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),temperature, humidity))
              conn.commit()
           else:
               print("Failed to get reading.")
           time.sleep(1)
           inputIO = GPIO.input(BUTTON)
           if inputIO == True and count == 0:
               print("first")
               state = "emergency"
               cur.execute(sql2, state)
               conn.commit()
           elif inputIO == True and count == 1:
               print("second")
               state = "delivery"
               cur.execute(sql2, state)
               conn.commit()
               count += 1
except KeyboardInterrupt :
       exit()
finally:
       conn.close()