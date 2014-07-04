import plumbum
import os
import glob
import imp


class TestsCollection:
	def __init__(self):
		self.info = []

	def add_test(self, name, path):
		self.info.append({"name": name, "path": path})

	def get_tests(self):
		return self.info

def get_tests(root_path):
	assert os.path.exists(root_path) and os.path.isdir(root_path)

	tests = TestsCollection()

	def filename_filter(filename):
		return filename.startswith("test-") and filename.endswith(".py")

	for root, _, filenames in os.walk(root_path):
		def add_test(filename):
			abs_path = os.path.join(root, filename)
			tests.add_test(filename, abs_path)

		map(add_test, filter(filename_filter, filenames))

	return tests


def get_test_description(testfn):
	try:
		import inspect
		desc = inspect.getcomments(testfn)
		if desc is not None:
			return str(desc)
	except Exception:
		pass


	try:
		desc = testfn.__doc__
		if desc is not None:
			return str(desc)
	except Exception:
		pass


	return "<None>"



class OVPL:
	def __init__(self, logger, repo_folder_path):
		self.logger = logger
		self.repo_path = repo_folder_path
		self.tests_path = os.path.join(self.repo_path, "scripts/")

	def test(self):
		#this will be in / wrt to OVPL directory
		tests = get_tests(self.tests_path)

		all_succeeded = True

		for test in tests.get_tests():
			filepath = test["path"]
			filename = test["name"]


			#find the relative file path of the test wrt scripts/ folder
			relpath = os.path.relpath(filepath, self.tests_path)

			self.logger.info("-")
			self.logger.info("loading test: {}".format(relpath))
			testfn = self.get_test_function(filepath, relpath)

			if not testfn:
				all_succeeded = False
			else:
				self.logger.info("test description->\n {}".format(get_test_description(testfn)))
				self.logger.info("executing test() in file: {}".format(relpath))

				all_succeeded = self.execute_test(testfn, filepath, relpath) and all_succeeded

			self.logger.info("-\n")

		return all_succeeded


	def get_test_function(self, filepath, relpath):
		testmodule = None

		try:
			testmodule = imp.load_source(relpath, filepath)
		except Exception, e:
			self.logger.error("unable to load module. file: {}".format(relpath))
			self.logger.error("exception: {}".format(e))
			#return a nil test function
			return None

		testfn = None
		try:
			testfn = getattr(testmodule, "test")
		except Exception, e:
			testfn = None
			self.logger.error("unable to find test(). file: {}".format(relpath))
			self.logger.error("exception: {}".format(e))

		return testfn



	def execute_test(self, testfn, filepath, relpath):
		def failure_string():
			return ("!{} failed---").format(relpath)

		file_dir = os.path.dirname(filepath)

		#change CWD to the script so that the script's relative paths work
		self.logger.debug("changing cwd to {}".format(file_dir))
		with plumbum.local.cwd(file_dir):
			self.logger.debug("changed cwd. pwd: {}".format(plumbum.local.cwd))

			try:
				#pass the logger to the test function
				success = testfn(self.logger)

				if not isinstance(success, bool):
					self.logger.error("!return value of test() is invalid: {}---".format(success))
					return False
				elif success:
					self.logger.info("+{} succeeded---".format(relpath))
					return True
				else:
					self.logger.error(failure_string())
					return False

			except Exception, e:
				self.logger.error("test {} threw exception".format(relpath))
				self.logger.error("exception: {}".format(e))
				self.logger.error(failure_string())
				return False

