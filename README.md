# Rollertec Garage Door Controller

A Python-based web and MQTT controller for garage doors, designed for easy integration with Home Assistant and remote operation via a web interface.

---

## Table of Contents

- [Features](#features)
- [Hardware & Wiring](#hardware--wiring)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Web Interface](#web-interface)
- [MQTT Integration](#mqtt-integration)
- [Home Assistant Integration](#home-assistant-integration)
- [Remote GPIO with pigpio](#remote-gpio-with-pigpio)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

- Control your garage door via a web interface or MQTT.
- View logs and update configuration from any device.
- Integrates easily with Home Assistant.
- Supports remote GPIO and multiple safety features.
- Supports remote relay control using pigpio.

---

## Hardware & Wiring

### Hardware Used

- **Raspberry Pi Zero W** (or compatible Pi)
- **2 or 3 Channel Relay DC 5V**
- **Rollertec Main Controller** (your garage door controller board)
- Jumper wires

### Wiring Instructions

#### 1. **Relay Power**
- Connect the relay module's VCC to the Pi's 5V pin.
- Connect the relay module's GND to the Pi's GND pin.

#### 2. **Relay Control Pins**
- Connect **IN1** on the relay to the Pi GPIO pin you set as `open_pin` (default: GPIO17).
- Connect **IN2** on the relay to the Pi GPIO pin you set as `close_pin` (default: GPIO27).
- (Optional) If using a stop button, connect **IN3** to the Pi GPIO pin set as `stop_pin` (default: GPIO22).

#### 3. **Relay to Rollertec Main Controller**
- The relay's NO (Normally Open) and COM (Common) terminals act as a switch.
- Wire each relay channel's NO and COM in parallel with the corresponding button (Open, Close, Stop) on your Rollertec main controller.
- When the Pi activates a relay, it "presses" the button by closing the circuit.

#### 4. **Example GPIO Pinout**

| Function | Pi GPIO Pin | Relay IN Pin |
|----------|-------------|--------------|
| Open     | 17          | IN1          |
| Close    | 27          | IN2          |
| Stop     | 22          | IN3 (if used)|

> **Note:** Double-check your relay module's pinout and your Pi's GPIO numbering.  
> Use female-to-female jumper wires for Pi to relay connections.

#### 5. **Safety**
- Ensure all wiring is done with the Pi powered off.
- Never connect mains voltage to the relay unless you are qualified to do so.
- The relay only switches the low-voltage circuits of your garage controller.

---

## Installation

### Prerequisites

- Python 3.7+
- `pip` (Python package manager)
- Raspberry Pi OS or compatible Linux
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
You may need to run as `sudo` for GPIO access.

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

- `remote_gpio`: Set to `1` to enable remote GPIO using pigpio.
- `gpio_address`: The IP address or hostname of the remote Raspberry Pi running the pigpio daemon.

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

You can integrate Rollertec with Home Assistant in two ways:

### 1. **Manual Configuration**

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

### 2. **HACS MQTT Integration**

Alternatively, you can use the [Home Assistant Community Store (HACS) MQTT Integration](https://hacs.xyz/docs/integration/mqtt/) for easier setup and management.

**Note:**  
- Adjust topics and payloads as needed to match your setup.
- Ensure your MQTT broker is accessible to both Rollertec and Home Assistant.

---

## Remote GPIO with pigpio

Rollertec supports controlling GPIO pins on a **remote Raspberry Pi** using the [pigpio](http://abyz.me.uk/rpi/pigpio/) library and daemon.

### How to Enable Remote GPIO

1. **On the Remote Raspberry Pi (the one connected to the relay):**

    - Install pigpio:
      ```bash
      sudo apt-get update
      sudo apt-get install pigpio python3-pigpio
      ```
    - Start the pigpio daemon:
      ```bash
      sudo systemctl enable pigpiod
      sudo systemctl start pigpiod
      ```
    - Ensure the Pi is on the same network as your Rollertec controller.

2. **On the Rollertec Controller Pi:**

    - In `config.json`:
      - Set `"remote_gpio": 1`
      - Set `"gpio_address"` to the IP address or hostname of the remote Pi running pigpio.

    Example:
    ```json
    {
        "remote_gpio": 1,
        "gpio_address": "192.168.1.42"
    }
    ```

3. **Restart Rollertec** after making these changes.

> **Note:**  
> When using remote GPIO, the Rollertec software will send relay commands over the network to the remote Pi.

---

## Troubleshooting

- **Webserver not starting:** Check for port conflicts or missing dependencies.
- **MQTT not working:** Verify broker address/port and network connectivity.
- **GPIO errors:** Ensure you are running as a user with GPIO access (often `sudo` is required on Raspberry Pi).
- **Logs not updating:** Check file permissions on `rollertec.log`.
- **Relay not switching:** Double-check GPIO pin numbers, wiring, and that the Pi is supplying 5V to the relay module.
- **Relay fires but door does not open:** Try increasing the `press_time` value in your configuration. Some garage controllers require a longer signal to register a button press.
- **Remote GPIO not working:** Ensure the pigpio daemon (`pigpiod`) is running on the remote Pi, and that firewalls are not blocking port 8888.

---

## License

MIT License.  

---

**Project maintained by allanbeth (https://github.com/allanbeth).**