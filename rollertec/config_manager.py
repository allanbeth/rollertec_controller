# rollertec.config_manager.py

ROOT_PATH = "Path(__file__).parents[1]"
LOG_FILE = "rollertec.log"
CONFIG_FILE = "config.json"
MQTT_TOPIC_PREFIX = "homeassistant/cover/rollertec_garage"
MQTT_DISCOVERY_PREFIX = "homeassistant"
DEVICE_ID = "rollertec_garage_door"

from rollertec.logger import rollertecLogger

import json

class configManager:
    def __init__(self):
        self.logger = rollertecLogger()
        self.config_data = self.load_config()
        
    def load_config(self):
        try:
            with open(CONFIG_FILE, "r") as f:
                self.logger.info(f"Config file opened Successfully.")
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning(f"Config file not found, creating default config.")
            default_config = {
                "max_log": 5,
                "open_pin": 17, 
                "close_pin": 27, 
                "stop_pin": 22, 
                "roller_time": 10,
                "press_time": 0.5,
                "stop_btn": 0,
                "mqtt_broker": "localhost",
                "mqtt_port": 1883,
                "webserver_host": "0.0.0.0",
                "webserver_port": 5000,
                "remote_gpio": 0,
                "gpio_address": "localhost"
                }  
            try:
                with open(CONFIG_FILE, "w") as f:
                    json.dump(default_config, f, indent=4)
                self.logger.info(f"Created new config file at {CONFIG_FILE}.")

            except Exception as e:
                self.logger.error(f"Failed to create config file: {e}")
            
            return default_config
            
    def save_config(self, config):
        self.logger.info(f"Saving config file at {CONFIG_FILE}.")

        new_config = {
            "max_log": int(config['max_log']),
            "open_pin": int(config['open_pin']), 
            "close_pin": int(config['close_pin']), 
            "stop_pin": int(config['stop_pin']), 
            "roller_time": int(config['roller_time']),
            "press_time": (config['press_time']),
            "stop_btn": int(config['stop_btn']),
            "mqtt_broker": config['mqtt_broker'],
            "mqtt_port": int(config['mqtt_port']),
            "webserver_host": config['webserver_host'],
            "webserver_port": config['webserver_port'],
            "remote_gpio": int(config['remote_gpio']),
            "gpio_address": config['gpio_address']
        }

        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(new_config, f, indent=4)
            self.logger.info(f"Saved config file at {CONFIG_FILE}.")
            self.config_data = new_config

        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")


    def reload_config (self):
        self.config_data = self.load_config()
        self.logger.info("Configuration reloaded from disk.")
	     
	     	
			