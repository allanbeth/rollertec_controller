import time
import pigpio

class GarageDoorController:
    """
    Controls the garage door via pigpio (local or remote).
    """

    def __init__(self, config):
        """
        Initialize the controller with the provided configuration.
        Uses pigpio for both local and remote GPIO.
        """
        self.config = config

        # Ensure all required config keys are present
        required_keys = ['remote_gpio', 'open_pin', 'close_pin', 'stop_pin', 'press_time']
        missing_keys = [key for key in required_keys if key not in self.config]
        if missing_keys:
            raise KeyError(f"Missing required config keys: {', '.join(missing_keys)}")

        # pigpio local or remote
        if self.config['remote_gpio'] == 1:
            # Remote pigpio
            address = self.config.get("gpio_address", "localhost")
            self.pi = pigpio.pi(address)
        else:
            # Local pigpio
            self.pi = pigpio.pi()

        if not self.pi.connected:
            raise RuntimeError("Could not connect to pigpio daemon")

        # Set all control pins as outputs, default LOW (relay off)
        for pin in [self.config['open_pin'], self.config['close_pin'], self.config['stop_pin']]:
            self.pi.set_mode(pin, pigpio.OUTPUT)
            self.pi.write(pin, 0)

    def trigger(self, pin):
        """
        Activates the relay connected to the given pin for the configured press_time.
        """
        self.pi.write(pin, 1)
        time.sleep(self.config['press_time'])
        self.pi.write(pin, 0)

    def open(self):
        self.trigger(self.config['open_pin'])

    def close(self):
        self.trigger(self.config['close_pin'])

    def stop(self):
        self.trigger(self.config['stop_pin'])

    def cleanup(self):
        """
        Clean up pigpio resources.
        """
        self.pi.stop()
