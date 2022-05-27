import paho.mqtt.client as mqtt
import serial

BROKER = 'mqtt.ssh.edu.it'
TOPIC_PUB = '4F/temperature/group9'
port = serial.Serial('COM4')

def on_connect(client, userdata, flags, rc):
    #print(f'{mqtt.connack_string(rc)}')
    event_flag = True


def on_publish(client, userdata, mid):
    #print(f'msg published with id: {mid}')
    event_flag = True

def main():
    client = mqtt.Client()

    # events --> callback association
    client.on_connect = on_connect
    client.on_publish = on_publish

    # client --> broker connection
    print('MQTT client connecting...', end=' ')
    client.connect(BROKER)
    client.loop_start()

    try:
        while True:
            msg = port.readline().decode('ascii').strip()
            print(msg)
            client.publish(TOPIC_PUB, msg)

    except KeyboardInterrupt:
        print('\nMQTT client disconnecting...bye')
    finally:
        client.disconnect()
        client.loop_stop()

if __name__ == '__main__':
    main()