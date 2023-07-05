import sqlite3
class controlDB:
    # Kết nối đến cơ sở dữ liệu SQLite
    conn = sqlite3.connect('Test.db')
    # Tạo đối tượng cursor để thao tác với cơ sở dữ liệu
    cursor = conn.cursor()
    # Thực thi các truy vấn SQL
    #cursor.execute("SELECT * FROM Test")

    def createDB(self):
        self.cursor.execute('''CREATE TABLE Test
                  (IP TEXT, Port INTEGER, Domain TEXT, URL TEXT)''')
    
        self.conn.close()


    def printTest(self):    
        self.cursor.execute("SELECT * FROM Test")
        # Lấy tất cả các kết quả trả về từ truy vấn
        result = self.cursor.fetchall()
        # In kết quả
        for row in result:
            print(row)

    def addValue(self,data):

        # Thêm dữ liệu từ từ điển vào bảng 'Test'
        self.cursor.execute("INSERT INTO Test (ip, port, domain, url) VALUES (?, ?, ?, ?)",
               (data['IP'], data['Port'], data['Domain'], data['URL']))
    # Lưu thay đổi vào cơ sở dữ liệu
        self.conn.commit()
        self.conn.close()
