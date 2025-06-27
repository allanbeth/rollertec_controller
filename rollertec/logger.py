import logging
import os
from rollertec.config_manager import LOG_FILE

class rollertecLogger:
    _instance = None 

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(rollertecLogger, cls).__new__(cls)
            cls._instance._init_logger()
        return cls._instance

    def _init_logger(self):
        self.max_log_size = 5 * 1024 * 1024 
        self.logger = logging.getLogger("rollertec")
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

            file_handler = logging.FileHandler(LOG_FILE)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def set_log_size(self, max_mb):
        self.max_log_size = max_mb * 1024 * 1024
        self.info("Log file size limit set to {}MB.".format(max_mb))

    def _check_log_size(self):
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > self.max_log_size:
            with open(LOG_FILE, 'w') as f:
                pass
            self.logger.info("Log file reset due to size limit.")

    def debug(self, msg):    self._check_log_size(); self.logger.debug(msg)
    def info(self, msg):     self._check_log_size(); self.logger.info(msg)
    def warning(self, msg):  self._check_log_size(); self.logger.warning(msg)
    def error(self, msg):    self._check_log_size(); self.logger.error(msg)
    def critical(self, msg): self._check_log_size(); self.logger.critical(msg)
