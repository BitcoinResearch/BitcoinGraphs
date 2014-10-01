#PURPOSE OF THIS FILE Main.py: Choose the time range and exchanges you want to compare, then run Main.py..
#                             ..and it will display minutely / hourly volatility
#PACKAGES REQUIRED: datetime, calendar, numpy, pymysql, ast, matplotlib

__author__ = 'Sam'

import PlotGraph
import AnalysisDatabase as analysis_db
import TradesDatabase as trades_db
import ast
import numpy as np
import datetime
import calendar

#choose the minimum & maximum date/time
#format:    Y    M    D   Hr  Min  Sec
minTime = (2014, 9,  1,  0,   0,   0)
maxTime = (2014, 9,  18,  12,  0,   0)

#Available exchanges, this is just used as an exchange name reference
available = ["1coinUSD", "anxhkUSD", "anxhkEUR", "anxhkGBP", "bitbayUSD", "bitbayEUR", "btcdeEUR", "bitcurexEUR",
             "bitfloorUSD", "bitfinexUSD", "bitstampUSD", "btceUSD", "btceEUR", "coinfloorGBP", "cotrUSD", "hitbtcUSD",
             "hitbtcEUR", "itbitUSD", "itbitEUR", "krakenUSD", "krakenEUR", "lakeUSD", "localbtcUSD", "localbtcEUR",
             "localbtcGBP", "rippleUSD", "rippleEUR", "zyadoEUR"]

#Enter the exchange names you want to compare here
exchanges = ["btcdeEUR"]#, "anxhkEUR", "btceEUR"]

#Generate charts for both minutely data, and hourly data? True = Yes, False = No
MINUTELY = True
HOURLY = True

