import requests
import json
'''
Client side demo to fetch data from a RESTful API.  Assumes Node.js file api is running (nodemon api.js <localhost|sunapee>) 
on the server side.
Author: Tim Pierson, Dartmouth CS61, Spring 2020
Requires installation of mysql connector: pip install mysql-connector-python
    also requires Requests: pip install requests
Based on: https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html

Usage: python call_api.py 
'''

def make_get_call(url):
    #make get call to url
    resp = requests.get(url)
    #expecting to get a status of 200 on success
    if resp.json()['status'] != 200:
        # This means something went wrong.
        print("something went wrong with your credentials")
        exit()
    return resp.json()['response']
    #print data returned


def make_post_call(url, data):
    #make post call to url passing it data
    resp = requests.post(url)
    #expecting to get a status of 201 on success
    return resp.json()['response']

def make_put_call(url,data):
    #make post call to url passing it data
    resp = requests.put(url)
    #expecting to get a status of 200 on success
    if resp.json()['status'] != 200:
        exit()
    return resp.json()['response']

def make_delete_call(url):
    #make post call to url passing it data
    resp = requests.delete(url)
    #expecting to get a status of 200 on success
    if resp.json()['status'] != 200:
        exit()
    return resp.json()['response']



if __name__ == '__main__':
    username = input("Please input username ")
    password = input("Please input password ")
    employeeID = input("Please input EmployeeID ")
    
#make a get call
    initial_get=make_get_call('http://localhost:3000/api/employees/'+username+'/'+password+'/'+employeeID)
    if not initial_get:
        print("invalid credentials")
        sys.exit()
    if (initial_get[0]['Admin']==1):
        print("You have entered a user with admin privileges.")
        while (True):
            c=input("To perform a command, please enter [g]et, [p]ost, p[u]t, [d]elete or [q]uit")
            if (c=='g'):
                empId=input("Please enter id of Employee you would like to query (just hit enter to get all)")
                print(make_get_call('http://localhost:3000/api/employees/'+username+'/'+password+'/'+empId))
            elif (c=='p'):
                params=input("Please enter the following parameters separated by spaces: idEmployees, DateHired, Salary, Username, Password, Admin>\n")
                data={}
                params=params.split(" ")
                if len(params)!= 6:
                    print("Invalid number of parameters")
                else:
                    msg='http://localhost:3000/api/employees/'+username+'/'+password+'/'
                    msg=msg+"?idEmployees="+params[0]
                    msg=msg+"&DateHired=" + params[1]
                    msg=msg+"&Salary=" + params[2]
                    msg=msg+"&Username="+params[3]
                    msg=msg+"&Password="+params[4]
                    msg=msg+"&Admin="+params[5]
                    print(make_post_call(msg,{}))
            elif (c=='d'):
                empId=input("Please enter id of Employee you would like to delete")
                print(make_delete_call('http://localhost:3000/api/employees/'+username+'/'+password+'/'+empId))
            elif (c=="u"):
                empId=input("Please enter id of Employee you would like to update")
                url='http://localhost:3000/api/employees/'+username+'/'+password+'/'+empId+'/'
                changes=input("please enter fields you would like changed in the form ?field1=arg1&field2=arg2%field3=....")
                print(make_put_call(url+changes,{}))
            elif (c=='q'):  
                break
    else:
        print("You have entered without admin privileges")
        while (True):
            c=input("To perform a command, please enter [g]et, p[u]t, [q]uit")
            if (c=='g'):
                print(make_get_call('http://localhost:3000/api/employees/'+username+'/'+password+'/'+employeeID))
            elif (c=="u"):
                url='http://localhost:3000/api/employees/'+username+'/'+password+'/'+employeeID+'/'
                changes=input("please enter fields you would like changed in the form ?field1=arg1&field2=arg2%field3=....")
                print(make_put_call(url+changes,{}))
            elif (c=='q'):  
                break
 
#    make_get_call('http://localhost:3000/api/employees/'+username+'/'+password+'/'+employeeID)

#restaurant_data = {"RestaurantName": "Your New Retaurant", "Boro": "Manhattan" }
#    make_post_call('http://localhost:3000/api/employees/'+username+'/'+password+'/'+employeeID)

#restaurant_data = {"RestaurantName": "This is a new name", "Boro": "Queens" }
#    make_put_call('http://localhost:3000/api/employees/'+username+'/'+password+'/'+employeeID,restaurant_data)

#    make_delete_call('http://localhost:3000/api/employees/'+username+'/'+password+'/'+employeeID)

