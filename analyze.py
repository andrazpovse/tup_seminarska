import time
import pymysql

import matplotlib.pyplot as plt
import datetime
import pandas as pd
import seaborn as sns
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



    def weatherQuery(self, limit):
        '''
        :param limit: How many rows you would like
        :return: Pandas dataframe with rows
        '''
        connection = self.connect()
        # cursor = connection.cursor()

        df = pd.read_sql("SELECT date,events FROM weather LIMIT %(limit)s", con=connection, params={"limit":limit})

        # cursor.close()
        connection.close()
        return df





test = database_queries()
data = test.weatherQuery(100)
print(data)





