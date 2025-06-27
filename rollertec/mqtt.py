# rollertec/mqtt.py

from rollertec.config_manager import MQTT_TOPIC_PREFIX, DEVICE_ID
import paho.mqtt.client as mqtt
import json

class mqttPublisher:
    def __init__(self, broker, port, logger):
        self.logger = logger
        self.broker = broker
        self.port = port
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.logger.info(f'MQTT: {self.broker} : {self.port}')
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()
        
    def on_connect(self, client, userdata, flags, rc):
        self.logger.info("Connected to MQTT")
        self.client.subscribe(f"{MQTT_TOPIC_PREFIX}/set")
        self.publish_discovery(client)

    def publish_discovery(self,client):
        config_topic = f"{MQTT_TOPIC_PREFIX}/config"
        config_payload = {
            "name": "Garage Door",
            "command_topic": f"{MQTT_TOPIC_PREFIX}/set",
            "state_topic": f"{MQTT_TOPIC_PREFIX}/state",
            "payload_open": "OPEN",
            "payload_close": "CLOSE",
            "payload_stop": "STOP",
            "state_open": "Open",
            "state_closed": "Closed",
            "optimistic": False,
            "device_class": "garage",
            "unique_id": DEVICE_ID,
            "device": {
                "identifiers": [DEVICE_ID],
                "name": "Rollertec Controller",
                "manufacturer": "allanbeth",
                "model": "Relay v2"
            }
        }
        self.client.publish(config_topic, json.dumps(config_payload), retain=True)

         
    def publish_state(self, state):
            topic = f"{MQTT_TOPIC_PREFIX}/state"
            self.logger.info(f"Publishing state: {state}")
            self.client.publish(topic, state, retain=True)
