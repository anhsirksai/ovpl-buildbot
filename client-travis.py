#!/usr/bin/env python2.7
import requests
import plumbum
import sys

def bb_endpoint():
	return "http://196.12.53.136"

def bb_port():
	return "8000"

def bb_api():
	return "build"

def bb_hash(git_sh):
	return git_sh["rev-parse"]("HEAD")

def bb_remote(git_sh):
	return git_sh["config"]["--get"]["remote.origin.url"]


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


	git_sh = plumbum.local["git"]


	data = {"remote": bb_remote(git_sh), "hash": bb_hash(git_sh)}
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