# rollertech/controller.py

import time

class GarageDoorController:
    """
    Controls the garage door via GPIO or remote pigpio.
    """

    def __init__(self, config):
        """
        Initialize the controller with the provided configuration.
        Sets up GPIO or pigpio depending on 'remote_gpio' config.
        """
        self.config = config

        # Ensure all required config keys are present
        required_keys = ['remote_gpio', 'open_pin', 'close_pin', 'stop_pin', 'press_time']
        missing_keys = [key for key in required_keys if key not in self.config]
        if missing_keys:
            raise KeyError(f"Missing required config keys: {', '.join(missing_keys)}")

        # Use pigpio for remote GPIO control
        if self.config['remote_gpio'] == 1:
            import pigpio
            self.pi = pigpio.pi(self.config.get("gpio_address", "localhost"))
            if not self.pi.connected:
                raise RuntimeError("Could not connect to remote pigpio")
        else:
            # Use RPi.GPIO for local GPIO control
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
            self.GPIO.setmode(GPIO.BCM)
            self.GPIO.setwarnings(False)
            # Set all control pins as outputs, default HIGH (relay off)
            for pin in [self.config['open_pin'], self.config['close_pin'], self.config['stop_pin']]:
                self.GPIO.setup(pin, self.GPIO.OUT, initial=self.GPIO.HIGH)

    def trigger(self, pin):
        """
        Activates the relay connected to the given pin for the configured press_time.
        """
        if self.config['remote_gpio'] == 1:
            # For pigpio, set pin HIGH, wait, then LOW
            self.pi.write(pin, 1)
            time.sleep(self.config['press_time'])
            self.pi.write(pin, 0)
        else:
            # For RPi.GPIO, set pin HIGH, wait, then LOW
            self.GPIO.output(pin, self.GPIO.HIGH)
            time.sleep(self.config['press_time'])
            self.GPIO.output(pin, self.GPIO.LOW)

    def open(self):
        """
        Trigger the 'open' relay.
        """
        self.trigger(self.config['open_pin'])

    def close(self):
        """
        Trigger the 'close' relay.
        """
        self.trigger(self.config['close_pin'])

    def stop(self):
        """
        Trigger the 'stop' relay.
        """
        self.trigger(self.config['stop_pin'])

    def cleanup(self):
        """
        Clean up GPIO resources (only for local GPIO).
        """
        if self.config['remote_gpio'] != 1:
            self.GPIO.cleanup()