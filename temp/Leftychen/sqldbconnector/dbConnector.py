import pymysql as sql
import pymysql.cursors
import pandas as pd
import numpy as np
import time
class SqlDBConnector:
    '''
    Author: leftychen
    Description:
        This is an interface to connect to our SQL DB, based on schemas and tables
        we have.

        Currently, we just data of HS300 futures.

        You need to start with a constructor and provide your username, password and DataBase Name
        and then simply call get_HS300_Current_Data or get_HS300_Future_Data function to get the data from our DB
        Only you need to provide the timestamp in tuple or list format with start time and end time
        eg.['2014-04-15', '2014-04-30']
        if you did not provide timestamp, the function will return whole content of tables which is not recommended

    Return: Pandas.DataFrame
    '''
# Constructor
    def __init__(self,user, pwd, db):
        self.__host = '174.128.226.174'
        self.__user = user
        self.__pwd = pwd
        self.__db = db
        self.__HS300_curr_table = 'stockmkt_cn_if00'
        self.__HS300_future_table = 'stockmkt_cn_if01'
        #Connect to DB
        self.__connection = sql.connect(host = self.__host,
                                      user = self.__user,
                                      password = self.__pwd,
                                      db = self.__db,
                                      cursorclass = pymysql.cursors.SSCursor
        )

        self.__cursor = self.__connection.cursor()

#Function of Get the HS300 Index future of current month
    def get_HS300_Current_Data(self, timestamp = None):
        df = None
        if(self.__db != 'jamauto_stockmkt_data'):
            raise Exception("Please use stock market DataBase...")
            return
        try:
            query = None
            if(timestamp == None):
                query = 'SELECT * FROM ' + self.__HS300_curr_table
            else:
                query = 'SElECT * FROM ' + self.__HS300_curr_table + \
                        ' WHERE Date BETWEEN ' + "'" + timestamp[0] + "'"\
                        ' AND ' + "'" + timestamp[1] + "'"
            self.__cursor.execute(query)
            date = []
            data = []

            for row in self.__cursor:
                date.append(row[0])
                temp = []
                temp.append(row[1])
                temp.append(row[2])
                temp.append(row[3])
                temp.append(row[4])
                temp.append(row[5])
                temp.append(row[6])
                temp.append(row[7])
                data.append(temp)

            date = np.array(date)
            data = np.array(data,dtype='float')
            df = pd.DataFrame(index = date, data = data,
                              columns =['Open', 'High', 'Low', 'Close','Volume', 'VolumeAmount', 'Position'])

        except Exception as e:
            raise e
            return None

        finally:
            return df


#Function of get the HS300 Future of next month
    def get_HS300_Future_Data(self, timestamp = None):
        df = None
        if (self.__db != 'jamauto_stockmkt_data'):
            raise Exception("Please use stock market DataBase...")

        try:
            query = None
            if (timestamp == None):
                query = 'SELECT * FROM ' + self.__HS300_future_table
            else:
                query = 'SElECT * FROM ' + self.__HS300_future_table + \
                        ' WHERE Date BETWEEN ' + "'" + timestamp[0] + "'" \
                        ' AND ' + "'" + timestamp[1] + "'"

            self.__cursor.execute(query)
            date = []
            data = []
            for row in self.__cursor:
                date.append(row[0])
                temp = []
                temp.append(row[1])
                temp.append(row[2])
                temp.append(row[3])
                temp.append(row[4])
                temp.append(row[5])
                temp.append(row[6])
                temp.append(row[7])
                data.append(temp)

            date = np.array(date)
            data = np.array(data, dtype='float')
            df = pd.DataFrame(index=date, data=data,
                              columns=['Open', 'High', 'Low', 'Close', 'Volume', 'VolumeAmount', 'Position'])


        except Exception as e:
            raise e


        finally:
            return df

# Close the database
    def close(self):
        self.__cursor.close()
        self.__connection.close()





