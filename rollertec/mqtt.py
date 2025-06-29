# rollertec/mqtt.py

from rollertec.config_manager import MQTT_TOPIC_PREFIX, DEVICE_ID
import paho.mqtt.client as mqtt
import json

class MqttPublisher:
    """
    Handles MQTT connection, publishing, and Home Assistant discovery for the Rollertec controller.
    """
    def __init__(self, broker, port, logger):
        """
        Initialize the MQTT client and connect to the broker.
        Args:
            broker (str): MQTT broker address.
            port (int): MQTT broker port.
            logger: Logger instance for logging events.
        """
        self.logger = logger
        self.broker = broker
        self.port = port
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.logger.info(f'MQTT: {self.broker} : {self.port}')
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
        except Exception as e:
            self.logger.error(f"Failed to connect to MQTT broker: {e}")
        
    def on_connect(self, client, userdata, flags, rc):
        """
        Callback when the MQTT client connects to the broker.
        Subscribes to the command topic and publishes discovery info.
        """
        self.logger.info("Connected to MQTT")
        self.client.subscribe(f"{MQTT_TOPIC_PREFIX}/set")
        self.publish_discovery()

    def publish_discovery(self):
        """
        Publishes Home Assistant MQTT discovery configuration for the garage door cover entity.
        """
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
            }
        }
        # Retain discovery message so Home Assistant can discover device after restart
        self.client.publish(config_topic, json.dumps(config_payload), retain=True)

    def publish_state(self, state):
        """
        Publishes the current state of the garage door to the MQTT state topic.
        Args:
            state (str): The state to publish (e.g., "open", "closed").
        """
        topic = f"{MQTT_TOPIC_PREFIX}/state"
        self.logger.info(f"Publishing state: {state}")
        self.client.publish(topic, state, retain=True)