import paho.mqtt.client as mqtt

# subscriber callback
def on_message(client, userdata, message):
    print("message received: ", str(message.payload.decode("utf-8")))
    print("message topic: ", message.topic)
    print("message qos: ", message.qos)
    print("message retain flag: ", message.retain)

# 브로커 주소 설정
broker_address = "broker.mqtt.cool"
client1 = mqtt.Client("python_pub_1")  # 클라이언트 ID 변경

# 연결 성공 시 호출되는 콜백
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("jetson/jetson")  # 구독하기

client1.on_connect = on_connect
client1.on_message = on_message

# 브로커에 연결
client1.connect(broker_address)

# 메시지 루프 시작
client1.loop_forever()