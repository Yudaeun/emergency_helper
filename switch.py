import RPi.GPIO as GPIO
import sys
import adafruit_dht
import pymysql
import mysql.connector;
from datetime import datetime
import time
import board

conn = mysql.connector.connect(host="localhost", user="root", passwd="", database="FOBO");
cur = conn.cursor(prepared=True);

button_pin = 21
#sensor=adafruit_DHT.DHT11
#dht11_pin = 4
count=0

#light_on = False

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(led_pin, GPIO.OUT)

max_time_end = time.time() + 3
# 시간 상한선을 3초로 두고 3초가 지나면 해당 count-state 값으로 고정 후 count 초기화

dhtDevice = adafruit_dht.DHT11(board.D4)


def button_callback(channel):
    global light_on    # Global 변수선언
    global count
    global max_time_end
    count+=1
    # count 값에 따라 버튼 제어 가능하게 함
    print("Button pushed!",count)
    if count==1:
        print("emergency")
        state="emergency"

        if time.time()>max_time_end:
            count=0
            max_time_end = time.time() + 3
    elif count==2:
        print("delivery")
        state="delivery"

        if time.time()>max_time_end:
            count=0
            max_time_end = time.time() + 3
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
    if count==0 :
        cur_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO call_time(time,house_num,definition,state) VALUES(%s,%s,%s,%s)"
        Values = [
            (cur_time, 1, state, 'waiting')
        ];
        cur.executemany(query, Values);
        conn.commit();


# Event 방식으로 핀의 Rising 신호를 감지하면 button_callback 함수를 실행
# 300ms 바운스타임을 설정하여 잘못된 신호를 방지
GPIO.add_event_detect(button_pin,GPIO.RISING,callback=button_callback, bouncetime=300)
while True:
    try:

        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )
        sql="insert into temptbl(time,house_num,temp,humidity) values(%s,%s,%s,%s);"
        cur.execute(sql,(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),'1',temperature_c,humidity))
        conn.commit();
    except RuntimeError as error:

        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
    time.sleep(10.0)

while 1: time.sleep(0.1)