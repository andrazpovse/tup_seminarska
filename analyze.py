import time
import pymysql

import matplotlib.pyplot as plt
import datetime
import pandas as pd
import seaborn as sns
import csv




'''
Kako naredimo query, kjer vzamemo samo vsako n-to (v tem primeru 5.) vrstico:

Ne rabimo, je cist ok, ce nardima query po korakih (LIMIT, OFFSET) in hranima vse v pandas objektu


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

    def basicQuery(self, query):
        connection = self.connect()
        df = pd.read_sql(query, con=connection)
        connection.close()
        return df

    def weatherQuery(self, limit, offset = 0):
        '''
        :param limit: How many rows you would like
        :return: Pandas dataframe with rows
        '''
        connection = self.connect()
        # cursor = connection.cursor()

        df = pd.read_sql("SELECT date,events FROM weather LIMIT %(limit)s OFFSET %(offset)s", con=connection,
                         params={"limit":limit, "offset":offset})

        # cursor.close()
        connection.close()
        return df


    def tripsOnEvent(self, event, limit, queryLimitations = '', offset = 0):
        '''
        :param event: Event in which this trip occured. '' = Normal day, 'Rain', 'Fog', ...
        :param queryLimitations: Extra parameters in query. Example 'AND w.date="2013-09-03" '
        :param limit: limit of rows return
        :param offset: offset where limit starts
        :return: Pandas dataframe with information on weather and trip on a day with event = :param event
        '''

        connection = self.connect()
        query = "SELECT w.date, t.duration, t.start_station_name, t.end_station_name, " \
                "t.zip_code FROM weather w INNER JOIN trip t ON w.date = date(t.start_date) " \
                "WHERE w.events=%(event)s " + queryLimitations + "LIMIT %(limit)s OFFSET %(offset)s "
        df = pd.read_sql(query, con=connection, params={"limit":limit, "offset":offset, "event":event})
        connection.close()
        return df




test = database_queries()
'''
query="select DAYOFWEEK(start_date) as 'Dan', AVG(duration) as 'Povprecno trajanje'  FROM trip WHERE duration < 10800 GROUP BY DAYOFWEEK(start_date)"
data = test.basicQuery(query)

data.to_csv("duration_po_dnevih_v_tednu_limit10800", sep='\t')






query="select Count(*) as 'Stevilo izposoj', month(start_date) as 'Mesec'  FROM trip WHERE year(start_date)='2015' GROUP BY month(start_date)"
izposoj_2015 = test.basicQuery(query)

izposoj_2015.to_csv("izposoj_po_mesecih_2015", sep='\t')




query="SELECT w.zip_code , AVG(t.duration) as Povp_trajanje_voznje, w.events FROM " \
      "weather w INNER JOIN trip t ON w.date = date(t.start_date) WHERE " \
      "w.events='Rain' AND t.duration < 10800 GROUP BY w.zip_code"
data = test.basicQuery(query)

data.to_csv("dez", sep='\t')

query="SELECT w.zip_code , AVG(t.duration) as Povp_trajanje_voznje, w.events FROM " \
      "weather w INNER JOIN trip t ON w.date = date(t.start_date) WHERE " \
      "w.events='Fog' AND t.duration < 10800 GROUP BY w.zip_code"
data = test.basicQuery(query)

data.to_csv("fog", sep='\t')


query="SELECT w.zip_code , AVG(t.duration) as Povp_trajanje_voznje, w.events FROM " \
      "weather w INNER JOIN trip t ON w.date = date(t.start_date) WHERE " \
      "w.events='Fog-Rain' AND t.duration < 10800 GROUP BY w.zip_code"
data = test.basicQuery(query)

data.to_csv("fog_rain", sep='\t')

query="SELECT w.zip_code , AVG(t.duration) as Povp_trajanje_voznje, w.events FROM " \
      "weather w INNER JOIN trip t ON w.date = date(t.start_date) WHERE " \
      "w.events='' AND t.duration < 10800 GROUP BY w.zip_code"
data = test.basicQuery(query)

data.to_csv("normal", sep='\t')


dez = pd.read_csv('dez', delimiter='\t')
normal = pd.read_csv('fog', delimiter='\t')
megla = pd.read_csv("fog_rain", delimiter='\t')
megla_dez = pd.read_csv("normal", delimiter='\t')


dez = dez.append(normal.append(megla.append(megla_dez)))
sns.set_style("whitegrid")

fig = sns.barplot(x=dez['zip_code'], y=dez['Povp_trajanje_voznje'], hue=dez['events'])
plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
plt.show()
print(dez)



sns.set()
izposoje_2013 = pd.read_csv('izposoj_po_mesecih_2013', delimiter='\t')
izposoje_2014 = pd.read_csv('izposoj_po_mesecih_2014', delimiter='\t')
izposoje_2015 = pd.read_csv('izposoj_po_mesecih_2015', delimiter='\t')
plt.plot(izposoje_2013['Mesec'], izposoje_2013['Stevilo izposoj'], label='2013')
plt.plot(izposoje_2014['Mesec'], izposoje_2014['Stevilo izposoj'], label='2014')
plt.plot(izposoje_2015['Mesec'], izposoje_2015['Stevilo izposoj'],label='2015')
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12])
plt.legend( ncol=2, loc='upper left');

plt.xlabel('Mesec')
plt.ylabel('Število voženj')

plt.show()
'''

izposoje_teden = pd.read_csv('izposoj_po_dnevih_v_tednu', delimiter='\t')
dolzina_teden = pd.read_csv('duration_po_dnevih_v_tednu_limit10800', delimiter='\t')

sns.set_style("whitegrid")


fig = sns.barplot(x=dolzina_teden['Dan'], y=dolzina_teden['Povprecno trajanje'])


plt.xticks([0,1,2,3,4,5,6], ['ned', 'pon', 'tor', 'sre', 'cet', 'pet', 'sob'])
plt.show()

