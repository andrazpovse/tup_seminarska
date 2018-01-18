import time
import pymysql

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime
import pandas as pd
import seaborn as sns
import csv
import numpy as np



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
                conn = pymysql.connect(unix_socket='/var/run/mysqld/mysqld.sock', user='root', passwd='ep',
                                       db='sf_bay_bike_share')

            except Exception as exc:
                print("Neuspesna povezava na podatkovno bazo. Ponovni poskus cez 1s...", exc)
                time.sleep(1)
        return conn



    def scatter_query1(self):
        connection = self.connect()
        # cursor = connection.cursor()
        # 94107, 94105
        df = pd.read_sql("SELECT day1, SUM(diff) as diff FROM day_to_day_diff WHERE YEAR(day1) = 2014 GROUP BY day1, day2", con=connection)

        # cursor.close()
        connection.close()
        return df

    def scatter_query2(self):
        connection = self.connect()
        # cursor = connection.cursor()
        # 94107, 94105
        df = pd.read_sql("SELECT day1 as 'Datum', SUM(diff) as 'Razlika' FROM day_to_day_diff WHERE YEAR(day1) = 2014 AND zip_code IN ('94107', '94105') GROUP BY day1, day2", con=connection)

        # cursor.close()
        connection.close()
        return df



test = database_queries()
data = test.scatter_query1()

sns.swarmplot(x="Datum", y="Razlika", data=data, size=3)

dates = [str(item) for sublist in data.as_matrix(columns=['day1']) for item in sublist]
diffs = [item for sublist in data.as_matrix(columns=['diff']) for item in sublist]
nsplit = 52
weeks = np.array_split(diffs, nsplit)
week_stds = pd.DataFrame({
    'Teden': range(1,nsplit + 1),
    'Standardni odklon': [np.std(week) for week in weeks]
})

# sns.swarmplot(x="Teden", y="Standardni odklon", data=week_stds, size=5)
sns.lmplot(x="Teden", y="Standardni odklon", data=week_stds, order=3)
# fig, ax = plt.subplots()
# ax.plot(dates,diffs)
# ax.set_xticks(ax.get_xticks()[::50])

#plt.plot(dates, diffs, 'ko')
#plt.xticks(np.arange(10))
plt.show()
