# Rollertec Garage Door Controller

A Python-based web and MQTT controller for garage doors, designed for easy integration with Home Assistant and remote operation via a web interface.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Web Interface](#web-interface)
- [MQTT Integration](#mqtt-integration)
- [Home Assistant Integration](#home-assistant-integration)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

- Control your garage door via a web interface or MQTT.
- View logs and update configuration from any device.
- Integrates easily with Home Assistant.
- Supports remote GPIO and multiple safety features.

---

## Installation

### Prerequisites

- Python 3.7+
- `pip` (Python package manager)
- A Raspberry Pi or Linux system with GPIO access (for direct control)
- (Optional) MQTT broker (e.g., Mosquitto) for MQTT integration

### Clone the Repository

```bash
git clone https://github.com/yourusername/rollertec.git
cd rollertec/Rollertec
```

### Install Dependencies

It is recommended to use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Note:**  
If you use GPIO, ensure you have the necessary permissions and libraries (e.g., `RPi.GPIO`).

---

## Configuration

The main configuration file is `config.json` in the `Rollertec` directory.  
It is created automatically on first run if it does not exist.

**Example `config.json`:**

```json
{
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
```

You can edit this file manually or via the web interface under the **Configuration** tab.

---

## Usage

### Start the Webserver

From the `Rollertec` directory, run:

```bash
python3 main.py
```

The web interface will be available at `http://<your-pi-ip>:<webserver_port>/` (default: `http://localhost:5000/`).

### Web Interface

- **Main Controls:** Open, Stop, and Close your garage door.
- **Log File:** View recent log entries.
- **Configuration:** Edit settings such as GPIO pins, MQTT, and webserver options.
- **About:** View this README and project info.

---

## Web Interface

- Accessible from any device on your network.
- Responsive design for mobile and desktop.
- Navigation bar for quick access to controls, logs, configuration, and about page.

---

## MQTT Integration

Rollertec can publish and receive commands via MQTT for integration with automation systems.

**MQTT Settings in `config.json`:**

- `mqtt_broker`: Address of your MQTT broker (e.g., `localhost` or IP).
- `mqtt_port`: Port for MQTT (default: `1883`).

**MQTT Topics:**

- Commands and status are published under the prefix:  
  `homeassistant/cover/rollertec_garage`

**Example Home Assistant MQTT Discovery:**

Rollertec supports Home Assistant MQTT discovery.  
You may need to restart Home Assistant or manually add the cover entity.

---

## Home Assistant Integration

Add the following to your `configuration.yaml` in Home Assistant:

```yaml
cover:
  - platform: mqtt
    name: "Garage Door"
    command_topic: "homeassistant/cover/rollertec_garage/set"
    state_topic: "homeassistant/cover/rollertec_garage/state"
    payload_open: "OPEN"
    payload_close: "CLOSE"
    payload_stop: "STOP"
    state_open: "open"
    state_closed: "closed"
    optimistic: false
    qos: 1
```

**Note:**  
- Adjust topics and payloads as needed to match your setup.
- Ensure your MQTT broker is accessible to both Rollertec and Home Assistant.

---

## Troubleshooting

- **Webserver not starting:** Check for port conflicts or missing dependencies.
- **MQTT not working:** Verify broker address/port and network connectivity.
- **GPIO errors:** Ensure you are running as a user with GPIO access (often `sudo` is required on Raspberry Pi).
- **Logs not updating:** Check file permissions on `rollertec.log`.

---

## License

MIT License.  


---

**Project maintained by allanbeth (https://github.com/allanbeth).**