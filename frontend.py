import requests
import os
import pandas as pd
import json

def read_json_custom(resp_json):
	for row in resp_json:
		for entry in row:
			print(str(entry) + ": " + str(row[entry]), end="\t")
		print()
		print("*******************************")

def user_login(url, data):
	resp = requests.get(url)
	if resp.json()['status'] == 401:
		print('Something went wrong: {}'.format(resp.json()['error']))
		exit()
	elif resp.json()['status'] == 402:
		print('Something went wrong: {}'.format(resp.json()['error']))
		exit()
	else:
		print('Login Succeeded {}'.format(resp.status_code))
	
	
	return resp.json()['response']


def login():
	# print("Enter Username: ")
	inputusername = input("Enter Username: ")
	# print("Enter Password: ")
	inputpass = input("Enter Password: ")
	# auth = {
	# 	"table": "Employees",
	# 	"username": inputusername,
	# 	"password": inputpass
	# }

	resp_json = user_login('http://localhost:3000/api/Employee/' +
	           str(inputusername) + "/" + str(inputpass), {})

	admin_status = 0

	for row in resp_json:
		
		if row['Username'] == str(inputusername):
			if row['IsAdmin'] == str(1):
				admin_status = 1

	return inputusername, inputpass, admin_status


def updates(x, username, password, objID, options):
	modify = []
	change = []
	data = ""
	mod = "not done"
	new = "not done"
	flag2 = True

	while mod != "done" and new != "done":
		mod = input("Field: ")
		new = input("New Value: ")

		if mod != "done" and new != "done":
			modify.append(mod)
			change.append(new)
		# elif mod == "done" or new == "done":
			
		# 	print()
		# 	print("Invalid Entry! Please try again.")
		# 	print("********************")
		# 	print("Press Enter to continue.")
		# 	input()
		# 	return

	flag = True
	for each in modify:
		if each not in options:
			flag = False
	
	if len(modify) == 0 or len(change) == 0:
		flag = False
	# print(flag)

	if flag:
		data += "?"
		for i in range(0, len(modify)):
			data += str(modify[i]) + "=" + str(change[i]) + "&"
		data = data[:-1]

		json_resp = make_put_call('http://localhost:3000/api/' + str(x) + '/' + str(
		    username) + '/' + str(password) + '/' + str(objID) + '/' + str(data), {})
		print(json_resp)
	else:
		print()
		print("Invalid Field Chosen! Please try again.")

	print()
	print("--------------------")
	print("Hit Enter When Done!")
	print("--------------------")
	y = input()

	os.system('clear')

def mod_auth(x, username, password):
	json_resp = make_get_call('http://localhost:3000/api/' + str(x) + '/' + str(username) + '/' + str(password))
	
	pklist = []
	for row in json_resp:
		for entry in row:
			pklist.append(row[entry])
			break
	print("Valid Keys:", end="")
	for i in range(len(pklist) - 1):
		print(str(pklist[i]) + ",", end="")
	print(str(pklist[len(pklist)-1]))
	
	return pklist


def set_Task(username, password, taskID, markTask):
	json_resp = make_put_call('http://localhost:3000/api/Complete/Task' + '/' + str(username) + '/' \
		+ str(password) + '/' + str(taskID) + '?isComplete=' + str(markTask), {})
	print(json_resp)
	
	print()
	print("--------------------")
	print("Hit Enter When Done!")
	print("--------------------")
	y = input()

	os.system('clear')

def deletes(username, password):
	pass

def add(x, username, password, fields):
	values = []
	data = ""
	i = 0
	value = ""
	while i < len(fields):
		while value == "":
			value = input("Enter Value for " + str(fields[i]) + ": ")
		values.append(value)
		value = ""

		i += 1

	data += "?"
	for i in range(0, len(fields)):
		data += str(fields[i]) + "=" + str(values[i]) + "&"
	data = data[:-1]

	# print(data)
	try:
		json_resp = make_post_call('http://localhost:3000/api/' + str(x) + '/' + str(
		username) + '/' + str(password) + '/' + str(data), {})

		print(json_resp)
	except:
		print("Erroneous Entry! Please try again.")
	
	
	print()
	print("--------------------")
	print("Hit Enter When Done!")
	print("--------------------")
	input()

	os.system('clear')

