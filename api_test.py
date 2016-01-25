import hashlib
import hmac
import json
import requests

edustore_api_endpoint = "https://repository.dikaios.fi/api/publisher/v2" 
client_key = "your_client_key"
client_secret = "your_client_secret"

def edustore_api_call(call, method, payload):

	url = edustore_api_endpoint + '/' + call

	message = json.dumps(payload)

	message = bytes(message).encode('utf-8')
	secret_key = bytes(client_secret).encode('utf-8')
	auth = "PUBLISHER" + ' ' + client_key + ':' + hmac.new(client_secret, message, digestmod=hashlib.sha256).hexdigest();

	headers = {
		'Authentication' :  auth,                                                                       
		'Content-Type' : 'application/json',
		'Content-Length' : str(len(message))         
	}

	print "CALLING [" + method + "] " + url + "\n";

	if method == "GET":
		r = requests.get(url, data=message, headers=headers)
	elif method == "PUT":
		r = requests.put(url, data=message, headers=headers)
	elif method == "POST":
		r = requests.post(url, data=message, headers=headers)
	elif method == "DELETE":
		r = requests.delete(url, data=message, headers=headers)

	print r.content, r.status_code

	if r.status_code != 200:
		raise Exception(r.status_code)

	return json.loads(r.content)


# Test connection 
response = edustore_api_call('ping', "GET", None)
print "Server responsed with " + response['message']

# Get available metadatas  
response = edustore_api_call('metadata', "GET", None)
print response


# Add resource  
resource = {
	"name" : "Some title",				# Max 128 
	"description" : "Longer description",		# Max 1024 chars 
	"is_link" : 1,								# is link or not 
	"link_url" : "test",						# Is link 
	"publisher_material_id" : "test2",			# Your material id
	"metadata"  : ["Koulutusaste/1. Luokka"],	# Pre-defined metadata
	"comment"  : "2016-01-11",					# Your internal comment itnerval  
	"tags"  : ['maantieto', 'kustantaja', 'biologia'],
}

response = edustore_api_call('resources', "POST", resource)
print response

# Get resource
response = edustore_api_call('resources/2a527158-3de7-6f18-1eed-ef73d13b4aaf', "GET", None)
print response


# Find resource by name, uid, link_url  
response = edustore_api_call('find?query=2a527158-3de7-6f18-1eed-ef73d13b4aaf', "GET", None)
print response


response = edustore_api_call('resources/5b2e2040-fb46-bc2f-3107-0a0123367156', "DELETE", None)
print response


uid = response['uid']
# Add resource  
resource = {
	"name" : "Some title Title2",				# Max 128 
	"description" : "Longer description 123123123123",		# Max 1024 chars 
	"is_link" : 1,								# is link or not 
	"link_url" : "test",						# Is link 
	"metadata"  : ["Koulutusaste/1. Luokka", "Koulutusaste/2. Luokka" ],	# Pre-defined metadata
	"publisher_material_id" : "test2",				# Your material id
	"comment"  : "2016-01-11",						# Your internal comment itnerval  
	"tags"  : ['maantieto', 'kustantaja', 'biologia'],
}

response = edustore_api_call('resources/' + uid, "PUT", resource)
print response


# Find resource by name, uid, link_url or comment
#response = edustore_api_call('find?query=2015-01-11', "GET", None)

