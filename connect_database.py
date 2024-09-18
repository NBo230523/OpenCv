import mysql.connector


class ConnectDatabase:
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.database = 'ds_sinhvien'
        self.user = 'root'
        self.password = ''
        self.dbname = 'ds_sinhvien'
        self.con = None
        self.cursor = None

    def connect_db(self):
        self.con = mysql.connector.connect(
            host=self.host,
            port=self.port,
            database=self.dbname,
            user=self.user,
            password=self.password
        )

        self.cursor = self.con.cursor(dictionary=True)

    def add_sinhvien(self, masv, hoten, diachi, sdt, anhsinhvien):
        self.connect_db()

        sql = f"""
        INSERT INTO `sinhvien`(`MASV`, `HOTEN`, `DIACHI`, `SDT`, `ANHSINHVIEN`) VALUES ({masv},'{hoten}','{diachi}',{sdt},'{anhsinhvien}')
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def update_sinhvien(self, masv, hoten, diachi, sdt, anhsinhvien):
        self.connect_db()

        sql = f"""
        UPDATE `sinhvien` SET `HOTEN`='{hoten}',`DIACHI`='{diachi}',`SDT`={sdt},`ANHSINHVIEN`='{anhsinhvien}' WHERE `MASV`={masv}
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def delete_sinhvien(self, masv):
        self.connect_db()
        sql = f"""
        DELETE FROM `sinhvien` WHERE `MASV`={masv}
    """
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def search_sinhvien(self, masv=None, hoten=None, diachi=None, sdt=None, anhsinhvien=None):
        self.connect_db()
        condition = ""
        if masv:
            condition += f" AND masv LIKE '%{masv}%' "
        if hoten:
            condition += f" AND hoten LIKE '%{hoten}%' "
        if diachi:
            condition += f" AND diachi LIKE '%{diachi}%' "
        if sdt:
            condition += f" AND sdt LIKE '%{sdt}%' "
        if anhsinhvien:
            condition += f" AND anhsinhvien LIKE '%{anhsinhvien}%' "

        sql = f"SELECT * FROM `sinhvien` WHERE 1"
        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql + condition)
            result = self.cursor.fetchall()
            return result
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()

    def get_all_sinhvien(self):
        self.connect_db()
        sql = f"Select * from sinhvien"
        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as E:
            self.con.rollback()
            return E
        finally:
            self.con.close()