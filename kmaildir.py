#
# Copyright 2017 Steve Miller (copart)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

__author__ = 'Steve Miller (copart)'

import os
import mailbox

__all__ = [ 'Kmaildir' ]

class Kmaildir(mailbox.Maildir):

	def list_folders(self):
		"""Return a list of folder names."""
		result = []
		path = os.path.join(os.path.dirname(self._path),".{}.directory".format(os.path.basename(self._path)))
		if os.path.isdir(path):
			for entry in os.listdir(path):
				if entry[0] != '.' and \
				   os.path.isdir(os.path.join(os.path.dirname(self._path),".{}.directory".format(os.path.basename(self._path)), entry)):
					result.append(entry)
		return result

	def get_folder(self, folder):
		"""Return a Maildir instance for the named folder."""
		return Kmaildir(os.path.join(os.path.dirname(self._path),".{}.directory".format(os.path.basename(self._path)), folder), factory=self._factory,	create=False)
	
	def add_folder(self, folder):
		"""Create a folder and return a Maildir instance representing it."""
		path = os.path.join(os.path.dirname(self._path),".{}.directory".format(os.path.basename(self._path)))

		if not os.path.isdir(path):
			os.makedirs(path)

		path = os.path.join(path,folder)
		result = Kmaildir(path, factory=self._factory)
		return result

	def remove_folder(self, folder):
		"""Delete the named folder, which must be empty."""
		print ( self._path)
		path = os.path.join(os.path.dirname(self._path),".{}.directory".format(os.path.basename(self._path)),folder)

		subpath = os.path.join(os.path.dirname(self._path),".{}.directory".format(os.path.basename(self._path)),".{}.directory".format(folder))

		for entry in os.listdir(os.path.join(path, 'new')) + \
					 os.listdir(os.path.join(path, 'cur')):
			if len(entry) < 1 or entry[0] != '.':
				raise mailbox.NotEmptyError('Folder contains message(s): %s' % folder)
		if os.path.isdir(subpath) and len(os.listdir(subpath)) > 0:
			raise mailbox.NotEmptyError("Folder contains at least one subdirectory: %s" % (folder))
		for root, dirs, files in os.walk(path, topdown=False):
			for entry in files:
				os.remove(os.path.join(root, entry))
			for entry in dirs:
				os.rmdir(os.path.join(root, entry))
		if os.path.isdir(subpath):
			os.rmdir(subpath)	
		os.rmdir(path)
