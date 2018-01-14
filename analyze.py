import time
import pymysql

import csv




'''
Kako naredimo query, kjer vzamemo samo vsako n-to (v tem primeru 5.) vrstico:


set @row:=-1;
SELECT Count(*)
FROM
    trip
    INNER JOIN
    (
        SELECT id
        FROM
            (
                SELECT @row:=@row+1 AS rownum, id 
                FROM
                    (
                        SELECT id FROM trip ORDER BY id
                    ) AS sorted
            ) as ranked
        WHERE rownum % 5 = 0
    ) AS subset
        ON subset.id = trip.id
'''




class database_queries:
    def __int__(self):
        pass
    def connect(self):
        conn = None
        while conn is None:
            try:
                # your host(localhost), username, password, database
                conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='tup', passwd='tup',
                                       db='tup_seminarska')

            except Exception as exc:
                print("Neuspesna povezava na podatkovno bazo. Ponovni poskus cez 1s...", exc)
                time.sleep(1)
        return conn


    # How many rows would you like printed. Limit of rows returned in each iteration.
    # rows = how many rows
    # limit = how many rows in each iteration
    def weatherQuery(self, rows, limit):
        connection = self.connect()
        cursor = connection.cursor()

        offset = 0
        iterations = 1
        if rows > limit:
            iterations = int(rows/limit)

        for iterations in range(iterations):
            print('New iteration')
            cursor.execute("SELECT * FROM weather LIMIT %s OFFSET %s", (limit, offset))
            for response in cursor:
                print(response)
            offset += limit


        cursor.close()
        connection.close()



test = database_queries()
test.weatherQuery(1000, 50)