if __name__ == "__main__":

    #for exchange in range(0, len(available)):
    #    print "\n"+str(exchange+1)+": "+available[exchange]+""
    #    print analysis_db.getLastTimestampMinute(exchange+1)
    #    print analysis_db.getLastTimestampHour(exchange+1)
    #exit()

    #These 4 lines convert the dates you entered above into timestamps
    time1 = calendar.timegm(minTime)
    time2 = calendar.timegm(maxTime)
    minDate = datetime.datetime.utcfromtimestamp(time1)
    maxDate = datetime.datetime.utcfromtimestamp(time2)

    allHourlyData = []
    allMinutelyData = []

    #Calculate per-minute graphs
    if MINUTELY == True:
        #for each exchange, retrieve the exchange ID
        for ex in range(len(exchanges)):
            exchangeID = trades_db.getExchangeID(exchanges[ex])
            #retrieve all per-minutely analysis from "trades_minute_analysis" for a particular exchange..
            #..between two dates. Append all this data to a list.
            allMinutelyData.append(analysis_db.getAllMinutesFromExchangeRange(exchangeID, time1, time2))
            #looks like: allMinutelyData = [dataExchange1, dataExchange2, dataExchange3]

        allAverages = []
        allStandard_dev = []
        allGraph_time = []
        allGraph_time_prices = []
        allGraph_time_seconds = []

        #for each exchange we have minutely data for:
        for exchangeData in range(len(allMinutelyData)):
            average = []
            standard_dev = []
            graph_time = []
            graph_time_prices = []
            graph_time_seconds = []
            #and for each minute of data in an exchange:
            for minute in range(len(allMinutelyData[exchangeData])):
                data = allMinutelyData[exchangeData]            #retrieve the data
                graph_data = ast.literal_eval(data[minute][2])  #retrieve the json data
                timeList = graph_data.keys()                    #retrieve the timestamp from the json data
                this_time = timeList[0]                         #extract the timestamp from array so it's readable
                graph_time.append(this_time)                    #append the timestamp to a list of all timestamps
                average.append(data[minute][0])                 #append the minute's average to a list of all averages
                standard_dev.append(data[minute][1])            #append the standard deviaton to a list of all sd's
                graph_time_data = graph_data.get(this_time)     #retrieve both the trade prices and trade seconds
                graph_time_prices.append(graph_time_data[0])    #store the trade prices
                graph_time_seconds.append(graph_time_data[1])   #store the trade seconds

            allAverages.append(average)              #append this exchange's averages to a list of all exchange averages
            allStandard_dev.append(standard_dev)     #append this exchange's standard deviations to a list of all exchange sd's
            allGraph_time.append(graph_time)         #append this exchange's timestamps to a list of all exchange timestamps
            allGraph_time_prices.append(graph_time_prices)   #append this exchange's prices to a list of all exchange prices
            allGraph_time_seconds.append(graph_time_seconds) #append this exchange's seconds to a list of all exchange seconds

        allFinalAverages = []
        allFinalSDs = []
        #for every average and standard deviation, calculate the overall averages and standard deviations for each the exchanges
        for av in range(len(allAverages)):
            allFinalAverages.append(np.average(allAverages[av]))
            allFinalSDs.append(np.std(allStandard_dev[av]))

        allHighSDs = []
        allLowSDs = []

        #for each exchange, calculate the lower and upper standard deviations for each exchange's minutely data
        for all in range(len(allStandard_dev)):
            highSD = []
            lowSD = []
            for x in range(len(allStandard_dev[all])):
                highSD.append(float(allAverages[all][x])+float(allStandard_dev[all][x]))
                lowSD.append(float(allAverages[all][x])-float(allStandard_dev[all][x]))
            allHighSDs.append(highSD)
            allLowSDs.append(lowSD)

        #call function in PlotGraph.py to graph the data.
        PlotGraph.plotStandardDeviation(allGraph_time, allAverages, allFinalSDs, allHighSDs, allLowSDs, allFinalAverages,
                                       minDate, maxDate, exchanges, "minutes")



    #SAME AS ABOVE, BUT GRAPHS HOURLY DATA
    if HOURLY == True:

        for ex in range(len(exchanges)):
            exchangeID = (trades_db.getExchangeID(exchanges[ex]))
            allHourlyData.append(analysis_db.getAllHoursFromExchangeRange(exchangeID, time1, time2))

        allAverages = []
        allStandard_dev = []
        allGraph_time = []
        allGraph_time_prices = []
        allGraph_time_seconds = []


        for thisData in range(len(allHourlyData)):
            average = []
            standard_dev = []
            graph_time = []
            graph_time_prices = []
            graph_time_seconds = []
            for hour in range(len(allHourlyData[thisData])):
                data = allHourlyData[thisData]
                graph_data = ast.literal_eval(data[hour][2])
                timeList = graph_data.keys()
                this_time = timeList[0]
                graph_time.append(this_time)
                average.append(data[hour][0])
                standard_dev.append(data[hour][1])
                graph_time_data = graph_data.get(this_time)
                graph_time_prices.append(graph_time_data[0])
                graph_time_seconds.append(graph_time_data[1])

            allAverages.append(average)
            allStandard_dev.append(standard_dev)
            allGraph_time.append(graph_time)
            allGraph_time_prices.append(graph_time_prices)
            allGraph_time_seconds.append(graph_time_seconds)

        allFinalAverages = []
        allFinalSDs = []
        for av in range(len(allAverages)):
            allFinalAverages.append(np.average(allAverages[av]))
            allFinalSDs.append(np.std(allStandard_dev[av]))

        allHighSDs = []
        allLowSDs = []
        allHours = []

        for all in range(len(allGraph_time)):
            hours = []
            for h in range(len(allGraph_time[all])):
                hours.append(h)
            allHours.append(hours)
        for all in range(len(allStandard_dev)):
            highSD = []
            lowSD = []
            for x in range(len(allStandard_dev[all])):
                highSD.append(float(allAverages[all][x])+float(allStandard_dev[all][x]))
                lowSD.append(float(allAverages[all][x])-float(allStandard_dev[all][x]))
            allHighSDs.append(highSD)
            allLowSDs.append(lowSD)

        PlotGraph.plotStandardDeviation(allGraph_time, allAverages, allFinalSDs, allHighSDs, allLowSDs, allFinalAverages,
                                       minDate, maxDate, exchanges, "hours")
#allHours
