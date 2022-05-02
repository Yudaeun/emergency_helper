import RPi.GPIO as GPIO
import sys
import Adafruit_DHT
import pymysql
import mysql.connector;
from datetime import datetime
import time

conn = mysql.connector.connect(host="localhost", user="root", passwd="", database="FOBO");
cur = conn.cursor(prepared=True);

button_pin = 21
#led_pin = 14
count=0

#light_on = False

GPIO.setwarnings(False)
# GPIO핀의 번호 모드 설정
GPIO.setmode(GPIO.BCM)
# 버튼 핀의 IN/OUT 설정 , PULL DOWN 설정
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(led_pin, GPIO.OUT)

def button_callback(channel):
    global light_on    # Global 변수선언
    global count
    count+=1

    # count 값에 따라 버튼 제어 가능하게 함
    print("Button pushed!",count)
    if count==1:
        print("emergency")
        state="emergency"
    elif count==2:
        print("delivery")
        state="delivery"
    elif count==3:
        print("consulting")
        state="consulting"
        count=0
    #if light_on == False:  # LED 불이 꺼져있을때
        #GPIO.output(led_pin,1)   # LED ON
        #print("LED ON!")
    #else:                                # LED 불이 져있을때
        #GPIO.output(led_pin,0)  # LED OFF
        #print("LED OFF!")
    #light_on = not light_on  # False <=> True
    d = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    query = "INSERT INTO test(state,test1,test2) VALUES(%s,%s,%s)"
    Values = [
        (d,state,1)
    ];
    cur.executemany(query, Values);
    conn.commit();


# Event 방식으로 핀의 Rising 신호를 감지하면 button_callback 함수를 실행
# 300ms 바운스타임을 설정하여 잘못된 신호를 방지
GPIO.add_event_detect(button_pin,GPIO.RISING,callback=button_callback, bouncetime=300)

while 1: time.sleep(0.1)