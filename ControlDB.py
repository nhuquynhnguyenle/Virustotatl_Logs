from log_management import log_management

class controlDB:
    
    def createTable(self, cursor):
        try:
            cursor.execute('''CREATE TABLE IF NOT EXISTS Test
                          (IP TEXT, Port INTEGER, Domain TEXT, URL TEXT, Score INTEGER)''')
            print("\nTable created successfully")
        except Exception as e:
            print("Error creating table:", str(e))


    def printTest(self,cursor):    
        cursor.execute("SELECT * FROM Test")
        result = self.cursor.fetchall()
        for row in result:
            print(row)

    def addValue(self, data, score, cursor):
        try:
            cursor.execute("INSERT INTO Test (IP, Port, Domain, URL, Score) VALUES (?, ?, ?, ?, ?)",
                       (data.IP, data.Port, data.Domain, data.URL, score))
        except Exception as e:
            print("Error adding value:", str(e))



