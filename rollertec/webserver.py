# rollertec/web.py

from flask import Flask, render_template, jsonify, request, send_file, abort
from pathlib import Path

import json

class flaskWrapper:

    def __init__(self, config, logger):
        self.config_manager = config
        self.logger = logger
        self.logger.info(f"Controller loaded")
        self.config_data = self.config_manager.config_data
        self.host = self.config_data['webserver_host']
        self.port = int(self.config_data['webserver_port'])
        self.logger.info(f'WEB: {self.host} : {self.port}')
        self.root = Path(__file__).parents[1]
        self.templatePath = self.root / "templates/"
        self.stylePath = self.root / "static/"
        self.readmePath = self.root / "README.md"
        self.logFilePath = self.root / "rollertec.log"
        self.app = Flask(__name__, template_folder=self.templatePath, static_folder=self.stylePath)
        self.app.route("/", methods=["GET", "POST"])(self.main)
        self.app.route('/open', methods=["POST"])(self.open_door) 
        self.app.route('/close', methods=["POST"])(self.close_door) 
        self.app.route("/stop", methods=["POST"])(self.stop_door)
        self.app.route("/log", methods=["GET", "POST"])(self.get_log_file)
        self.app.route("/config", methods=["POST"])(self.save_config)
        self.app.route("/about", methods=["GET"])(self.get_readme)

    def main(self):
        self.logger.info(f"index.html loaded successfully")
        return render_template("index.html", config_data=self.config_manager.config_data)
    
    def on_press(self, key):
        return key
    
    def open_door(self):

        self.on_press('OPEN')
        return jsonify({"status": "opened"})

    def close_door(self):
        self.on_press('CLOSE')
        return jsonify({"status": "closed"})

    def stop_door(self):
        self.on_press('STOP')
        return jsonify({"status": "stopped"})
    
    
    def get_log_file(self):
        if not self.logFilePath.exists():
            return jsonify({"logs": []})
            
        try:
            self.logger.info(f"Retrieving Logs")
            with open(self.logFilePath, "r") as f:
                lines = f.readlines()

            # Return last N lines (e.g., 100)
            logs = [{"logs": line.strip()} for line in lines[-100:]][::-1]
            self.logger.info(f"Loaded logs")
            return jsonify({"logs": logs})
        except Exception as e:
            return jsonify({"error": str(e), "logs": []}), 500

    def save_config(self):
        data = request.get_json()
        self.config_manager.save_config(data)
        self.logger.info(f"Configuration Saved")
        return jsonify({"status": "saved"})
    
    def get_readme(self):
        if self.readmePath.exists():
            with open(self.readmePath, "r", encoding="utf-8") as f:
                content = f.read()
            self.logger.info(f"README.md loaded successfully")
            return jsonify({"content": content})
        else:
            return jsonify({"error": "README.md not found"}), 404

    def start(self):
         self.app.run(host=self.host, port=self.port, debug=True, use_reloader=False)