#!/usr/bin/python

import datetime
import smtplib
import MySQLdb


#1. Load Birthday List

#TODO: expand from just JoyGivers -- Add a "Group" identifier to distinguish between groups, then make it behave (send email) particularly to a specific group

today = datetime.date.today()

db = MySQLdb.connect("localhost","root","","people_db")

cursor = db.cursor()

sql = "SELECT * FROM name_and_birthday \
      WHERE MONTH(birthday) = MONTH(NOW()) and DAY(birthday) = DAY(NOW())" 

print sql

#2. Check if Today is Someone's Birthday

birthday_list = []
try:
  cursor.execute(sql)
  results = cursor.fetchall()
  for row in results:
    print row
    birthday_list.append(row[1] + " " + row[2])
except:
  print "Error: Unable to Fetch Data"

db.close()

# print today.month
# print today.day
# for person in people_list:
#   if(person[2] == today.month and person[3] == today.day):
#     birthday_list.append(person[0])

#3. Send out Birthday Mail

if(len(birthday_list) > 0):
  SERVER = "localhost"
  
  FROM = "BirthdayBot"
  FROM_ADDR = "root@inyongie.com"
  TO = ["inyong89@gmail.com"] # must be a list
  
  SUBJECT = "Happy Birthday, "
  
  for name in birthday_list:
    SUBJECT = SUBJECT + name + ", "
  SUBJECT = SUBJECT[:-2]
  SUBJECT = SUBJECT + "!"
  
  TEXT = "Today is the birthday of the people in the title. Happy Birthday!\n\n\n\nNOTE: This is sent by a script. It will not be able to receive or process responses."
  
  # Prepare actual message
  
  message = 'Subject: %s\nFrom: %s\n\n%s' % (SUBJECT, FROM, TEXT)
  
  # Send the mail
  
  server = smtplib.SMTP(SERVER)
  server.sendmail(FROM_ADDR, TO, message)
  server.quit()