def make_get_call(url):
	# make get call to url
	resp = requests.get(url)
	# expecting to get a status of 200 on success
	if resp.json()['status'] != 200:
		# This means something went wrong.
		print('Something went wrong {}'.format(resp.status_code))
		exit()
	return resp.json()['response']

def make_post_call(url, data):
	# make post call to url passing it data
	resp = requests.post(url, json=data)
	# expecting to get a status of 201 on success
	if resp.json()['status'] != 200:
		print('Something went wrong {}'.format(resp.status_code))
		exit()
	print('post succeeded')
	return resp.json()['response']

def make_put_call(url, data):
	# make post call to url passing it data
	resp = requests.put(url, json=data)
	# expecting to get a status of 200 on success
	if resp.json()['status'] != 200:
		print('Something went wrong: {}'.format(resp.json()['error']))
		exit()
	print('put succeeded')
	return resp.json()['response']

def make_delete_call(url):
	# make post call to url passing it data
	resp = requests.delete(url)
	# expecting to get a status of 200 on success
	if resp.json()['status'] != 200:
		print('Something went wrong {}'.format(resp.json()['error']))
		exit()
	print('delete succeeded')
	return resp.json()['response']


def use(username, password, admin_status):
	x = "not quit"
	# response = make_get_call('http://localhost:3000/api/employees/' + str(username))
	# admin_status = response['response'][0]['AdminRights']
	

	if admin_status == 1:
		

		while (x != "quit"):
			print("You are currently in the Main Admin panel!")
			print("--------------------------------------------------")
			print("Options: ViewInfo, ModifyInfo, AddInfo, DeleteInfo")
			print("--------------------------------------------------")
			x = input()
			os.system('clear')

			if (x == "ViewInfo"):
				while(x != "back" and x != "quit"):
					os.system('clear')
					print("You are currently in the ViewInfo panel!")
					print("----------------------------------------")
					print("For more Info please select: Employee, EmployeeShift, EmployeeType, ShiftType, Task, TaskCode, Patient, Room")
					print("Log Options: TaskLog, PatientLog")
					print("To go back, simply enter 'back'")
					print("----------------------------------------")
					x = input()
					os.system('clear')
					if (x == "Employee" or x == "EmployeeShift" or x == "EmployeeType" or x == "Patient"
						or x == "ShiftType" or x == "Task" or x == "TaskCode" or x == "Room" or x == "TaskLog" or x == "PatientLog"):
						json_resp = make_get_call(
							'http://localhost:3000/api/' + str(x) + '/' + str(username) + '/' + str(password))
						# print(json_resp)
						read_json_custom(json_resp)
					elif (x == 'back'):
						os.system('clear')
						break
					elif (x != "back" or x != "quit"):
						print("That wasn't one of the choices! Try again.")

					print()
					print("--------------------")
					print("Hit Enter When Done!")
					print("--------------------")
					y = input()
					os.system('clear')

			elif(x == "ModifyInfo"):
				while(x != "back" and x != "quit"):
					os.system('clear')
					print("You are currently in the ModifyInfo panel!")
					print("----------------------------------------")
					print("Modification Options: Employee, EmployeeShift, EmployeeType, Task, TaskCode, Patient, Room")
					print("To go back, simply enter 'back'")
					print("----------------------------------------")

					x = input()
					os.system('clear')

					if (x == "Employee"):
						objID = input("Which employee would you like to update (ID): ")

						pklist = mod_auth(x, username, password)
						if int(objID) in pklist:
							print("Employee Modification Options: EmployeeName, EmployeeTypeID, Salary, IsAdmin")
							option_list = ['EmployeeName', 'EmployeeTypeID', 'Salary', 'IsAdmin']
							updates(x, username, password, objID, option_list)
						else:
							print("Invalid ID!")
							print("*******************")
							input("Press Enter to Continue!")


					elif (x == "EmployeeShift"):
						objID = input("Which shift would you like to update (ShiftID): ")
						pklist = mod_auth(x, username, password)
						if int(objID) in pklist:
							print("EmployeeShift Modification Options: EmployeeID, ShiftTypeID")
							option_list = ['EmployeeID', 'ShiftTypeID']
							updates(x, username, password, objID, option_list)
						else:
							print("Invalid ID!")
							print("*******************")
							input("Press Enter to Continue!")

					elif (x == "EmployeeType"):
						objID = input("Which employee type would you like to update (TypeID): ") 
						pklist = mod_auth(x, username, password)
						if int(objID) in pklist:
							print("EmployeeType Modification Options: TypeName, TypeDescription")
							option_list = ['TypeName', 'TypeDescription']
							updates(x, username, password, objID, option_list)
						else:
							print("Invalid ID!")
							print("*******************")
							input("Press Enter to Continue!")
					elif (x == "Patient"):
						objID = input("Which patient would you like to update (PatientID): ")
						pklist = mod_auth(x, username, password)
						if int(objID) in pklist:
							print("Patient Modification Options: PatientName, PatientDescription")
							option_list = ['PatientName', 'PatientDescription']
							updates(x, username, password, objID, option_list)
						else:
							print("Invalid ID!")
							print("*******************")
							input("Press Enter to Continue!")
					elif (x == "Task"):
						objID = input("Which task's completion status would you like to update (TaskID): ")
						pklist = mod_auth(x, username, password)
						if int(objID) in pklist:
							markTask = input("Type 0 if you would like to mark task as incomplete, Type 1 if you would like to mark task as complete: ")
							while markTask != str(0) and markTask != str(1):
								markTask = input("Please type 0 or 1 ONLY: ")
							set_Task(username, password, objID, markTask)
						else:
							print("Invalid ID!")
							print("*******************")
							input("Press Enter to Continue!")

					elif (x == "TaskCode"):
						objID = input("Which task code would you like to update (TaskCodeID): ")
						pklist = mod_auth(x, username, password)
						if int(objID) in pklist:
							print("TaskCode Modification Options: TaskName, TaskDescription, Equipment")
							option_list = ['TaskName', 'TaskDescription', 'Equipment']
							updates(x, username, password, objID, option_list)
						else:
							print("Invalid ID!")
							print("*******************")
							input("Press Enter to Continue!")

							
					elif (x == "Room"):
						objID = input("Which room would you like to update (RoomID): ")
						pklist = mod_auth(x, username, password)
						if int(objID) in pklist:
							print("Room Modification Options: IsEmpty, Purpose")
							option_list = ['IsEmpty', 'Purpose']
							updates(x, username, password, objID, option_list)
						else:
							print("Invalid ID!")
							input("Press Enter to Continue!")
							
					elif (x == "back" or x == "quit"):
						continue
					elif (x != "back" or x != "quit"):
						print("That wasn't one of the choices. Try again!")
						print("--------------------")
						print("Hit Enter To Continue!")

						y = input()
				os.system('clear')
				


			elif(x == "AddInfo"): # NEED TO FINISH THIS
				while(x != "back" and x != "quit"):
					os.system('clear')
					print("You are currently in the AddInfo panel!")
					print("----------------------------------------")
					print("Addition Options: Employee, EmployeeShift, EmployeeType, Task, TaskCode, Patient, Room")
					print("To go back, simply enter 'back'")
					print("----------------------------------------")

					x = input()
					os.system('clear')
					if (x == "Employee"):
						fields = ['EmployeeID', 'EmployeeName', 'EmployeeTypeID', 'Salary', 'StartDate', 'Username', 'Password', 'IsAdmin']
						add(x, username, password, fields)
						
					elif(x == "EmployeeShift"):
						fields = ['ShiftID', 'EmployeeID', 'Date']
						add(x, username, password, fields)
					elif(x == "EmployeeType"):
						fields = ['EmployeeTypeID', 'TypeName', 'TypeDescription']
						add(x, username, password, fields)
					elif(x == "Task"):
						fields = ['TaskID', 'TaskCodeID', 'IsComplete', 'TimeAssigned', 'RoomID', 'ShiftID']
						add(x, username, password, fields)
					elif(x == "TaskCode"):
						fields = ['TaskCodeID', 'TaskName', 'TaskDescription', 'Equipment']
						add(x, username, password, fields)
					elif(x == "Patient"):
						fields = ['PatientID', 'RoomID', 'PatientName', 'ArrivalDate', 'PatientDescription']
						add(x, username, password, fields)
					elif(x == "Room"):
						fields = ['RoomID', 'IsEmpty', 'Purpose']
						add(x, username, password, fields)
					elif (x == "back" or x == "quit"):
						continue
					elif (x != "back" or x != "quit"):
						print("That wasn't one of the choices. Try again!")
						print("--------------------")
						print("Hit Enter To Continue!")

			elif (x == "DeleteInfo"):  # NEED TO HANDLE ERRORS SUCH AS INVALID IDS
				while(x != "back" and x != "quit"):
					os.system('clear')
					print("You are currently in the DeleteInfo panel!")
					print("----------------------------------------")
					print("Deletion Options: Employee, ShiftType, Shift, EmployeeType, Task, TaskCode, Patient, Room")
					print("To go back, simply enter 'back'")
					print("----------------------------------------")
					objID = ""
					x = input()
					os.system('clear')
					if (x == "Employee" or x == "ShiftType" or x == "EmployeeType" or x == "Patient"
						or x == "Shift" or x == "Task" or x == "TaskCode" or x == "Room"):

						while objID == "":
							objID = input("Which " + str(x).lower() + " would you like to delete (" + str(x) + "ID): ")

						pklist = mod_auth(x, username, password)
						# print(pklist)

						if int(objID) in pklist:
							try:
								json_resp = make_delete_call('http://localhost:3000/api/' + str(x) + '/' + str(username) + '/' + \
									str(password) + '/' + str(objID))
								print(json_resp)
							except:
								print("Erroneous Entry! Please try again.")
								print("For reference here is a list of valid delete ID's")
						else:		
							print("Invalid ID!")

						

						print()
						print("--------------------")
						print("Hit Enter To Continue!")
						print("--------------------")
						y = input()

						os.system('clear')
					elif (x == "back" or x == "quit"):
						continue
					elif (x != "back" or x != "quit"):
						print("That wasn't one of the choices. Try again!")
						print("--------------------")
						print("Hit Enter To Continue!")

						y = input()
				os.system('clear')
	elif admin_status == 0:
		while (x != "quit"):
			print("You are currently in the Main User panel!")
			print("--------------------------------------------------")
			print("Options: ViewInfo, ModifyInfo")
			print("--------------------------------------------------")
			x = input()
			os.system('clear')

			if (x == "ViewInfo"):
				while(x != "back" and x != "quit"):
					os.system('clear')
					print("You are currently in the ViewInfo panel!")
					print("----------------------------------------")
					print("For more Info please select: Employee, EmployeeShift, EmployeeType, ShiftType, Task, TaskCode, Patient, Room")
					print("To go back, simply enter 'back'")
					print("----------------------------------------")
					x = input()
					os.system('clear')
					if (x == "Employee" or x == "EmployeeShift" or x == "EmployeeType" or x == "Patient"
						or x == "ShiftType" or x == "Task" or x == "TaskCode" or x == "Room" or x == "TaskLog" or x == "PatientLog"):
						json_resp = make_get_call(
							'http://localhost:3000/api/' + str(x) + '/' + str(username) + '/' + str(password))
						# print(json_resp)
						read_json_custom(json_resp)
					elif (x == 'back'):
						os.system('clear')
						break
					elif (x != "back" or x != "quit"):
						print("That wasn't one of the choices! Try again.")

					print()
					print("--------------------")
					print("Hit Enter When Done!")
					print("--------------------")
					y = input()
					os.system('clear')


					
if __name__ == '__main__':
	(userID, userpass, admin_status)= login()
	use(userID, userpass, admin_status)
	# print(resp_json)