import sys
import subprocess
from PyQt6.QtWidgets import QMainWindow, QApplication
from connect_database import ConnectDatabase
from trang_chu_ui import Ui_trang_chu
from ds_sinhvien import ds_sinhvien


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_trang_chu()
        self.ui.setupUi(self)

        # Create a database connection object
        self.db = ConnectDatabase()

        self.diemDanh = self.ui.diemDanh
        self.dsSinhVien = self.ui.dsSinhVien

        # Initialize signal-slot connections
        self.init_signal_slot()

    def init_signal_slot(self):
        self.diemDanh.clicked.connect(self.diemDanhSv)
        self.dsSinhVien.clicked.connect(self.show_ds_sinhvien)


    def diemDanhSv(self):
       subprocess.Popen([sys.executable, 'D:\OpenCv\OpenCv\recognize.py'])

    def show_ds_sinhvien(self):
        self.ds_sinhvien_window = ds_sinhvien()
        self.ds_sinhvien_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Main()
    window.show()

    sys.exit(app.exec())
