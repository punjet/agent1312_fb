from stem import Signal
from stem.control import Controller
import time
from modules.logger import logger

class TorManager:
    def __init__(self, control_port: int = 9051, password: str = None):
        self.port = control_port
        self.password = password

    def new_identity(self):
        with Controller.from_port(port=self.port) as controller:
            if self.password:
                controller.authenticate(self.password)
            controller.signal(Signal.NEWNYM)
            time.sleep(controller.get_newnym_wait())
            logger.info("Tor: new identity created")