#!/usr/bin/env python2.7
import custom_logging
import config
import ovpl
import git

import sys
import os
from flask import Flask, request, make_response

app = Flask(__name__)
logger = None

def construct_clone_path(git_hash):
	return str(os.path.join(os.path.abspath("./repos/"), git_hash))

@app.route("/build", methods=["GET"])
def build_endpoint():
	git_hash = request.args.get("hash")
	git_remote = request.args.get("remote")


	logger.info("git hash: {}".format(git_hash))
	logger.info("git remote: {}".format(git_remote))

	if git_hash == None:
		return make_response("git hash not sent"), 400
	if git_remote == None:
		return make_response("git remote not sent"), 400


	git_hash_str = str(git_hash).strip()
	git_remote_str = str(git_remote).strip()

	git_clone_path = construct_clone_path(git_hash)
	ovpl_repo = git.Git(logger=logger, remote=git_remote_str, repo_folder_path=git_clone_path)
	logger.info("cloning succeeded. Now checking out version {}".format(git_hash_str))
	ovpl_repo.checkout(git_hash_str)

	logger.info("starting OVPL tests...")
	ovpl_instance = ovpl.OVPL(logger=logger, repo_folder_path=git_clone_path)
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


