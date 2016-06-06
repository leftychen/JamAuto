from temp.Leftychen.sqldbconnector.dbConnector import SqlDBConnector

conn = SqlDBConnector("jamtest", "jamtest", "jamauto_stockmkt_data")
df = conn.get_HS300_Current_Data(('2010-04-16', '2010-05-16'))
print(df.head(5))
conn.close()