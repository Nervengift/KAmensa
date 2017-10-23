#!/usr/bin/python3
# -*- coding: utf-8 -*-
import KAMensa
import datetime

## On weekends, print plan for monday
date = datetime.date.today();
if date.weekday() == 5 :
    date += datetime.timedelta(2)
elif date.weekday() == 6:
    date += datetime.timedelta(1)

plan = KAMensa.mensaplan()

header = KAMensa.key_to_name('adenauerring') + " " + str(date)

print('*'*len(header) +'\n' + header + '\n' + '*'*len(header))

for line in plan.keys('adenauerring'):
    meal = plan.meal('adenauerring',line,date)
    if meal != None :
            # Linie
            print('\n' + str(KAMensa.key_to_name(line)) + ':')
            for item in meal:
                if 'nodata' not in item.keys():
                    print('|-'+ item['meal'] + ' ' + item['dish'] + ' ' + str(item['price_1']) + u'€ ' + item['info'])
                else:
                    print("No Data")
    else:
            print('No Data')
