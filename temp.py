import esp
import machine
import network
import dht
from bme280 import BME280
import ujson as json
from utime import sleep
from umqtt.simple import MQTTClient

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
    machine.deepsleep((MEASURE_TIME - 10) * 1000)

def main():
    try:
        while True:
            print("Connecting to Wifi")
            wifi = connect_wifi(timeout=10)
            if not wifi.isconnected():
                print("Can't connect to wifi")
                deepsleep()
            print("Connecting to MQTT")
            mqtt = connect_mqtt(MQTT_SERVER, SENSOR_NAME)

            dhtjson = read_dht()
            print("Read dht %s" % dhtjson)

            i2c = machine.SoftI2C(scl=machine.Pin(GPIO_SCL), sda=machine.Pin(GPIO_SDA))
            bme = BME280(i2c=i2c)
            bmejson = format_bme280(bme)
            print("Read bme %s" % bmejson)

            print("Publishing to mqtt")
            mqtt.publish("afra.sensors", bytes(dhtjson, 'utf-8'))
            mqtt.publish("afra.sensors", bytes(bmejson, 'utf-8'))
            mqtt.disconnect()
            wifi.disconnect()
            print("Successful cycle, going into deepsleep")
            deepsleep()
    except Exception as exp:
        print("Exception occured %s" % exp)
        deepsleep()
