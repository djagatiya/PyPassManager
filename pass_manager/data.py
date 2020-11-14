import json
import os
import logging

DATA_FILE = "data_file.json"
DATA_KEY_PASSWORD = "password"
DATA_KEY_RECORD_ID_COUNTER = "record_id_counter"
DATA_KEY_DATA = "data"

def data_file_exists():
    return os.path.exists(DATA_FILE) and os.path.isfile(DATA_FILE)

# TODO: Use logging

class DataManager:

    def __init__(self):
        logging.debug("Initialize DataManager.")
        self.__json_data = {}

    def setup(self, password):
        """
        todo: Imeplemtation is pending....
        """
        self.__json_data = {
                DATA_KEY_PASSWORD: password, 
                DATA_KEY_RECORD_ID_COUNTER: 0, 
                DATA_KEY_DATA: {}
        }
        print("Do Setup:", self.__json_data)

    def login(self, password):
        """
        Load json data if password is correct.
        """
        with open(DATA_FILE, "r") as json_file:
            data = json.load(json_file)
        if data[DATA_KEY_PASSWORD] == password:
            self.__json_data = data
            return True
        return False

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
        if self.__json_data != {}:
            with open(DATA_FILE, "w") as json_data_file:
                json.dump(self.__json_data, json_data_file)
                print("Data saved:", DATA_FILE)
        else:
            print("Empty json not saved.")
