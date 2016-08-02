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
				print(item.keys())
				if 'closing_start' not in item.keys():
					if 'nodata' not in item.keys():
						print('|-'+ item['meal'] + ' ' + item['dish'] + ' ' + str(item['price_1']) + u'€ ' + item['info'])
					else:
						print("No Data")
				else:
					close_start = datetime.datetime.fromtimestamp(int(item['closing_start'])).strftime('%d. %m. %Y')
					close_end   = datetime.datetime.fromtimestamp(int(item['closing_end'])).strftime('%d. %m. %Y')
					print("Closed from {} to {}".format(close_start,close_end))
	else:
			print('No Data')
