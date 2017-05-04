import sys
import logging
from main_window import Ui_Window
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog


class List_Handler(logging.Handler):
    """Custom Logging handler that sends logging to the Main Window"""
    def emit(self, record):
        log_entry = self.format(record)
        form.list_log.addItem(log_entry)
        form.list_log.scrollToBottom()



class MainForm(QMainWindow, Ui_Window):
    """Main Window"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Set initial vars
        self.local_path = ''

        # Set custom logging handler
        self.list_handler = List_Handler()
        self.list_handler.setFormatter(log_formatter)
        log.addHandler(self.list_handler)

        # Connect button clicks to actions
        self.action_download_path.triggered.connect(self.download_path_click)
        self.action_load_settings.triggered.connect(self.load_settings_click)
        self.action_save_settings.triggered.connect(self.save_settings_click)
        self.action_find_remote_folders.triggered.connect(self.find_folders_click)
        self.action_sync.triggered.connect(self.sync_click)




    def download_path_click(self):

        self.path = QFileDialog.getExistingDirectory()
        log.debug('Download path set: {}'.format(self.path))

    def load_settings_click(self):
        log.debug('Loaded Settings')

    def save_settings_click(self):
        pass

    def find_folders_click(self):
        pass

    def sync_click(self):
        pass

    def update_bar_progress(self):
        pass





if __name__ == '__main__':

    # Logging

    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s','%c')
    console_handler.setFormatter(log_formatter)
    log.addHandler(console_handler)

    log.debug('log started')

    # Start the Aplication
    app = QApplication(sys.argv)
    # Create the main form
    form = MainForm()
    # Show the main form
    form.show()

    app.exec_()





