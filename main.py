# main.py

from rollertec.config_manager import ConfigManager
from rollertec.rollertec_manager import RollertecManager


config = ConfigManager()
manager = RollertecManager(config)

       
if __name__ == "__main__":    
    # Start Rollertec
    manager.webserver.start()

    

        