import paho.mqtt.client as mqtt
from datetime import datetime
import os

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = "87net3za5cF7OuwM-6eKGgt2Ysf0M64YFLQdt2AN333QJi_rraPWxsElhH_6oRs04P_heIYH14iyvJ0fz_R8yA=="
org = "giovanni.castaldi@fermi.mo.it"
bucket = "temperature"
clientDB = InfluxDBClient(url="https://europe-west1-1.gcp.cloud2.influxdata.com/", token=token, org=org)

BROKER = 'mqtt.ssh.edu.it'
TOPIC = '4F/temperature/group9'


def on_connect(client, userdata, flags, rc):
    print(f'{mqtt.connack_string(rc)}')
    print('MQTT client subscribing...', end = ' ')
    client.subscribe(TOPIC)

def on_subscribe(client, userdata, mid, granted_qos):
    print(f'subscribed {TOPIC} with QoS: {granted_qos[0]}\n')

def on_message(client, userdata, msg):
    print(msg.payload.decode())
    value = msg.payload.decode()

    point = Point("TEMPERATURES") \
        .tag("device", "MSP430") \
        .tag("group", "9") \
        .field("temp", float(value))
    write_api = clientDB.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket, org, point)


def main():
    client = mqtt.Client()
    #events --> callback association
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message

    #client --> broker connection
    print('MQTT client connecting...', end = ' ')
    client.connect(BROKER)

    #wait and listen for events (ctrl-c to quit)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print('\nMQTT client disconnecting...bye')
        clientDB.close()
    finally:
        client.disconnect()

if name == 'main':
    main()