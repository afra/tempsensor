import esp
import machine
import network
import dht
import ujson as json
from utime import sleep

from umqtt.simple import MQTTClient

# https://github.com/micropython/micropython-lib/blob/master/umqtt.simple/example_pub_button.py

MQTT_SERVER = "172.28.0.1"
SENSOR_NAME = "afra-t1"

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

def read_sensor():
    sensor = dht.DHT22(machine.Pin(5))
    sensor.measure()
    result = {
        "name": SENSOR_NAME,
        "data": {
            "temp": sensor.temperature(),
            "humidity": sensor.humidity(),
            },
        "measuretime": MEASURE_TIME,
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
            result = read_sensor()
            print("Read sensor %s" % result)
            mqtt.publish("afra.sensors", bytes(result, 'utf-8'))
            mqtt.disconnect()
            wifi.disonnect()
            deepsleep()
    except:
        deepsleep()
