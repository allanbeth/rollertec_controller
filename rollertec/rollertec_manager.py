# rollertec.rollertec_manager.py

from rollertec.logger import RollertecLogger
from rollertec.controller import GarageDoorController
from rollertec.webserver import FlaskWrapper
from rollertec.mqtt import MqttPublisher
import json, time, threading

class RollertecManager:
    """
    Main manager class that ties together configuration, controller, MQTT, and webserver.
    Handles command routing and state updates.
    """
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.logger = RollertecLogger()
        # Initialize the garage door controller with config data
        self.ctrl = GarageDoorController(self.config_manager.config_data)
        # Extract MQTT broker and port from config
        self.mqtt_broker = self.config_manager.config_data['mqtt_broker']
        self.mqtt_port = self.config_manager.config_data['mqtt_port']
        # Ensure roller_time is present in config
        if 'roller_time' not in self.config_manager.config_data:
            raise KeyError("Missing required config key: 'roller_time'")
        self.roller_time = self.config_manager.config_data['roller_time']
        # Initialize MQTT publisher and set up message callback
        self.mqtt = MqttPublisher(self.mqtt_broker, self.mqtt_port, self.logger)
        self.mqtt.client.on_message = self.on_message
        # Initialize webserver and set up button press callback
        self.webserver = FlaskWrapper(self.config_manager, self.logger)
        self.webserver.on_press = self.on_press

    def on_message(self, client, userdata, msg):
        """
        Callback for handling incoming MQTT messages.

        Args:
            client: The MQTT client instance.
            userdata: The private user data as set in Client() or userdata_set().
            msg: An instance of MQTTMessage, which contains topic, payload, qos, retain.
        """
        payload = msg.payload.decode().upper()
        # Handle MQTT commands in separate threads to avoid blocking
        if payload == "OPEN":
            threading.Thread(target=self._handle_open).start()
        elif payload == "CLOSE":
            threading.Thread(target=self._handle_close).start()
        elif payload == "STOP":
            self.ctrl.stop()
            self.logger.info("MQTT - Stop")

    def _handle_open(self):
        """
        Handles the open command: publishes state, triggers open relay, waits, then updates state.
        """
        self.mqtt.publish_state("Opening")
        self.ctrl.open()
        time.sleep(self.roller_time)
        self.mqtt.publish_state("Open")
        self.logger.info("MQTT - Open")

    def _handle_close(self):
        """
        Handles the close command: publishes state, triggers close relay, waits, then updates state.
        """
        self.mqtt.publish_state("Closing")
        self.ctrl.close()
        time.sleep(self.roller_time)
        self.mqtt.publish_state("Closed")
        self.logger.info("MQTT - Close")

    def _handle_press(self, key):
        """
        Handles button presses from the web interface.
        Args:
            key (str): "OPEN", "CLOSE", or "STOP"
        """
        if key == "OPEN":
            self.mqtt.publish_state("Opening")
            self.ctrl.open()
            time.sleep(self.roller_time)
            self.mqtt.publish_state("Open")
            self.logger.info("WEB - Open")
        elif key == "CLOSE":
            self.mqtt.publish_state("Closing")
            self.ctrl.close()
            time.sleep(self.roller_time)
            self.mqtt.publish_state("Closed")
            self.logger.info("WEB - Close")
        elif key == "STOP":
            self.ctrl.stop()
            self.logger.info("WEB - Stop")

    def on_press(self, key):
        """
        Callback for web UI button presses. Runs the handler in a new thread.
        Args:
            key (str): "OPEN", "CLOSE", or "STOP"
        """
        threading.Thread(target=self._handle_press, args=(key,)).start()