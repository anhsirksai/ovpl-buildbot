import plumbum
from plumbum import FG, BG
import shutil
import os


class Git:
	def __init__(self, logger, remote, repo_folder_path, git_hash):
		assert isinstance(repo_folder_path, str)
		assert isinstance(remote, str)
		assert isinstance(git_hash, str)

		self.logger = logger
		self.repo_path = repo_folder_path
		self.hash = git_hash

		self.git_sh = plumbum.local["git"]

		#delete the folder if it exists
		if os.path.isdir(repo_folder_path):
			self.logger.debug("repo exists. reseting {} to base".format(repo_folder_path))

			with plumbum.local.cwd(self.repo_path):
				self.logger.debug("changed cwd. pwd: {}".format(plumbum.local.cwd))
				reset_command = self.git_sh["reset", "--hard", "HEAD^"]

			return

			# self.logger.info("{} exists. deleting...".format(repo_folder_path))
			# delete_cmd = shutil.rmtree(repo_folder_path, ignore_errors=True)
			# self.logger.info("{} deleted".format(repo_folder_path))

		#construct the clone command and pipe output to foreground
		clone_cmd = self.git_sh["clone", remote, repo_folder_path]
		logger.debug("clone command: {}".format(clone_cmd))
		clone_cmd & FG



	def checkout(self):

		checkout_cmd = self.git_sh["checkout"]#git_hash]

		self.logger.debug("changing cwd to {}...".format(self.repo_path))
		#change path to the repo path and then run checkout
		with plumbum.local.cwd(self.repo_path):
			self.logger.debug("changed cwd. pwd: {}".format(plumbum.local.cwd))

			self.logger.debug("checkout command: {}".format(checkout_cmd))
			self.logger.debug("checking out {} ...".format(self.hash))

			checkout_cmd(self.hash)

			self.logger.debug("checked out {}".format(self.hash))
