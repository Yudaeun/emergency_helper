import mysql.connector;
import RPi.GPIO as GPIO
import sys
import time
import Adafruit_DHT
import pymysql
from datetime import datetime

#sensor = Adafruit_DHT.DHT11
conn = mysql.connector.connect(host="localhost", user="root", passwd="", database="FOBO");

BUTTON=21 # 스위치 꽂는 핀 번호
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#dht11_pin = 4 #온습도 센서 꽂는 핀 번호


GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
count=0


try :
     with conn.cursor() as cur :
        print("1")
         # Connection으로부터 cursor 생성
        #sql="insert into temptbl values(%s,%s,%s);"
        sql2 = "insert into call_time(state) values(%s);"     #Temptbl에 쿼리던지기
        print("2");
        while True :
            #온습도 센서 돌리고 값 db로 보냄
           '''humidity, temperature = Adafruit_DHT.read_retry(sensor, dht11_pin)
           if humidity is not None and temperature is not None:
              print('TEMP=%0.1f*C  Humidity=%0.1f'%(temperature, humidity))    #PI에 온습도 정보 띄움
              # 테이블에 데이터 입력
              cur.execute(sql,(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),temperature, humidity))
              conn.commit()
           else:
               print("Failed to get reading.")
           time.sleep(1)'''
            # 스위치 제어하고 값 db로 보냄
           inputIO = GPIO.input(BUTTON)
           print("Button pushed!",count)
           if inputIO == True and count == 1:
               print("first")
               state = "emergency"
               cur.execute(sql2, state)
               count+=1
               conn.commit()
           elif inputIO == True and count == 2:
               print("second")
               state = "delivery"
               cur.execute(sql2, state)
               conn.commit()
               count += 1
           elif inputIO == True and count==3:
               print("third")
               state="consulting"
               cur.execute(sql2,state)
               conn.commit()
               count=0
           time.sleep(3)
except KeyboardInterrupt :
       exit()
finally:
       conn.close()