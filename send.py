import paho.mqtt.client as mqtt
import time  # 메시지 전송 간격을 위해 추가

# Broker address
broker_address = "10.150.151.226"
client1 = mqtt.Client("python_pub_1")  # 발행자 역할을 반영하도록 이름 변경

# Callback for successful connection
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

client1.on_connect = on_connect

# Connect to broker
client1.connect(broker_address, 1883)
client1.loop_start()  # 백그라운드에서 네트워크 루프 시작

# 메시지 발행 루프
try:
    while True:
        message = "Hello from Python Publisher"
        client1.publish("jetson/jetson", message)
        print(f"Published: {message}")
        time.sleep(1)  # 1초 간격으로 메시지 전송

except KeyboardInterrupt:
    print("발행자 종료")
    client1.loop_stop()
    client1.disconnect()