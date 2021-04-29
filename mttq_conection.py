import paho.mqtt.publish as publish

# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code "+str(rc))

#     # Subscribing in on_connect() means that if we lose the connection and
#     # reconnect then subscriptions will be renewed.
#     client.subscribe("its_center/inqueue/cpm/0/3/1/3/3/2/2/3/3/3/0/1/0/0/0/3/0/0/1")

# # The callback for when a PUBLISH message is received from the server.
# def on_message(client, userdata, msg):
#     print(msg.topic+" "+str(msg.payload))

# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message

# client.connect("broker.es.av.it.pt", 1883, 60)

# # Blocking call that processes network traffic, dispatches callbacks and
# # handles reconnecting.
# # Other loop*() functions are available that give a threaded interface and a
# # manual interface.
# client.loop_forever()


publish.single(topic="its_center/inqueue/5g-mobility",payload= "payload", port=1883,hostname="broker.es.av.it.pt")
