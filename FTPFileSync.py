import logging
import sys
from threading import Thread

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog
from ftputil import FTPHost

from main_window import Ui_Window


class Search_Thread(Thread):
    def __init__(self, hostname, username, password):
        super().__init__()
        self.hostname = hostname
        self.username = username
        self.password = password

    def run(self):

        try:
            with FTPHost(self.hostname, self.username, self.password) as ftp:
                for folder in ftp.listdir('.'):
                    log.info('Found remote folder: {}'.format(folder))
        except Exception as e:
            print(e)


class Download_Thread(Thread):
    def __init__(self, hostname, username, password, list_of_folders):
        super().__init__()
        self.hostname = hostname
        self.username = username
        self.password = password
        self.list_of_folders = list_of_folders
        self.list_of_files = []

    def run(self):
        if form.stop_sync is not True:
            for folder in self.list_of_folders:
                log.info('Attempting to retrieve file list from {}'.format(folder))

                try:
                    with FTPHost(self.hostname, self.username, self.password) as ftp:
                        for root, dirs, files in ftp.walk(folder):
                            for file in files:
                                form.list_transfer.addItem(root + '/' + file)
                except Exception as e:
                    log.exception(e)


class List_Handler(logging.Handler):
    """Custom Logging handler that sends logging to the Main Window"""
    def emit(self, record):
        log_entry = self.format(record)
        form.list_log.addItem(log_entry)


class MainForm(QMainWindow, Ui_Window):
    """Main Window"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)


        # Set initial vars
        self.local_path = ''
        self.remote_folders = []
        self.stop_sync = False

        # Set custom logging handler
        self.list_handler = List_Handler()
        self.list_handler.setFormatter(log_formatter)
        log.addHandler(self.list_handler)

        # Connect button clicks to actions
        self.action_download_path.triggered.connect(self.download_path_click)
        self.action_load_settings.triggered.connect(self.load_settings_click)
        self.action_save_settings.triggered.connect(self.save_settings_click)
        self.action_find_remote_folders.triggered.connect(self.find_folders_click)
        self.action_add_folder.triggered.connect(self.add_folder_click)
        self.action_sync.triggered.connect(self.sync_click)

    def download_path_click(self):

        self.local_path = QFileDialog.getExistingDirectory()
        log.debug('Download path set: {}'.format(self.local_path))

    def load_settings_click(self):
        log.debug('Getting path from user....')
        path = QFileDialog.getOpenFileName(filter=('FTP Config File (*.ftc)'))
        log.debug('Attempting to load the settings file')

        try:
            with open(path[0], 'r') as file_handler:
                self.input_hostname.setText(file_handler.readline().rstrip('\n'))
                self.input_username.setText(file_handler.readline().rstrip('\n'))
                self.input_password.setText(file_handler.readline().rstrip('\n'))
                log.debug('Loaded settings from {}'.format(path[0]))

        except Exception as e:
            log.exception(e)

    def save_settings_click(self):
        log.debug('Getting path from user....')
        path = QFileDialog.getSaveFileName(filter=('FTP Config File (*.ftc)'))
        log.debug('Attempting to save settings file')

        try:
            with open(path[0], 'w') as file_handler:
                file_handler.write(self.input_hostname.text() + '\n')
                file_handler.write(self.input_username.text() + '\n')
                file_handler.write(self.input_password.text() + '\n')
                log.debug('Saved settings to {}'.format(path[0]))
        except Exception as e:
            log.exception(e)

    def find_folders_click(self):

        new_thread = Search_Thread(self.input_hostname.text(), self.input_username.text(), self.input_password.text())
        new_thread.start()

    def add_folder_click(self):

        text, ok = QInputDialog.getText(self, 'Remote Folder', 'Enter the name of a remote folder to add:')

        if ok:

            try:
                with FTPHost(self.input_hostname.text(), self.input_username.text(), self.input_password.text()) as ftp:
                    if ftp.path.exists(text) is True:
                        self.remote_folders.append(text)
                        log.info('Added {} to the list of remote folders to search.'.format(text))
                    else:
                        log.warning('{} does not exist on {}'.format(text, self.input_hostname.text()))
            except Exception as e:
                log.debug(e)

    def sync_click(self):
        new_thread = Download_Thread(self.input_hostname.text(), self.input_username.text(), self.input_password.text(),
                                     self.remote_folders)
        new_thread.start()



if __name__ == '__main__':

    # Logging

    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s','%c')
    console_handler.setFormatter(log_formatter)
    log.addHandler(console_handler)

    # Start the Aplication
    app = QApplication(sys.argv)
    # Create the main form
    form = MainForm()
    # Show the main form
    form.show()

    app.exec_()





