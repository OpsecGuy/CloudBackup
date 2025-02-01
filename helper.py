from mega import Mega
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from datetime import datetime

import threading
import logging
import pathlib
import zipfile
import gnupg
import json
import glob
import time
import sys
import os


log = logging.Logger(__name__, level=logging.INFO)
log_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(threadName)s:%(funcName)s] - %(levelname)s - %(message)s")
log_handler.setFormatter(formatter)
log.addHandler(log_handler)


class Config():
    def __init__(self):
        self.file_name = "backup_config.json"
        if not pathlib.Path(self.file_name).exists():
            self.create_defaiult()
        else:
            self.data = self.load() 

    def create_defaiult(self):
        log.info(f"Creating default config file <{self.file_name}>")
        with open(self.file_name, "w+") as f:
            data = {
                "mega_login" : "",
                "mega_password": "",
                "encryption_key_file_name": "example.asc",
                "recipments": "xxx@gmail.com",
                "output_file_name": "output",
                "do_not_save_file_locally": False,
                "backup_repeat_delay": 0,
                "paths": ["/xxx", "/xxx"]
            }
            json.dump(data, f, indent=4)
        log.error("Update config file and run program again")
        os._exit(0)
    
    def load(self):
        with open(self.file_name, "r") as f:
            data = json.load(f)
        log.info("Config has been loaded successfully")
        return data




