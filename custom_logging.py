#!/usr/bin/env python2.7
import os
import logging
from logging.handlers import TimedRotatingFileHandler, MemoryHandler
import sys
import StringIO


def __create_formatter__():
	return logging.Formatter(
			'%(asctime)s - %(levelname)s : [%(filename)s:%(lineno)d] : %(message)s',
			datefmt='%Y-%m-%d %I:%M:%S %p')

def create_logger(name, file_path, should_log_stdout):
	directory = os.path.dirname(file_path)
	#if the directory does not exist, create it
	if not os.path.exists(directory):
		os.makedirs(directory)

	logger = BuildbotLogger(logging.getLogger(name))

	logger.setLevel(logging.DEBUG)

	# Add the log message handler to the logger
	timed_rotating_handler = TimedRotatingFileHandler(
								file_path, when='midnight', backupCount=5)

	logger.addHandler(timed_rotating_handler)

	if should_log_stdout or True:
		rainbow_handler = RainbowLoggingHandler(sys.stdout)
		logger.addHandler(rainbow_handler)

	logger.info("-New Log-")

	return logger


class BuildbotLogger:
	def __init__(self, logger):
		self.logger = logger

		self.formatter = __create_formatter__()

		self.logged_string = StringIO.StringIO()
		self.stream_handler = logging.StreamHandler(self.logged_string)
		self.stream_handler.setFormatter(self.formatter)

		logger.addHandler(self.stream_handler)

	def get_logged_string(self):
		return self.logged_string.getvalue()

	def clear_logged_string(self):
		#self.logged_string = StringIO.StringIO()
		#self.stream_handler.setTarget(self.logged_string)
		self.stream_handler.flush()
		self.logged_string.seek(0)
		self.logged_string.truncate(0)

	def setLevel(self, level):
		self.logger.setLevel(level)

	def hasNoHandlers(self):
		return len(self.logger.handlers) == 0

	def addHandler(self, handler):
		handler.setFormatter(self.formatter)
		self.logger.addHandler(handler)

	def info(self, string):
		self.logger.info(string)

	def debug(self, string):
		self.logger.debug(string)

	def warn(self, string):
		self.logger.warn(string)

	def error(self, string):
		self.logger.error(string)


from logutils.colorize import ColorizingStreamHandler
class RainbowLoggingHandler(ColorizingStreamHandler):
	""" A colorful logging handler optimized for terminal debugging aestetichs.

	- Designed for diagnosis and debug mode output - not for disk logs

	- Highlight the content of logging message in more readable manner

	- Show function and line, so you can trace where your logging messages
	  are coming from

	- Keep timestamp compact

	- Extra module/function output for traceability

	The class provide few options as member variables you
	would might want to customize after instiating the handler.
	"""

	# Define color for message payload
	level_map = {
		logging.DEBUG: (None, 'cyan', False),
		logging.INFO: (None, 'white', False),
		logging.WARNING: (None, 'yellow', True),
		logging.ERROR: (None, 'red', True),
		logging.CRITICAL: ('red', 'white', True),
	}

	#date_format = "%H:%m:%S"
	date_format = "%Y-%m-%d %I:%M:%S %p"
	#: How many characters reserve to function name logging
	who_padding = 40

	#: Show logger name
	show_name = True

	def get_color(self, fg=None, bg=None, bold=False):
		"""
		Construct a terminal color code

		:param fg: Symbolic name of foreground color

		:param bg: Symbolic name of background color

		:param bold: Brightness bit
		"""
		params = []
		if bg in self.color_map:
			params.append(str(self.color_map[bg] + 40))
		if fg in self.color_map:
			params.append(str(self.color_map[fg] + 30))
		if bold:
			params.append('1')

		color_code = ''.join((self.csi, ';'.join(params), 'm'))

		return color_code

	def colorize(self, record):
		"""
		Get a special format string with ASCII color codes.
		"""

		# Dynamic message color based on logging level
		if record.levelno in self.level_map:
			fg, bg, bold = self.level_map[record.levelno]
		else:
			# Defaults
			bg = None
			fg = "white"
			bold = False

		# Magician's hat
		# https://www.youtube.com/watch?v=1HRa4X07jdE
		template = [
			"[",
			self.get_color("white", None, True),
			"%(asctime)s",
			self.reset,
			"] ",
			self.get_color("white", None, True) if self.show_name else "",
			"%(name)s " if self.show_name else "",
			"%(padded_who)s",
			self.reset,
			" ",
			self.get_color(bg, fg, bold),
			"%(message)s",
			self.reset,
		]

		format = "".join(template)

		who = [self.get_color("green"),
			   getattr(record, "filename", ""),
			   ": ",
			   getattr(record, "funcName", ""),
			   "()",
			   self.get_color("black", None, True),
			   ":",
			   self.get_color("cyan"),
			   str(getattr(record, "lineno", 0))]

		who = "".join(who)

		# We need to calculate padding length manualy
		# as color codes mess up string length based calcs
		unformatted_who = str(getattr(record, "filename", "")) + \
			    ": " + getattr(record, "funcName", "") + "()" + \
			":" + str(getattr(record, "lineno", 0))

		if len(unformatted_who) < self.who_padding:
			spaces = " " * (self.who_padding - len(unformatted_who))
		else:
			spaces = ""

		record.padded_who = who + spaces

		formatter = logging.Formatter(format, self.date_format)
		self.colorize_traceback(formatter, record)
		output = formatter.format(record)
		# Clean cache so the color codes of traceback don't leak to other formatters
		record.ext_text = None
		return output

	def colorize_traceback(self, formatter, record):
		"""
		Turn traceback text to red.
		"""
		if record.exc_info:
			# Cache the traceback text to avoid converting it multiple times
			# (it's constant anyway)
			record.exc_text = "".join([
				self.get_color("red"),
				formatter.formatException(record.exc_info),
				self.reset,
			])

	def format(self, record):
		"""
		Formats a record for output.

		Takes a custom formatting path on a terminal.
		"""
		if self.is_tty:
			message = self.colorize(record)
		else:
			message = logging.StreamHandler.format(self, record)

		return message