import logging

from PySide2 import QtWidgets

from pass_manager.data import DataManager

class Login(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        layout = QtWidgets.QHBoxLayout()
        self.pass_enter = QtWidgets.QLineEdit()
        layout.addWidget(self.pass_enter)
        self.login_btn = QtWidgets.QPushButton(text="Login")
        layout.addWidget(self.login_btn)
        self.setLayout(layout)


class Home(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        # setup table
        table = QtWidgets.QTableWidget()
        self.table = table

        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Id", "Title", "UserName", "Password", "Notes"])

        for row in manager.get_data():
            self.append_row(row)

        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.resizeColumnsToContents()

        # button panel
        button_widget_panel = QtWidgets.QWidget()
        button_widget_layout = QtWidgets.QHBoxLayout()

        self.add_button = QtWidgets.QPushButton(text="Add")
        self.edit_button = QtWidgets.QPushButton(text="Edit")
        self.delete_button = QtWidgets.QPushButton(text="Delete")

        button_widget_layout.addWidget(self.add_button)
        button_widget_layout.addWidget(self.edit_button)
        button_widget_layout.addWidget(self.delete_button)
        button_widget_layout.addStretch()

        button_widget_panel.setLayout(button_widget_layout)

        # Root Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(button_widget_panel)
        self.setLayout(layout)

    def append_row(self, items):
        row_index = self.table.rowCount()
        self.table.insertRow(row_index)
        self.set_items(row_index, items)

    def set_items(self, row_index, items):
        for i, r in enumerate(items):
            self.table.setItem(row_index, i, QtWidgets.QTableWidgetItem(r))


class Form(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        form_layout = QtWidgets.QFormLayout()

        
        self.title_edit = QtWidgets.QLineEdit()
        form_layout.addRow(QtWidgets.QLabel("Title"), self.title_edit)

        self.user_name_edit = QtWidgets.QLineEdit()
        form_layout.addRow(QtWidgets.QLabel("UserName"), self.user_name_edit)

        self.pass_word_edit = QtWidgets.QLineEdit()
        form_layout.addRow(QtWidgets.QLabel("Password"), self.pass_word_edit)

        self.note_edit = QtWidgets.QLineEdit()
        form_layout.addRow(QtWidgets.QLabel("Note"), self.note_edit)

        self.save_btn = QtWidgets.QPushButton("Save")
        self.close_btn = QtWidgets.QPushButton("Close")
        self.reset_btn = QtWidgets.QPushButton("Reset")

        form_layout.addRow(self.save_btn, self.close_btn)
        form_layout.addRow(self.reset_btn)

        self.setLayout(form_layout)

# Data manager
# TODO : REPLACE with "sqlite"
manager = DataManager()
manager.login("1234")


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.stacked = QtWidgets.QStackedWidget()

        self.w_login = Login()
        self.w_home = Home()
        self.w_form = Form()

        self.stacked.addWidget(self.w_login)
        self.stacked.addWidget(self.w_home)
        self.stacked.addWidget(self.w_form)

        self.setCentralWidget(self.stacked)

        # login event
        self.w_login.login_btn.clicked.connect(self.on_login)

        # home event
        self.w_home.add_button.clicked.connect(self.show_form)
        self.w_home.delete_button.clicked.connect(self.delete_click)
        self.w_home.edit_button.clicked.connect(self.edit_click)

        # form event
        self.w_form.reset_btn.clicked.connect(self.reset_form)
        self.w_form.close_btn.clicked.connect(self.reset_form_and_close)
        self.w_form.save_btn.clicked.connect(self.save_fun)

        # this property will handle single form for edit and save
        self.row_index = -1

    def on_login(self):
        if self.w_login.pass_enter.text() == "master":
            self.show_home()
        else:
            box = QtWidgets.QMessageBox(icon=QtWidgets.QMessageBox.Critical, text="Login error.")
            box.exec_()
            print("Login Failed..")

    def reset_form(self):
        self.row_index = -1
        self.w_form.title_edit.setText("")
        self.w_form.user_name_edit.setText("")
        self.w_form.pass_word_edit.setText("")
        self.w_form.note_edit.setText("")

    def reset_form_and_close(self):
        self.reset_form()
        self.show_home()

    def save_fun(self):
        title = self.w_form.title_edit.text()
        username = self.w_form.user_name_edit.text()
        password = self.w_form.pass_word_edit.text()
        note = self.w_form.note_edit.text()
        if self.row_index == -1:
            _id = manager.add(title, username, password, note)
            logging.info(f"{_id} generated while saving record.")
            self.w_home.append_row([str(_id), *[title, username, "***", note]])

        else:        
            fetch_id = self.w_home.table.item(self.row_index, 0).text()
            update_data =  [fetch_id, title, username, password, note]
            
            logging.info(f"Going to update: {update_data}")
            
            # update to data manager
            manager.update(*update_data)
            
            # update to table widget
            update_data[3] = "***"
            self.w_home.set_items(self.row_index, update_data)

        # reset at the end of the operation
        self.row_index = -1

    def show_login(self):
        # TODO: No need to show explicitly
        self.stacked.setCurrentIndex(0)

    def show_home(self):
        self.stacked.setCurrentIndex(1)

    def show_form(self):
        self.stacked.setCurrentIndex(2)

    def add_click(self):
        self.show_form()

    def edit_click(self):
        # table.setHorizontalHeaderLabels(["Id", "Title", "UserName", "Password", "Notes"])
        self.row_index = self.w_home.table.currentRow()
        row = self.row_index
        fetch_id = self.w_home.table.item(self.row_index, 0).text()
        fetch_title = self.w_home.table.item(row, 1).text()
        fetch_username = self.w_home.table.item(row, 2).text()
        fetch_password = manager.get_password(fetch_id)
        fetch_notes = self.w_home.table.item(row, 4).text()

        logging.info(f"Fetch: {row}, {fetch_title}, "  \
                + f"{fetch_username}, {fetch_password}, {fetch_notes}")

        self.w_form.title_edit.setText(fetch_title)
        self.w_form.user_name_edit.setText(fetch_username)
        self.w_form.pass_word_edit.setText(fetch_password)
        self.w_form.note_edit.setText(fetch_notes)
        
        self.show_form()

    def find_selected_row_and_selected_id(self):
        table = self.w_home.table

        # find selected rows
        rows = table.selectionModel().selectedRows()
        logging.info(f"Selected Rows: {rows}")

        # TODO: check len
        row = rows[0]
        selected_id = table.model().data(row)
        logging.info(f"{selected_id}")
        
        return row, selected_id

    def delete_click(self):
        logging.info("Requesting for delete row.")

        row, selected_id = self.find_selected_row_and_selected_id()

        # remove row from table widget
        self.w_home.table.removeRow(row.row())

        # remove from data manager
        manager.remove(selected_id)
        
        pass

    def closeEvent(self, event):
        print("Close event")
        super().closeEvent(event)
        manager.close()
