import json
import os
import logging
from cryptography.fernet import Fernet

KEY_FILE = "pass_manager.key"
DATA_FILE = "pass_manager.data"
DATA_KEY_RECORD_ID_COUNTER = "record_id_counter"
DATA_KEY_DATA = "data"

class DataManager:

    def __init__(self, out_path):
        global KEY_FILE, DATA_FILE

        KEY_FILE = os.path.join(out_path, KEY_FILE)
        DATA_FILE = os.path.join(out_path, DATA_FILE)

        print("Key:", KEY_FILE)
        print("Data:", DATA_FILE)

        logging.debug("Initialize DataManager.")
        
        if not os.path.exists(KEY_FILE) and not os.path.exists(DATA_FILE):
            logging.debug("Both files not exist, so we need to do setup..")
            # Do setup
            self.key = Fernet.generate_key()

            # save key
            with open(KEY_FILE, mode="wb") as _token_file:
                _token_file.write(self.key)

            self.__json_data = {
                    DATA_KEY_RECORD_ID_COUNTER:0,
                    DATA_KEY_DATA:{}
            }

        elif not os.path.exists(KEY_FILE):
            raise Exception("key file missing at working directory.")
        elif not os.path.exists(DATA_FILE):
            raise Exception("data file missing at working directory.")
        else:
            logging.info("Both files are available.")

            with open(KEY_FILE, mode='rb') as _token_file:
                self.key = _token_file.read()
            
            with open(DATA_FILE, mode='rb') as _data_file:
                data = _data_file.read()
                data = Fernet(self.key).decrypt(data)
                data = data.decode('utf-8')

            self.__json_data = eval(data)


    def add(self, title, name, password, notes):
        logging.debug(f"{title}, {name}, {password}, {notes}")
        counter = self.__json_data[DATA_KEY_RECORD_ID_COUNTER] + 1
        self.__json_data[DATA_KEY_RECORD_ID_COUNTER] = counter
        # Sync with "self.remove" function
        self.__json_data[DATA_KEY_DATA][str(counter)] = \
                (title, name, password, notes)
        return counter

    def remove(self, _id):
        # FYI : _id given by table widget as integer. and json data saved in string.
        self.__json_data[DATA_KEY_DATA].pop(str(_id))
        print("Removed:", _id)

    def update(self, _id, title, name, password, notes):
        self.__json_data[DATA_KEY_DATA][_id] = (title, name, password, notes)
        print("Updated", _id, title, name, password, notes)

    def get_password(self, _id):
        return self.__json_data[DATA_KEY_DATA][_id][2]

    def get_data(self):
        result_data = []
        for record_id, record in self.__json_data[DATA_KEY_DATA].items():
            record = list(record) # make copy of record
            record[2] = "***" # hide actual password
            result_data.append((record_id, *record))
        return result_data

    def close(self):
        data = str(self.__json_data).encode('utf-8')
        data = Fernet(self.key).encrypt(data)
        with open(DATA_FILE, mode="wb") as _out:
            _out.write(data)
