# rollertec.rollertec_manager.py

from rollertec.logger import rollertecLogger
from rollertec.controller import GarageDoorController
from rollertec.webserver import flaskWrapper
from rollertec.mqtt import mqttPublisher
import json, time

class rollertecManager:
    def __init__(self, cnfMgr):
        self.cnfMgr = cnfMgr
        self.logger = rollertecLogger()
        self.ctrl = GarageDoorController(self.cnfMgr.config_data)
        self.mqtt_broker = self.cnfMgr.config_data['mqtt_broker']
        self.mqtt_port = self.cnfMgr.config_data['mqtt_port']
        self.roller_time = self.cnfMgr.config_data['roller_time'] 
        self.mqtt = mqttPublisher(self.mqtt_broker, self.mqtt_port, self.logger)
        self.mqtt.client.on_message = self.on_message 
        self.webserver = flaskWrapper(self.cnfMgr, self.logger)
        self.webserver.on_press = self.on_press


    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode().upper()
        if payload == "OPEN":
            self.mqtt.publish_state("Opening")
            self.ctrl.open()
            time.sleep(self.roller_time)
            self.mqtt.publish_state("Open")
            self.logger.info("MQTT - Open")
        elif payload == "CLOSE":
            self.mqtt.publish_state("Closing")
            self.ctrl.close()
            time.sleep(self.roller_time)
            self.mqtt.publish_state("Closed")
            self.logger.info("MQTT - Close")
        elif payload == "STOP":
            self.ctrl.stop()
            self.logger.info("MQTT - Stop")

    def on_press(self, key):
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



