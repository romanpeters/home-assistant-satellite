import sds011
import time
import paho.mqtt.client as paho

sensor = sds011.SDS011("/dev/ttyUSB0", use_query_mode=True)

def on_connect(client, userdata, flags, rc):
    print("Succesfully connected to MQTT broker" % (rc))

client = paho.Client()
client.on_connect = on_connect
client.connect("10.10.10.11", 1883)
client.loop_start()

freq = 900  # refresh rate

try:
  while True:
    sensor.sleep(sleep=False)
    time.sleep(15)  # Allow time for the sensor to measure properly
    pm25, pm10 = sensor.query()
    (rc, mid) = client.publish("satellite/sensor/pm25/state", pm25, qos=1)
    (rc, mid) = client.publish("satellite/sensor/pm10/state", pm10, qos=1)
    print("PM2.5:", pm25, "PM10:", pm10)
    sensor.sleep()
    time.sleep(freq - 15)
except KeyboardInterrupt:
  print("You pressed ctrl-c, quitting")
  sys.exit(0)
