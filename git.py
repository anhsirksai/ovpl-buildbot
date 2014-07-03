import plumbum
from plumbum import FG, BG
import shutil
import os


import pbhelper

class Git:
	def __init__(self, logger, remote, repo_folder_path):
		assert isinstance(repo_folder_path, str)
		assert isinstance(remote, str)
		self.logger = logger
		self.repo_path = repo_folder_path

		self.git_sh = plumbum.local["git"]

		#delete the folder if it exists
		if os.path.isdir(repo_folder_path):
			self.logger.debug("{} exists. hard restting".format(repo_folder_path))

			with plumbum.local.cwd(self.repo_path):
				self.logger.info("changed cwd. pwd: {}".format(plumbum.local.cwd))
				self.git_sh["reset", "--hard", "HEAD^"]

			return

			# self.logger.info("{} exists. deleting...".format(repo_folder_path))
			# delete_cmd = shutil.rmtree(repo_folder_path, ignore_errors=True)
			# self.logger.info("{} deleted".format(repo_folder_path))

		#construct the clone command and pipe output to foreground
		clone_cmd = self.git_sh["clone", remote, repo_folder_path]
		logger.info("clone command: {}".format(clone_cmd))
		clone_cmd & FG



	def checkout(self, git_hash):
		assert isinstance(git_hash, str)

		checkout_cmd = self.git_sh["checkout"]#git_hash]

		self.logger.info("changing cwd to {}...".format(self.repo_path))
		#change path to the repo path and then run checkout
		with plumbum.local.cwd(self.repo_path):
			self.logger.info("changed cwd. pwd: {}".format(plumbum.local.cwd))

			self.logger.info("checkout command: {}".format(checkout_cmd))
			self.logger.info("checking out {} ...".format(git_hash))

			checkout_cmd(git_hash)

			self.logger.info("checked out {}".format(git_hash))
