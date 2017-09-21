import dht
import machine
import network
import time
from umqtt.simple import MQTTClient

SSID = 'HelloWorld'
NETWORK_PASS = 'coolpassword'
SENSOR_NAME = 'room_humidity_1'
MQTT_TOPIC = 'sensor_net/room_humidity'
MQTT_SERVER = '192.168.42.1'
DHT_SENSOR_PIN = 14

red_led = machine.Signal(0, machine.Pin.OUT, invert=True)
blue_led = machine.Signal(2, machine.Pin.OUT, invert=True)
red_led.off()
blue_led.off()

temp_sensor = machine.ADC(0)

# Disable access point interface
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# Station (client) interface
sta_if = network.WLAN(network.STA_IF)


def toggle(pin):
    pin.value(not pin.value())


def flash(led, count=2):
    while count > 0:
        toggle(led)
        time.sleep_ms(225)

        toggle(led)
        time.sleep_ms(200)

        count -= 1

    time.sleep_ms(550)


def mqtt_connect():
    '''Wait for MQTT connection'''
    while True:
        try:
            mqtt_client = MQTTClient(SENSOR_NAME, MQTT_SERVER)
            mqtt_client.connect()
            flash(red_led, count=2)
            return mqtt_client
        except:
            flash(blue_led, count=6)


def read_temp_sensor():
    '''Read analog TMP36GZ temperature sensor'''
    sensor_reading = temp_sensor.read()
    celsius = (sensor_reading - 500) / 10
    fahrenheit = (celsius * 1.8) + 32
    print(sensor_reading, fahrenheit)
    return fahrenheit


def main():
    # Connect to wifi
    while not sta_if.isconnected():
        flash(blue_led)
        sta_if.active(True)
        sta_if.connect(SSID, NETWORK_PASS)
        flash(red_led)
        time.sleep(5)

    mqtt_client = mqtt_connect()
    dht_sensor = dht.DHT22(machine.Pin(DHT_SENSOR_PIN))
    retries = 0

    while True:
        if sta_if.isconnected():
            flash(red_led, count=2)
            try:
                # sensor needs a cooldown period
                time.sleep(2)
                dht_sensor.measure()
                humidity = dht_sensor.humidity()
                temp = dht_sensor.temperature()
                reading = '{}, {}'.format(humidity, temp)
                print(reading)

                mqtt_client.publish(MQTT_TOPIC,
                                    reading)
            except Exception as e:
                print(e)
                flash(blue_led, count=4)

                # sensor reading fails on the first try at boot
                retries += 1
                if retries > 5:
                    return
        else:
            sta_if.connect(SSID, NETWORK_PASS)
            flash(blue_led, count=10)


if __name__ == '__main__':
    main()
