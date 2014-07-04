#!/usr/bin/env python2.7
import requests
import sys

def bb_endpoint():
	return "http://196.12.53.136"

def bb_port():
	return "8000"

def bb_api():
	return "build"

def bb_hash():
	return "8d9427ccb17b0a9d38947133292aa649ffe4b4d5"

def bb_remote():
	#return "https://bollu@github.com/bollu/ovpl.git"
	return "https://github.com/bollu/ovpl.git"


def is_bb_alive():
	try:
		alive = requests.get("{endpoint}:{port}/".format(endpoint=bb_endpoint(), port=bb_port()))
		return alive.status_code == 200
	except Exception, e:
		print "\vbuildbot ping"
		print e
		return False

if __name__ == "__main__":
	print "checking if buildbot is alive.."

	if not is_bb_alive():
		print "bb is dead"
		exit(1)
	else:
		print "bb is alive"

	data = {"remote": bb_remote(), "hash": bb_hash()}
	request_fmt =  "{endpoint}:{port}/{api}".format(endpoint=bb_endpoint(), port=bb_port(), api=bb_api())

	print "request to: " + request_fmt
	print "data: " + str(data)
	print "\n"

	try:
		response = requests.get(request_fmt, params=data)
	except Exception, e:
		print "\nrequest failed"
		print e
		exit(1)

	print "response: {}".format(response)
	print "response text: {}".format(response.text)
	print "\n"

	if response.status_code == 200:
		print "tests passed"
		exit(0)
	else:
		print "tests failed"
		exit(1)