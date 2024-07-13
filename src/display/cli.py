from utils.constants import *
from utils.logger import get_log
from utils.core import generate


class CLI:
    def __init__(self):
        pass

    def start(self):
        log = get_log()
        log.info("Start cli...")
        table = generate()
        print(table)
        log.info("End cli...")
