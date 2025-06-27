# main.py

from rollertec.config_manager import configManager
from rollertec.rollertec_manager import rollertecManager


config = configManager()
manager = rollertecManager(config)

       
if __name__ == "__main__":    
    # Start Rollertec
    manager.webserver.start()

    

        