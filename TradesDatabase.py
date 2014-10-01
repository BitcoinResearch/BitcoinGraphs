__author__ = 'Sam'

import pymysql
emptyList = ['']
conn = pymysql.Connect(host='10.42.72.21', port=3306, user='root', passwd='bitcoin', db='bitcoin', autocommit=True)
cur = conn.cursor()
print("Connected")

def getExchangeID(exchangeName):
    """Get an exchange ID from an exchange name"""
    cur.execute("SELECT exchange_id FROM exchanges "
                "WHERE exchange_name='"+str(exchangeName)+"'")
    exchangeID = str(cur.fetchone())
    #print(exchangeID)
    if exchangeID != None:
        exchangeID = exchangeID.strip("(',')")                  #cleaning up the returned data
    #print("tradeAfter: ", exchangeID)
    return exchangeID
