#!/usr/bin/env python
import requests

def bb_endpoint():
	return "http://196.12.53.136"

def bb_port():
	return "8000"

def bb_api():
	return "/"
	#return "/api"

def bb_hash():
	return "hash"

def bb_remote():
	return "remote"


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
	print "\n\n"
	response = requests.get(request_fmt, data=data)

	print response
	print response.text
