#!/usr/bin/env python
import custom_logging
import sys

def logger_path():
	import os
	return os.path.join(os.path.dirname(os.path.abspath(__file__)), "log/build-log.log")

def log_to_stdout():
	return len(sys.argv) >= 2 and sys.argv[1] == "--debug"

if __name__ == "__main__":
	logger = custom_logging.create_logger("buildbot", logger_path(), log_to_stdout())
	logger.info("logging is up")
