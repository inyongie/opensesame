#!/usr/bin/python

import MySQLdb

db = MySQLdb.connect("localhost", "root", "", "people_db")

cursor = db.cursor()

#cursor.execute("SELECT VERSION()")

first_name = raw_input('First Name : ')
last_name = raw_input('Last Name : ')
birthday = raw_input('Brithday (YYYY-MM-DD) : ')
category = raw_input('Category:\nJoyGivers (1)\n89 (2)\nNFC (3)\nFamily/Relative (4)\nOther (5)\n-----------\n')

print "Inserting %s %s, %s into table" % (first_name, last_name, birthday)

sql = "INSERT INTO name_and_birthday (first_name, last_name, birthday, group_id) \
	VALUES ('%s', '%s', '%s', '%s')" % \
	(first_name, last_name, birthday, category)


try:
  cursor.execute(sql)
  db.commit()

  # fetaching all entries
  cursor.execute ("SELECT * FROM name_and_birthday")
  data = cursor.fetchall ()
  for row in data :
    print row
    #print row[1] + " " + row[2] + "\t" + row[3]
except:
  db.rollback()
  print "Insertion Failed"
  

#data = cursor.fetchone()

#print "Database version : %s " % data

db.close()

