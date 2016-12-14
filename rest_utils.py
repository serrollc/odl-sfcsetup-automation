#!/usr/bin/python
import requests,json
from requests.auth import HTTPBasicAuth
import time


def put(host, port, username, password, uri, data, debug=False):
    '''Perform a PUT rest operation, using the URL and data provided'''

    url='http://'+host+":"+port+uri

    headers = {'Content-type': 'application/yang.data+json',
               'Accept': 'application/yang.data+json'}
    if debug == True:
        print "PUT %s" % url
        print json.dumps(data, indent=4, sort_keys=True)
    r = requests.put(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(username, password))
    if debug == True:
        print r.text
    r.raise_for_status()
    time.sleep(5)

def post(host, port, username, password, uri, data, debug=False):
    '''Perform a POST rest operation, using the URL and data provided'''

    url='http://'+host+":"+port+uri
    headers = {'Content-type': 'application/yang.data+json',
               'Accept': 'application/yang.data+json'}
    if debug == True:
        print "POST %s" % url
        print json.dumps(data, indent=4, sort_keys=True)
    r = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(username, password))
    if debug == True:
        print r.text
    r.raise_for_status()
    time.sleep(5)

def delete(host, port, username, password, uri, data, debug=False):
    '''Perform a DELETE rest operation, using the URL and data provided'''

    url='http://'+host+":"+port+uri

    headers = {'Content-type': 'application/yang.data+json',
               'Accept': 'application/yang.data+json'}
    if debug == True:
        print "DELETE %s" % url
        print json.dumps(data, indent=4, sort_keys=True)
    r = requests.delete(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(username, password))
    if debug == True:
        print r.text
    r.raise_for_status()
    time.sleep(5)
