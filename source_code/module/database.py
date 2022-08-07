import pymysql, os, time

class Database:
    def connect(self):
        DB_USER = os.getenv('DB_USER')
        DB_PASSWORD = os.environ.get('DB_PASSWORD')
        DB_HOSTNAME = os.environ.get('DB_HOSTNAME')
        conn = pymysql.connect(host=DB_HOSTNAME, user=DB_USER, password=DB_PASSWORD, database="flask_app", charset='utf8mb4')
        if conn.open is False:
            max_try = 15
            tries = 0
            while conn.open is False:
                if tries < max_try:
                    conn.ping()
                tries +=1
                time.sleep(3)
        return conn

    def read(self, id):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            if id == None:
                cursor.execute("SELECT * FROM phonebook order by name asc")
            else:
                cursor.execute(
                    "SELECT * FROM phonebook where id = %s order by name asc", (id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def insert(self, data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("INSERT INTO phonebook(name,phone,address) VALUES(%s, %s, %s)",
                           (data['name'], data['phone'], data['address'],))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def update(self, id, data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE phonebook set name = %s, phone = %s, address = %s where id = %s",
                           (data['name'], data['phone'], data['address'], id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def delete(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM phonebook where id = %s", (id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()
