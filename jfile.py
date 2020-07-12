import os
import threading
import time

class JFileWatcher():
	"""JHookFileWatcher object

	Object instantiation:
	To create a file watching object, you must pass in the absolute path 
	to the file you want to create a hook. It would be best if you also 
	gave in a file stat option to be watched see https://www.geeksforgeeks.org/python-os-stat-method/ 
	for reference. By default, the file option to be observed is st_mtime.

	Advanced thread daemon options:
	There is no need to set these threading options; however, they are customizable for 
	advanced configuration. Check time refers to the frequency in which the daemon monitors 
	the file selected; this must be greater than 1. You can pass in a custom change function 
	to execute when the hook triggers. By default, the change function set to None, which 
	lets the trigger event know to call the load_file_data() option as a default.
	"""
	
	def __init__(self, file_abs_path, change_function=None, file_stat_opt="st_mtime", check_time=1, logging=False):

		self.file_abs_path = file_abs_path
		self.file_stat_opt = file_stat_opt
		self.check_time = check_time
		self.change_function = change_function
		self.logging = logging
		self.running = False
		self.last_st_data = self.__load_file_stat()[file_stat_opt]
		self.data = ""
		self.daemon = None
		self.__load_file_data()

	def __load_file_data(self):
		"""Reloads contents of file into self.data..."""

		with open(self.file_abs_path, "r") as hook_file:
			self.data = hook_file.readlines()
			hook_file.close()

	def __load_file_stat(self):
		"""Loads file status and parses it for daemon use..."""

		status = os.stat(self.file_abs_path)
		return dict(st_mode=status.st_mode, st_ino=status.st_ino,
					st_dev=status.st_dev, st_nlink=status.st_nlink,
					st_uid=status.st_uid, st_gid=status.st_gid,
					st_size=status.st_size, st_atime=status.st_atime,
					st_mtime=status.st_mtime, st_ctime=status.st_ctime,
					st_atime_ns=status.st_atime_ns, st_mtime_ns=status.st_mtime_ns,
					st_ctime_ns=status.st_ctime_ns, st_blocks=status.st_blocks,
					st_rdev=status.st_rdev, st_flags=status.st_flags)

	def __check_daemon(self):
		"""Daemon function..."""

		while(self.running):
			status = self.__load_file_stat()[self.file_stat_opt]
			if status != self.last_st_data:
				self.last_st_data = status
				if self.logging:
					print(f"Change detected for file {self.file_abs_path} on status {self.file_stat_opt}")
				if self.change_function == None:
					self.__load_file_data()
				else:
					if type(self.change_function) is tuple:
						if "last_st_data" in self.change_function[1].keys():
							self.change_function[1]["last_st_data"] = self.last_st_data
						if "jfile_data" in self.change_function[1].keys():
							self.change_function[1]["jfile_data"] = self.data
						if "file_abs_path" in self.change_function[1].keys():
							self.change_function[1]["file_abs_path"] = self.data
						self.change_function[0](**self.change_function[1])
					else:
						self.change_function()
			time.sleep(self.check_time)

		if self.logging:
			print(f"Daemon ended for file {self.file_abs_path} on status {self.file_stat_opt}")

	def run_hook(self):
		"""Builds new daemon thread..."""

		self.daemon = threading.Thread(target=self.__check_daemon, name='JFileWatcher daemon')
		self.running = True
		self.daemon.start()

		if self.logging:
			print(f"File watcher started on {self.file_abs_path} on status {self.file_stat_opt}")

	def stop_hook(self):
		"""Stops currently running daemon thread..."""

		if self.running:
			self.running = False

		if self.logging:
			print(f"File watcher stopped on {self.file_abs_path} on status {self.file_stat_opt}")










