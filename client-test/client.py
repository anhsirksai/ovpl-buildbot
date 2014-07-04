#!/usr/bin/env python2.7
import requests

def bb_endpoint():
	return "http://196.12.53.136"

def bb_port():
	return "10000"

def bb_api():
	return "build"

def bb_hash():
	return "3534b81b3fc2598652739ac9480cd37947de0778"

def bb_remote():
	#return "https://bollu@github.com/bollu/ovpl.git"
	return "https://github.com/bollu/ovpl.git"


def is_bb_alive():
	alive = requests.get("{endpoint}:{port}/".format(endpoint=bb_endpoint(), port=bb_port()))
	return alive.status_code == 200

if __name__ == "__main__":
	print "checking if buildbot is alive.."

	if not is_bb_alive():
		print "bb is dead"
		exit()
	else:
		print "bb is alive"

	data = {"remote": bb_remote(), "hash": bb_hash()}
	request_fmt =  "{endpoint}:{port}/{api}".format(endpoint=bb_endpoint(), port=bb_port(), api=bb_api())

	print "request to: " + request_fmt
	print "data: " + str(data)
	print "\n"
	response = requests.get(request_fmt, params=data)

	print response
	print response.text
