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

			self.logger.info("loading test: {}".format(relpath))
			testfn = self.get_test_function(filepath, relpath)

			if not testfn:
				all_succeeded = False
			else:
				self.logger.debug("executing test() in file: {}".format(relpath))
				all_succeeded = self.execute_test(testfn, relpath) and all_succeeded

			self.logger.info("-------\n")

		return all_succeeded


	def get_test_function(self, filepath, relpath):
		testmodule = None

		try:
			testmodule = imp.load_source("name", filepath)
		except Exception, e:
			self.logger.error("unable to load module. file: {}".format(relpath))
			self.logger.error("exception: {}".format(e))
			#return a nil test function
			return None

		testfn = None
		try:
			testfn = getattr(testmodule, "test")
		except Exception, e:
			test_fn = None
			self.logger.error("unable to find test(). file: {}".format(relpath))
			self.logger.error("exception: {}".format(e))

		return testfn



	def execute_test(self, testfn, relpath):
		try:
			#pass the logger to the test function
			success = testfn(self.logger)

			if not isinstance(success, bool):
				self.logger.error("---return value of test() is invalid: {}---".format(success))
				return False
			elif success:
				self.logger.info("---test succeeded!---")
				return True
			else:
				return False
				self.logger.error("---test failed---")

		except Exception, e:
			return False
			self.logger.error("test {} threw exception".format(relpath))
			self.logger.error("exception: {}".format(e))

