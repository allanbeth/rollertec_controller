# rollertech/controller.py

import time

class GarageDoorController:
    def __init__(self, config):
        self.config = config

        if self.config['remote_gpio'] == 1:
            import pigpio
            self.pi = pigpio.pi(self.config.get("gpio_address", "localhost"))
            if not self.pi.connected:
                raise RuntimeError("Could not connect to remote pigpio")
        else:
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
            self.GPIO.setmode(GPIO.BCM)
            self.GPIO.setwarnings(False)
            for pin in [self.config['open_pin'], self.config['close_pin'], self.config['stop_pin']]:
                self.GPIO.setup(pin, self.GPIO.OUT, initial=self.GPIO.HIGH)
                #self.GPIO.output(pin, self.GPIO.LOW)

    def trigger(self, pin):
        if self.config['remote_gpio'] == 1:
            self.pi.write(pin, 1)
            time.sleep(self.config['press_time'])
            self.pi.write(pin, 0)
        else:
            self.GPIO.output(pin, self.GPIO.HIGH)
            time.sleep(self.config['press_time'])
            self.GPIO.output(pin, self.GPIO.LOW)

    def open(self):
        self.trigger(self.config['open_pin'])

    def close(self):
        self.trigger(self.config['close_pin'])

    def stop(self):
        self.trigger(self.config['stop_pin'])

    def cleanup(self):
        self.GPIO.cleanup()
