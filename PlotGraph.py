#PURPOSE OF THIS FILE PlotGraph.py: Use the matplotlib library to plot the standard deviations of exchanges..
#                                  .. and visualise the volatility. See: http://matplotlib.org/1.4.0/api/index.html

import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt

colours = ["black", "cyan", "magenta", "yellow", "black", "white"]
#symbols = [".",     "x",    "--",       "v",       "^",       "+"]

def plotStandardDeviation(seconds, average, standardDeviation, highSD, lowSD, allAverages, date1, date2, exchangeName, timeframe):
    """Graph all standard deviations for each exchange"""

    allDates = []

    fig, ax = plt.subplots(1)

    #set the dateformatter to year, month, day, hour, minute, second.
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)

    for sd in range(len(highSD)):
        #convert all timestamps to dates
        dates=[dt.datetime.fromtimestamp(ts) for ts in seconds[sd]]
        #append all dates to an array
        allDates.append(dates)
        #plot the high standard deviations
        ax.plot(allDates[sd], highSD[sd], lw=2, color=colours[sd])
        #optionally show the average
        #ax.plot(seconds[sd], average[sd], lw=1, label=exchangeName[sd], color=colours[sd], ls="-")
        #plot the low standard deviations
        ax.plot(allDates[sd], lowSD[sd], lw=3, label=exchangeName[sd], color=colours[sd])
        #fill the space between the high and low standard deviations to visualise the volatility
        ax.fill_between(allDates[sd], lowSD[sd], highSD[sd], facecolor=colours[sd], alpha=0.5, label="test")

        #Visualises when the exchange rose above or fell below it's overall average
        #Best to use only when looking at a single exchange otherwise it looks messy
        #ax.fill_between(allDates[sd], average[sd], allAverages[sd], where=allAverages[sd]>average[sd], facecolor='red', alpha=0.3)
        #ax.fill_between(allDates[sd], average[sd], allAverages[sd], where=allAverages[sd]<average[sd], facecolor='blue', alpha=0.3)

    ax.plot() #plot.

    ax.legend(loc='upper left') #location of legend

    ax.set_xlabel(timeframe)    #minutes, or hours
    ax.set_ylabel('price')
    ax.grid()
    plt.title("Range: " + str(date1) + " - " + str(date2)) #displays range as title
    plt.show()
