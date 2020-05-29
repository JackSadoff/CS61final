import requests
import os

def user_login(url, data):

	resp = requests.get(url, json=data)

	if resp.json()['status'] == 401:
		print('Something went wrong: {}'.format(resp.json()['response']))
		exit()
	elif resp.json()['status'] == 402:
		print('Something went wrong: {}'.format(resp.json()['response']))
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

	user_login('http://localhost:3000/api/Employee/' + str(inputusername) + "/" + str(inputpass), auth)

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
		
		json_resp = make_put_call('http://localhost:3000/api/' + str(x) + '/' + str(username) + '/' + str(password) + '/' + str(objID) + '/' + str(data), {})
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


def make_get_call(url):
	#make get call to url
	resp = requests.get(url)
	#expecting to get a status of 200 on success
	if resp.json()['status'] != 200:
		# This means something went wrong.
		print('Something went wrong {}'.format(resp.status_code))
		exit()
		
	return resp.json()['response']

def make_post_call(url, data):
	#make post call to url passing it data
	resp = requests.post(url, json=data)
	#expecting to get a status of 201 on success
	if resp.json()['status'] != 201:
		print('Something went wrong {}'.format(resp.status_code))
		exit()
	print('post succeeded')
	
def make_put_call(url,data):
	#make post call to url passing it data
	resp = requests.put(url, json=data)
	#expecting to get a status of 200 on success
	if resp.json()['status'] != 200:
		print('Something went wrong {}'.format(resp.status_code))
		exit()
	print('put succeeded')

	return resp.json()['response']
	

def make_delete_call(url):
	#make post call to url passing it data
	resp = requests.delete(url)
	#expecting to get a status of 200 on success
	if resp.json()['status'] != 200:
		print('Something went wrong {}'.format(resp.status_code))
		exit()
	print('delete succeeded')

def use(username, password):
	x = "not quit"
	# response = make_get_call('http://localhost:3000/api/employees/' + str(username))
	# admin_status = response['response'][0]['AdminRights']

	admin_status = 1
	
	print(admin_status)
	while (x != "quit"):
		print("You are currently in the Main panel!")
		print("----------------------------------------")
		print("Options: ViewInfo, ModifyInfo")
		print("----------------------------------------")
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
				if (x == "Employee" or x == "EmployeeShift" or x == "EmployeeType" or x == "PatientID" \
					or x == "ShiftType" or x =="Task"or x == "TaskCode"or x == "Room" or x == "TaskLog" or x == "PatientLog"):
					json_resp = make_get_call('http://localhost:3000/api/' + str(x) + '/' + str(username) + '/' + str(password))
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
				
				
				#if (x == "Employee" or x == "EmployeeShift" or x == "EmployeeType" or x == "PatientID" \
					#or x =="Task"or x == "TaskCode"or x == "Room"):

				if (x == "Employee"):
					objID = input("Which employee would you like to update (ID): ")
					print("Employee Modification Options: EmployeeName, EmployeeTypeID, Salary, IsAdmin")
					option_list = ['EmployeeName', 'EmployeeTypeID', 'Salary', 'IsAdmin']
					updates(x, username, password, objID, option_list)

				# elif (x == "EmployeeShift"):
				# 	objID = input("Which shift would you like to update (ShiftID): ")
				# 	print("Employee Modification Options: EmployeeID, ShiftTypeID")
				# 	updates(x, username, password, objID)

				# elif (x == "EmployeeType"):
				# 	objID = input("Which employee type would you like to update (TypeID): ")
				# 	print("Employee Modification Options: TypeName, TypeDescription")
				# 	updates(x, username, password, objID)

				
							
if __name__ == '__main__':
	(userID, userpass)= login()
	# use(userID, userpass)
	json_resp = make_put_call('http://localhost:3000/api/Complete/Task' + str(userID) + '/' + str(userpass) + "/6", {} )
	print(json_resp)				