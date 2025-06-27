# cli.py

from garage_door.controller import GarageDoorController
import sys

ctrl = GarageDoorController()

if len(sys.argv) < 2:
    print("Usage: python cli.py [open|close|stop]")
    sys.exit(1)

command = sys.argv[1].lower()
if command == "open":
    ctrl.open()
elif command == "close":
    ctrl.close()
elif command == "stop":
    ctrl.stop()
else:
    print("Unknown command. Use 'open', 'close' or 'stop'")
