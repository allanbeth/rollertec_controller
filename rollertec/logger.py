# rollertec/logger.py

from rollertec.config_manager import LOG_FILE

import logging, os

class RollertecLogger:
    """
    Singleton logger class for Rollertec.
    Handles logging to both file and console, with log file size management.
    """
    _instance = None

    def __new__(cls):
        # Ensure only one instance (singleton pattern)
        if cls._instance is None:
            cls._instance = super(RollertecLogger, cls).__new__(cls)
            cls._instance._init_logger()
        return cls._instance

    def _init_logger(self):
        """
        Initialize the logger, set up file and console handlers.
        """
        self.max_log_size = 5 * 1024 * 1024  # Default max log size: 5MB
        self.logger = logging.getLogger("rollertec")
        self.logger.setLevel(logging.INFO)

        # Only add handlers if they haven't been added yet
        if not self.logger.handlers:
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

            # File handler for persistent logs
            file_handler = logging.FileHandler(LOG_FILE)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

            # Console handler for real-time output
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def set_log_size(self, max_mb):
        """
        Set the maximum log file size.

        Args:
            max_mb (int): Maximum log file size in megabytes.
        """
        self.max_log_size = max_mb * 1024 * 1024
        self.info("Log file size limit set to {}MB.".format(max_mb))

    def _check_log_size(self):
        """
        Check if the log file exceeds the maximum size.
        If so, reset (truncate) the log file.
        """
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > self.max_log_size:
            with open(LOG_FILE, 'w') as f:
                pass  # Truncate the file
            self.logger.info("Log file reset due to size limit.")

    # Logging methods for different levels
    def debug(self, msg):
        self._check_log_size() 
        self.logger.debug(msg)

    def info(self, msg):
        self._check_log_size() 
        self.logger.info(msg)

    def warning(self, msg):
        self._check_log_size() 
        self.logger.warning(msg)

    def error(self, msg):    
        self._check_log_size() 
        self.logger.error(msg)

    def critical(self, msg): 
        self._check_log_size() 
        self.logger.critical(msg)