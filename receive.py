import paho.mqtt.client as mqtt

# subscriber callback
def on_message(client, userdata, message):
    print("message received: ", str(message.payload.decode("utf-8")))
    print("message topic: ", message.topic)
    print("message qos: ", message.qos)
    print("message retain flag: ", message.retain)

# Broker address
broker_address = "10.150.151.226"  # Ensure this is the correct IP address
client1 = mqtt.Client("python_sub_1")  # Changed client name to reflect subscriber role

# Callback for successful connection
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("jetson/jetson")  # Ensure this is the correct topic

client1.on_connect = on_connect
client1.on_message = on_message

# Connect to broker
client1.connect(broker_address,1883)  # Ensure the correct port is used if needed

# Start the message loop
client1.loop_forever()