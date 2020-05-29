import requests
import os


def user_login(url, data):
	resp = requests.get(url, json=data)
	if resp.json()['status'] == 401:
		print('Something went wrong: {}'.format(resp.json()['error']))
		exit()
	elif resp.json()['status'] == 402:
		print('Something went wrong: {}'.format(resp.json()['error']))
		exit()
	else:
		print('Login Succeeded {}'.format(resp.status_code))
	print(resp.json())


def login():
	# print("Enter Username: ")
	inputusername = input("Enter Username: ")
	# print("Enter Password: ")
	inputpass = input("Enter Password: ")
	auth = {
		"table": "Employees",
		"username": inputusername,
		"password": inputpass
	}
	user_login('http://localhost:3000/api/Employee/' +
	           str(inputusername) + "/" + str(inputpass), auth)
	return inputusername, inputpass


def updates(x, username, password, objID, options):
	modify = []
	change = []
	data = ""
	mod = "not done"
	new = "not done"

	while mod != "done" and new != "done":
		mod = input("Field: ")
		new = input("New Value: ")

		if mod != "done" and new != "done":
			modify.append(mod)
			change.append(new)

	flag = True
	for each in modify:
		if each not in options:
			flag = False

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
	value = "not done"
	i = 0

	while value != "done" and i < len(fields):
		value = input("Enter Value for " + str(fields[i]) + ": ")
		if value != "done":
			values.append(value)
		i += 1

	data += "?"
	for i in range(0, len(fields)):
		data += str(fields[i]) + "=" + str(values[i]) + "&"
	data = data[:-1]

	json_resp = make_post_call('http://localhost:3000/api/' + str(x) + '/' + str(
		username) + '/' + str(password) + '/' + str(data), {})
	print(json_resp)
	
	print()
	print("--------------------")
	print("Hit Enter When Done!")
	print("--------------------")
	y = input()
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


def use(username, password):
	x = "not quit"
	# response = make_get_call('http://localhost:3000/api/employees/' + str(username))
	# admin_status = response['response'][0]['AdminRights']
	admin_status = 1

	print(admin_status)
	while (x != "quit"):
		print("You are currently in the Main panel!")
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
				if (x == "Employee" or x == "EmployeeShift" or x == "EmployeeType" or x == "PatientID"
					or x == "ShiftType" or x == "Task" or x == "TaskCode" or x == "Room" or x == "TaskLog" or x == "PatientLog"):
					json_resp = make_get_call(
					    'http://localhost:3000/api/' + str(x) + '/' + str(username) + '/' + str(password))
					print(json_resp)
				elif (x == 'back'):
					os.system('clear')
					break
				else:
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
					print("Employee Modification Options: EmployeeName, EmployeeTypeID, Salary, IsAdmin")
					option_list = ['EmployeeName', 'EmployeeTypeID', 'Salary', 'IsAdmin']
					updates(x, username, password, objID, option_list)
				elif (x == "EmployeeShift"):
					objID = input("Which shift would you like to update (ShiftID): ")
					print("EmployeeShift Modification Options: EmployeeID, ShiftTypeID")
					option_list = ['EmployeeID', 'ShiftTypeID']
					updates(x, username, password, objID, option_list)
				elif (x == "EmployeeType"):
					objID = input("Which employee type would you like to update (TypeID): ") 
					print("EmployeeType Modification Options: TypeName, TypeDescription")
					option_list = ['TypeName', 'TypeDescription']
					updates(x, username, password, objID, option_list)
				elif (x == "Patient"):
					objID = input("Which patient would you like to update (PatientID): ")
					print("Patient Modification Options: RoomID, PatientName, PatientDescription")
					option_list = ['RoomID', 'PatientName', 'PatientDescription']
					updates(x, username, password, objID, option_list)
				elif (x == "Task"):
					taskID = input("Which task's completion status would you like to update (TaskID): ")
					markTask = input("Type 0 if you would like to mark task as incomplete, Type 1 if you would like to mark task as complete: ")
					while markTask != str(0) and markTask != str(1):
						markTask = input("Please type 0 or 1 ONLY: ")
					set_Task(username, password, taskID, markTask)

				elif (x == "TaskCode"):
					objID = input("Which task code would you like to update (TaskCodeID): ")
					print("TaskCode Modification Options: TaskName, TaskDescription, Equipment")
					option_list = ['TaskName', 'TaskDescription', 'Equipment']
					updates(x, username, password, objID, option_list)
				elif (x == "Room"):
					objID = input("Which room would you like to update (RoomID): ")
					print("Room Modification Options: IsEmpty, Purpose")
					option_list = ['IsEmpty', 'Purpose']
					updates(x, username, password, objID, option_list)
				else:
					print("That wasn't one of the choices. Try again!")
					
			
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
				else:
					print("That wasn't one of the choices. Try again!")

		elif (x == "DeleteInfo"):  # NEED TO HANDLE ERRORS SUCH AS INVALID IDS
			while(x != "back" and x != "quit"):
				os.system('clear')
				print("You are currently in the DeleteInfo panel!")
				print("----------------------------------------")
				print("Deletion Options: Employee, ShiftType, Shift, EmployeeType, Task, TaskCode, Patient, Room")
				print("To go back, simply enter 'back'")
				print("----------------------------------------")

				x = input()
				os.system('clear')
				if (x == "Employee" or x == "ShiftType" or x == "EmployeeType" or x == "Patient"
					or x == "Shift" or x == "Task" or x == "TaskCode" or x == "Room"):
					objID = input("Which " + str(x).lower() + " would you like to delete (" + str(x) + "ID): ")
					json_resp = make_delete_call('http://localhost:3000/api/' + str(x) + '/' + str(username) + '/' + \
						str(password) + '/' + str(objID))
					print(json_resp)

					print()
					print("--------------------")
					print("Hit Enter When Done!")
					print("--------------------")
					y = input()

					os.system('clear')
				else:
					print("That wasn't one of the choices. Try again!")

					
if __name__ == '__main__':
	(userID, userpass)= login()
	use(userID, userpass)
