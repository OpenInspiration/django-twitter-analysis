#!/bin/use/python

#import json

#from pprint import pprint

#with open('smi.json') as data_file:    
#    data = json.load(data_file)

#print(data["om_points"])

import MySQLdb

db = MySQLdb.connect("127.0.0.1", "root", "root", "checkin")

cursor = db.cursor()

cursor.execute("select * from checkinsystem")

try:
	results = cursor.fetchall()
	for row in results:
		print row[0]

except:
	print "Error"
	
db.close()