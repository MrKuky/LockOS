from tkinter import *
import RPi.GPIO as GPIO
import time
import mysql.connector
import threading


# DB CONNECT

mydb = mysql.connector.connect(host="innodb.endora.cz", port="3306", user="thekukycz", passwd="Admin001", database="kukysos")
mycursor = mydb.cursor()

# selecting column value into PY variable

sqlQ_status = "select status from door where id = '2'"
#id = (2,)
#mycursor.execute(sqlQ_status, id)
mycursor.execute(sqlQ_status)
record = mycursor.fetchone()
statusV = float(record[0])
print("Door STATUS is NOW: ",statusV)


root = Tk()

root.title("Lock")

GPIO.setmode(GPIO.BOARD)
pin=37

def unlock():
	GPIO.setup(pin, GPIO.OUT)
	print("odemykam ... nastavuji pin na OUT")
	sqlU = "UPDATE door SET status = '0' WHERE ID = '2'"
	mycursor.execute(sqlU)
	mycursor.execute(sqlQ_status)
	record = mycursor.fetchone()
	statusV = float(record[0])
	mydb.commit()
	print("Status door is now set to : ",statusV)
	button_lock["state"] = "normal"
	button_unlock["state"] = "disabled"
	
def lock():
	GPIO.setup(pin, GPIO.IN)
	print("zamykam ... nastavuji pin na IN")
	sqlL = "UPDATE door SET status = '1' WHERE ID = '2'"
	mycursor.execute(sqlL)
	mycursor.execute(sqlQ_status)
	record = mycursor.fetchone()
	statusV = float(record[0])
	mydb.commit()
	print("Status door is now set to : ",statusV)
	button_lock["state"] = "disabled"
	button_unlock["state"] = "normal"
	
	
button_lock = Button(root, text="Lock", padx=91, pady=20, command=lambda:[lock()])
button_unlock = Button(root, text="Unlock", padx=91, pady=20, command=lambda:[unlock()])


# put on the screen

button_lock.grid(row=1, column=1)
button_unlock.grid(row=1, column=2)



def printit():
	threading.Timer(5.0, printit).start()
	print("Hello, World!")
	# check database
	sqlQ_status = "select status from door where id = '2'"
	mycursor.execute(sqlQ_status)
	record = mycursor.fetchone()
	statusV = float(record[0])
	print("Door STATUS is NOW: ",statusV)
	if statusV == 0:
		unlock()
	else:
		lock()
	  

printit()

# -- END -- 
root.mainloop()
GPIO.cleanup()
	

