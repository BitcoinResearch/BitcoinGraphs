__author__ = 'Sam'

import pymysql
emptyList = ['']
conn = pymysql.Connect(host='10.42.72.21', port=3306, user='root', passwd='bitcoin', db='bitcoin', autocommit=True)
cur = conn.cursor()
print("Connected to TESTDB")


def getAllHoursFromExchangeRange(exchange, minTime, maxTime):
    """Get all hours from an exchange between a range of two dates"""
    cur.execute("SELECT average, standard_deviation, trade_json FROM trades_hour_analysis "
                "WHERE exchange_id='"+str(exchange)+"' "
                "AND timestamp BETWEEN '"+str(minTime)+"' AND '"+str(maxTime)+"'")
    data = cur.fetchall()
    return data

def getAllMinutesFromExchangeRange(exchange, minTime, maxTime):
    """Get all minutes from an exchange between a range of two dates"""
    cur.execute("SELECT average, standard_deviation, trade_json FROM trades_minute_analysis "
                "WHERE exchange_id='"+str(exchange)+"' "
                "AND timestamp BETWEEN '"+str(minTime)+"' AND '"+str(maxTime)+"'")
    data = cur.fetchall()
    return data
