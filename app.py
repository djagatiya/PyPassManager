from PySide2 import QtWidgets

from pass_manager.gui import MainWindow

import logging
import sys

# ------------- SETUP LOGGER -------------

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s - [%(filename)s:%(lineno)s - %(funcName)20.20s ] %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

logging.debug("Logger setup done.")

# ---------------------------------------

if __name__ == "__main__":

    print("Args:", sys.argv)

    app = QtWidgets.QApplication([])
    main_win = MainWindow(sys.argv[1])
    main_win.resize(800, 400)
    main_win.show()
    app.exec_()

    pass
