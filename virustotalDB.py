import sqlite3
from log_management import log_management

class controlDB:
    conn = sqlite3.connect('Test.db')
    cursor = conn.cursor()

    def createTable(self):
        self.cursor.execute('''CREATE TABLE Test
                  (IP TEXT, Port INTEGER, Domain TEXT, URL TEXT,Score int)''')

        #self.conn.close()

    def printTest(self):    
        self.cursor.execute("SELECT * FROM Test")
        result = self.cursor.fetchall()
        for row in result:
            print(row)

    def addValue(self,data,score):
        self.cursor.execute("INSERT INTO Test (IP, Port, Domain, URL,Score) VALUES (?, ?, ?, ?,?)",
               (data.IP ,data.Port, data.Domain, data.URL,score))
        self.conn.commit()
        #self.conn.close()


