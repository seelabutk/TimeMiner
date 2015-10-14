from datetime import date
from dateutil.rrule import rrule, DAILY
from json import dumps
from sys import argv, maxint
from time import sleep
from urllib2 import urlopen, HTTPError, unquote
from zlib import decompress, MAX_WBITS

def process_data(result, year, month, day, hour, data):
    for line in data.splitlines():
        if line.startswith('en ') and len(line.split()) >= 3:
            name, view_count = line.split()[1:3]
            name = name.replace('_', ' ')
            view_count = int(view_count)
            views[name] = {
                'date': {
                    'year': year,
                    'month': month,
                    'day': day,
                    'hour': hour
                },
                'view_count': view_count
            }

def scrape_day(result, year, month, day):
    day += 1 # days returned begin at 0, when they need to begin at 1

    for hour in range(24):
        # get file name and url
        fname = 'pagecounts-' + str(year) + format(month, '02') \
            + format(day, '02') + '-' + format(hour, '02') + '0000.gz'
        url = 'http://dumps.wikimedia.org/other/pagecounts-raw/' \
            + str(year) + '/' + str(year) + '-' + format(month, '02') + '/' \
            + fname

        # grab data and gunzip it
        try:
            response = urlopen(url)
        except HTTPError:
            return
        data = unquote(decompress(response.read(), 16 + MAX_WBITS))

        # process data
        process_data(views, year, month, day, hour, data)

if __name__ == '__main__':
    # you must use this correctly
    if len(argv) != 1:
        print >> sys.stderr, 'usage: python delta_scraper.py'
        exit(1)

    start = date(2007, 12, 9)

    # scrape wiki
    views = {}
    for dt in rrule(DAILY, dtstart=start, until=date.today()):
        scrape_day(views, dt.year, dt.month, dt.day)
