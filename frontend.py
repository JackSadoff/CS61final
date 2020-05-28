import requests

def make_get_call(url):
	#make get call to url
	resp = requests.get(url)
	#expecting to get a status of 200 on success
	if resp.json()['status'] != 200:
		# This means something went wrong.
		print('Something went wrong {}'.format(resp.status_code))
		exit()

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
	

def make_delete_call(url):
	#make post call to url passing it data
	resp = requests.delete(url)
	#expecting to get a status of 200 on success
	if resp.json()['status'] != 200:
		print('Something went wrong {}'.format(resp.status_code))
		exit()
	print('delete succeeded')

if __name__ == '__main__':
    username = input("Please input username ")
    password = input("Please input password ")
    initial_get_call = 
    