import esp
import machine
import network
import dht
from bme280 import BME280
import ujson as json
from utime import sleep

from umqtt.simple import MQTTClient

# https://github.com/micropython/micropython-lib/blob/master/umqtt.simple/example_pub_button.py

MQTT_SERVER = "10.254.0.1"
SENSOR_NAME = "afra-t1"
DHT_TOPIC = "afra-t1"
BME_TOPIC = "afra-t2"


GPIO_DHT = 26
GPIO_SCL = 22
GPIO_SDA = 21

# how often it should be measured. Every x seconds
MEASURE_TIME = 5 * 60

def connect_mqtt(server, client_id):
    client = MQTTClient(client_id, server)
    client.connect()
    print("Connected to mqtt")
    return client

def connect_wifi(timeout):
    """ timeout in sec """
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('discord', 'baraustrinken')

    for _ in range(timeout):
        # wait x sec
        if sta_if.isconnected():
            print("Connected to wifi")
            break
        sleep(1)
    return sta_if

def read_dht():
    sensor = dht.DHT22(machine.Pin(GPIO_DHT))
    sensor.measure()
    result = {
        "name": DHT_TOPIC,
        "data": {
            "temp": sensor.temperature(),
            "humidity": sensor.humidity(),
            },
        "measuretime": MEASURE_TIME,
        }
    return json.dumps(result)

def format_bme280(bme):
    temp, pressure, _hum = bme.read_compensated_data()

    temp = temp / 100
    hpa = (pressure // 256) / 100

    result = {
        "name": BME_TOPIC,
        "data": {
            "temp": temp,
            "pressure": hpa
            },
        "measuretime": 60 * 5,
        }
    return json.dumps(result)

def deepsleep():
    print("Goint to deepsleep in 10 sec")
    sleep(10)
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # set RTC.ALARM0 to fire after 10 seconds (waking the device)
    rtc.alarm(rtc.ALARM0, (MEASURE_TIME - 10) * 1000)

    machine.deepsleep()

def main():
    try:
        while True:
            wifi = connect_wifi(timeout=10)
            if not wifi.isconnected():
                deepsleep()
            mqtt = connect_mqtt(MQTT_SERVER, SENSOR_NAME)

            dhtjson = read_dht()

            i2c = machine.I2C(scl=GPIO_SCL, sda=GPIO_SDA)
            bme = BME280(i2c=i2c)
            bmejson = format_bme280(bme)

            print("Read dht %s" % dhtjson)
            print("Read bme %s" % bmejson)
            mqtt.publish("afra.sensors", bytes(dhtjson, 'utf-8'))
            mqtt.publish("afra.sensors", bytes(bmejson, 'utf-8'))
            mqtt.disconnect()
            wifi.disonnect()
            deepsleep()
    except:
        deepsleep()
