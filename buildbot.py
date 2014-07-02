#!/usr/bin/env python2.7
import custom_logging
import config
import ovpl

import sys
from flask import Flask, request, make_response

app = Flask(__name__)
logger = None


@app.route("/build", methods=["GET"])
def build_endpoint():
	git_hash = request.args.get("hash")
	git_remote = request.args.get("remote")

	if git_hash == None:
		return make_response("git hash not sent"), 400
	if git_remote == None:
		return make_response("git remote not sent"), 400


	ovpl_instance = ovpl.OVPLInstance(git_hash, git_remote)

	success = ovpl_instance.test()

	if success:
		return make_response("build & test successful"), 200
	else:
		return make_response("build & test unsucessful"), 400

	return "success"
@app.route("/")
def slash_endpoint():
	return "you're trying to reach buildbot. try and use /build ?"

if __name__ == "__main__":
	#logging
	def logger_path():
		import os
		return os.path.join(os.path.dirname(os.path.abspath(__file__)), "log/build-log.log")

	def is_debug():
		return len(sys.argv) >= 2 and sys.argv[1] == "--debug"


	logger = custom_logging.create_logger("buildbot", logger_path(), is_debug())
	logger.info("logging is up")

	if is_debug():
		app.debug = True
	app.run(port=config.get_app_port(), host="0.0.0.0")


