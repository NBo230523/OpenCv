import sys
from PyQt6.QtWidgets import QApplication, QPushButton, QMessageBox, QTableWidgetItem, QMainWindow
from PyQt6.QtGui import  QPixmap

from ds_sinhvien_ui import Ui_ds_sinhvien
from connect_database import ConnectDatabase as ConnectDB


class ds_sinhvien(QMainWindow):

    def __init__(self):
        super().__init__()

        # Init the UI from a separate UI file
        self.ui = Ui_ds_sinhvien()
        self.ui.setupUi(self)

        # Create a database connection object
        self.db = ConnectDB()

        # Connect UI elements to class variables
        self.soLuongRow = self.ui.soLuongRow

        self.maSv = self.ui.maSinhVien
        self.hoTen = self.ui.hoVaTen
        self.diaChi = self.ui.diaChi
        self.sdt = self.ui.soDienThoai
        self.anhSinhVien = self.ui.anhSinhVien


        self.themBtn = self.ui.them
        self.suaBtn = self.ui.sua
        self.timKiemBtn = self.ui.timKiem
        self.lamTrongBtn = self.ui.lamTrong
        self.xoaBtn = self.ui.xoa
        self.image_label = self.ui.image_label

        self.result_table = self.ui.tableWidget
        self.result_table.setSortingEnabled(False)
        self.buttons_list = self.ui.groupBox_2.findChildren(QPushButton)

        # double click table
        self.result_table.mouseDoubleClickEvent = self.custom_mouse_double_click

        # Initialize signal-slot connections
        self.init_signal_slot()

        # Populate the initial data in the table in the combo-boxes
        self.search_sinhvien(True)

    def init_signal_slot(self):
        # connect buttons to their respective functions
        self.themBtn.clicked.connect(self.add_sinhvien)
        self.suaBtn.clicked.connect(self.update_sinhvien)
        self.lamTrongBtn.clicked.connect(self.clear_data)
        self.timKiemBtn.clicked.connect(self.search_sinhvien)
        self.xoaBtn.clicked.connect(self.delete_sinhvien)

    # Result table double click
    def custom_mouse_double_click(self, event):
        self.select_sinhvien_info()

    def attach_image(self, path: str):
        mypmap = QPixmap(path)
        self.image_label.setPixmap(mypmap)
        self.image_label.setMask(mypmap.mask())

    def add_sinhvien(self):
        self.disable_buttons()
        sinhvien_info = self.get_sinhvien_info()

        if sinhvien_info["maSv"] and sinhvien_info["hoTen"] and sinhvien_info["diaChi"] and sinhvien_info["sdt"] and sinhvien_info["anhSinhVien"]:
            add_result = self.db.add_sinhvien(masv = sinhvien_info["maSv"],
                                            hoten = sinhvien_info["hoTen"],
                                            diachi = sinhvien_info["diaChi"],
                                            sdt = sinhvien_info["sdt"],
                                            anhsinhvien = sinhvien_info["anhSinhVien"])

            if add_result:
                QMessageBox.information(self, "Lỗi", f"Thêm thất bại: {add_result}. Vui lòng kiểm tra lại thông tin.", QMessageBox.StandardButton.Ok)
            else:
                QMessageBox.information(self, "Successful", "Thêm thành công.", QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.information(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin.", QMessageBox.StandardButton.Ok)

        self.search_sinhvien(True)
        self.enable_buttons()

    def get_sinhvien_info(self):
        # Lay thong tin sach tu cac Input

        maSv = self.maSv.text().strip()
        hoTen = self.hoTen.text().strip()
        diaChi = self.diaChi.text().strip()
        sdt = self.sdt.text().strip()
        anhSinhVien = self.anhSinhVien.text().strip()

        sinhVienInfo = {
            "maSv": maSv,
            "hoTen": hoTen,
            "diaChi": diaChi,
            "sdt": sdt,
            "anhSinhVien": anhSinhVien
        }

        return sinhVienInfo

    def update_sinhvien(self):
        self.disable_buttons()
        new_sinhvien_info = self.get_sinhvien_info()

        if new_sinhvien_info["maSv"] and new_sinhvien_info["hoTen"] and new_sinhvien_info["diaChi"] and new_sinhvien_info["sdt"] and new_sinhvien_info["anhSinhVien"]:
            update_result = self.db.update_sinhvien(masv = new_sinhvien_info["maSv"],
                                            hoten = new_sinhvien_info["hoTen"],
                                            diachi = new_sinhvien_info["diaChi"],
                                            sdt = new_sinhvien_info["sdt"],
                                            anhsinhvien = new_sinhvien_info["anhSinhVien"])

            if update_result:
                QMessageBox.information(self, "Lỗi", f"Sửa thất bại: {update_result}, Vui lòng kiểm tra lại thông tin.", QMessageBox.StandardButton.Ok)
            else:
                QMessageBox.information(self, "Successful", "Sửa thành công.", QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.information(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin.", QMessageBox.StandardButton.Ok)

        self.search_sinhvien(True)
        self.enable_buttons()

    def delete_sinhvien(self):
        # Function to delete student information
        select_row = self.result_table.currentRow()
        if select_row != -1:
            selected_option = QMessageBox.warning(self, "Cảnh báo", "Bạn có chắc chắn muốn xóa?",
                                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

            if selected_option == QMessageBox.StandardButton.Yes:
                sinhvien_id = self.result_table.item(
                    select_row, 0).text().strip()

                delete_result = self.db.delete_sinhvien(int(sinhvien_id))
                QMessageBox.information(self, "Successful", "Xóa sinh viên thành công.", QMessageBox.StandardButton.Ok)

                if not delete_result:
                    self.search_sinhvien(True)
                else:
                    QMessageBox.information(self, "Cảnh báo", f"Lỗi: {delete_result}. Vui lòng thử lại.",
                                            QMessageBox.StandardButton.Ok)

        else:
            QMessageBox.information(self, "Cảnh báo", "Vui lòng một dòng trên bảng.", QMessageBox.StandardButton.Ok)

    def select_sinhvien_info(self):
        # Function to select and populate student information in the form
        select_row = self.result_table.currentRow()
        if select_row != -1:
            maSv = self.result_table.item(select_row, 0).text().strip()
            hoTen = self.result_table.item(select_row, 1).text().strip()
            diaChi = self.result_table.item(select_row, 2).text().strip()
            sdt = self.result_table.item(select_row, 3).text().strip()
            anhSinhVien = self.result_table.item(select_row, 4).text().strip()

            self.attach_image(anhSinhVien)

            self.maSv.setText(maSv)
            self.hoTen.setText(hoTen)
            self.diaChi.setText(diaChi)
            self.sdt.setText(sdt)
            self.anhSinhVien.setText(anhSinhVien)
        else:
            QMessageBox.information(self, "Cảnh báo", "Vui lòng chọn một dòng trên bảng.",
                                    QMessageBox.StandardButton.Ok)

    def clear_data(self):
        self.maSv.clear()
        self.hoTen.clear()
        self.diaChi.clear()
        self.sdt.clear()
        self.anhSinhVien.clear()
        self.attach_image("D:/Img TTNT/placeholder.jpg")
        self.search_sinhvien(True)

    def search_sinhvien(self, emptySearch: bool):

        if not emptySearch:
            sinhvien_info = self.get_sinhvien_info() 
            sinhvien_result = self.db.search_sinhvien(
                masv=sinhvien_info["maSv"],
                hoten=sinhvien_info["hoTen"],
                diachi=sinhvien_info["diaChi"],
                sdt=sinhvien_info["sdt"],
                anhsinhvien=sinhvien_info["anhSinhVien"]
            )

            if type(sinhvien_result) == list:
                self.show_data(sinhvien_result)
            else:
                QMessageBox.information(self, "Lỗi", f"Lỗi: {sinhvien_result}", QMessageBox.StandardButton.Ok)
                return
        else:
            sinhvien_result = self.db.search_sinhvien()
            if type(sinhvien_result) == list:
                self.show_data(sinhvien_result)
            else:
                QMessageBox.information(self, "Lỗi", f"Lỗi: {sinhvien_result}",
                                        QMessageBox.StandardButton.Ok)
                return

    def show_data(self, sinhvien_data_list):
        if sinhvien_data_list:
            self.result_table.setRowCount(0)
            self.result_table.setRowCount(len(sinhvien_data_list))
            self.soLuongRow.setText("Số lượng sinh viên: " + str(len(sinhvien_data_list)))

            for row, info in enumerate(sinhvien_data_list):
                info_list = [
                    info["MASV"],
                    info["HOTEN"],
                    info["DIACHI"],
                    info["SDT"],
                    info["ANHSINHVIEN"]
                ]

                for column, item in enumerate(info_list):
                    cell_item = QTableWidgetItem(str(item))
                    self.result_table.setItem(row, column, cell_item)
        else:
            self.result_table.setRowCount(0)
            return

    def disable_buttons(self):
        for btn in self.buttons_list:
            btn.setProperty('enabled', False)

    def enable_buttons(self):
        for btn in self.buttons_list:
            btn.setProperty('enabled', True)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = ds_sinhvien()
    window.show()

    sys.exit(app.exec())
