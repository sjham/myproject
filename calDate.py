from datetime import datetime, date, timedelta


def calDate():
    syear = int(input('Start Year: '))
    smonth = int(input('Start Month: '))
    sday = int(input('Start Day: '))
    eyear = int(input('End Year: '))
    emonth = int(input('End Month: '))
    eday = int(input('End Day: '))
    date1 = datetime.date(syear, smonth, sday)
    date2 = datetime.date(eyear, emonth, eday)


    #startDay = input('Enter a Start date in YYYY-MM-DD format: ')
    #year, month, day = int(map(startDay.split('-')))
    #date1 = datetime.date(year, month, day)
    #endDay = input('Enter a End date in YYYY-MM-DD format: ')
    #year, month, day = int(map(endDay.split('-')))
    #date2 = datetime.date(year, month, day)
    date1 = date(input("Insert Start Day(yyyy,m,d): "))
    date2 = date(input("Insert End Day(yyyy,m,d): "))

#    date1 = date.strptime(s, '%Y, %m, %d')
#    date2 = date.strptime(e, '%Y, %m, %d')
    #date1 = date(ds)  # start date
    #date2 = date(de)  # end date
    delta = date2 - date1         # timedelta
    for i in range(delta.days + 1):
        rawDates = date1 + timedelta(days=i)
        newsDates = [str(rawDates)]
    return newsDates
#    print(newsDates)

calDate()
