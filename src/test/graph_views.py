#!/usr/bin/env python

from matplotlib import pyplot, dates as mdates
from datetime import datetime
import pickle, sys

# Calculate the simple moving average for the given data
def sma(data, window):
    offset = (window - 1) / 2
    length = len(data)
    
    # Pad the front of the array so it will be graphed correctly
    result = [None for i in range(offset)]
    partial_sum = 0
    
    # Calculate averages
    for i in range(offset, length-offset):
        # Left side, centerpoint, and right side sums
        partial_sum += sum([data[i - left] for left in range(1, offset + 1)])
        partial_sum += data[i]
        partial_sum +=sum([data[i + right] for right in range(1, offset + 1)])
        # Take average
        avg = partial_sum / window
        result.append(avg)
        partial_sum = 0

    # Pad the end of the array
    for i in range(offset):
        result.append(None)
    return result

# Load our dictionaries as a time-sorted list of tuples from pickled files
# ('YYYY-MM-DD', value)
def load(filename):
    try:
        data = pickle.load(open(filename))
    except IOError:
        print 'ERROR: Could not load', filename
        print 'You probably need to run get_views.py first'
        sys.exit(1)
    result = [(key, data[key]) for key in sorted(data)]
    
    # Need to sanitize the result because stats.grok.se returns 31 days for every month
    sanitized = []
    for pair in result:
        try:
            date = datetime.strptime(str(pair[0]), '%Y-%m-%d')
            sanitized.append( (date, pair[1]) )
        except:
            pass
    return sanitized

# Manipulate and graph the data
def graph(name, data, window=5):
    # Separate the dates
    dates = mdates.date2num([d[0] for d in data])
    # Separate the values and calculate SMA
    values = [d[1] for d in data]
    data_sma = sma(values, window)

    # Start graphing
    figure, axis = pyplot.subplots()
    axis.plot_date(dates, values, 'b-', color='b', alpha=0.25)
    axis.xaxis.set_major_locator(mdates.MonthLocator())
    axis.xaxis.set_major_formatter(mdates.DateFormatter('%b \'%y'))

    axis.plot_date(dates, data_sma, 'b-', color='c', alpha=1)
    pyplot.ylabel('Views')
    figure.autofmt_xdate()
    pyplot.show()

filename = 'Ebola_virus_disease2014.p'
name = 'Ebola'
window = 7
print 'Loading ' + filename + '...'
ebola = load(filename)
print 'SMA window = ' + str(window)
print 'Plotting...'
graph(name, ebola, window)
