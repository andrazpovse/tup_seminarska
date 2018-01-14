import time
import pymysql

import csv


class database_queries:
    def __int__(self):
        pass
    def connect(self):
        conn = None
        while conn is None:
            try:
                conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='tup', passwd='tup',
                                       db='tup_seminarska')

            except Exception as exc:
                print("Neuspesna povezava na podatkovno bazo. Ponovni poskus cez 1s...", exc)
                time.sleep(1)
        return conn



    def weatherQuery(self):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("SELECT date FROM weather")

        for response in cursor:
            print(response)


        cursor.close()
        connection.close()



test = database_queries()
test.weatherQuery()