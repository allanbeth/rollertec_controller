# rollertec/webserver.py

from flask import Flask, render_template, jsonify, request
from pathlib import Path

class FlaskWrapper:
    """
    Flask web server wrapper for the Rollertec controller.
    Handles web UI, API endpoints, and serves static files.
    """

    def __init__(self, config, logger):
        # Store references to config manager and logger
        self.config_manager = config
        self.logger = logger
        self.logger.info(f"Controller loaded")
        self.config_data = self.config_manager.config_data

        # Read host/port from config
        self.host = self.config_data['webserver_host']
        self.port = int(self.config_data['webserver_port'])
        self.logger.info(f'WEB: {self.host} : {self.port}')

        # Set up paths for templates, static files, README, and log file
        self.root = Path(__file__).parents[1]
        self.templatePath = self.root / "templates/"
        self.stylePath = self.root / "static/"
        self.readmePath = self.root / "README.md"
        self.logFilePath = self.root / "rollertec.log"

        # Initialize Flask app with custom template and static folders
        self.app = Flask(__name__, template_folder=str(self.templatePath), static_folder=str(self.stylePath))

        # Register routes for web UI and API endpoints
        self.app.route("/", methods=["GET", "POST"])(self.main)
        self.app.route('/open', methods=["POST"])(self.open_door) 
        self.app.route('/close', methods=["POST"])(self.close_door) 
        self.app.route("/stop", methods=["POST"])(self.stop_door)
        self.app.route("/log", methods=["GET", "POST"])(self.get_log_file)
        self.app.route("/config", methods=["POST"])(self.save_config)
        self.app.route("/about", methods=["GET"])(self.get_readme)

    def main(self):
        """
        Render the main web UI (index.html) and pass current config data.
        """
        self.logger.info(f"index.html loaded successfully")
        return render_template("index.html", config_data=self.config_manager.config_data)
    
    def on_press(self, key):
        """
        Placeholder for button press handling.
        Should be overridden by the main manager to handle actions.
        """
        raise NotImplementedError("on_press method must be implemented to handle key actions.")
    
    def open_door(self):
        """
        API endpoint to trigger the 'open' action.
        """
        self.on_press('OPEN')
        return jsonify({"status": "opened"})

    def close_door(self):
        """
        API endpoint to trigger the 'close' action.
        """
        self.on_press('CLOSE')
        return jsonify({"status": "closed"})

    def stop_door(self):
        """
        API endpoint to trigger the 'stop' action.
        """
        self.on_press('STOP')
        return jsonify({"status": "stopped"})
    
    def get_log_file(self):
        """
        API endpoint to retrieve the last 100 lines of the log file.
        Returns logs in reverse order (most recent first).
        """
        if not self.logFilePath.exists():
            return jsonify({"logs": []})
        try:
            self.logger.info(f"Retrieving Logs")
            with open(self.logFilePath, "r") as f:
                lines = f.readlines()
                
            # Return last N lines (e.g., 100) as a list of strings for clarity
            logs = [line.strip() for line in lines[-100:]][::-1]
            self.logger.info(f"Loaded logs successfully")
            return jsonify({"logs": logs})
        except Exception as e:
            return jsonify({"error": str(e), "logs": []}), 500

    def save_config(self):
        """
        API endpoint to save configuration changes from the web UI.
        """
        data = request.get_json()
        self.config_manager.save_config(data)
        self.logger.info(f"Configuration Saved")
        return jsonify({"status": "saved"})
    
    def get_readme(self):
        """
        API endpoint to fetch the README.md content for the About page.
        """
        if self.readmePath.exists():
            with open(self.readmePath, "r", encoding="utf-8") as f:
                content = f.read()
            self.logger.info(f"README.md loaded successfully")
            return jsonify({"content": content})
        else:
            return jsonify({"error": "README.md not found"}), 404

    def start(self):
        """
        Start the Flask web server.
        """
        self.app.run(host=self.host, port=self.port, debug=True, use_reloader=False)