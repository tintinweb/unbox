#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Author : <github.com/tintinweb>


import os
import tempfile
import commands
import urllib

import logging

logger = logging.getLogger(__name__)

from local import LocalPath
import base
from utils.filesystem import TempFile

class GitRepo(LocalPath):

    def __init__(self, source):
        self.uri = source

        self.tmp_local_file = TempFile()
        self.tmp_local_file.mkdirectory()
        source = self._fetch(source, str(self.tmp_local_file))

        LocalPath.__init__(self, source)

    def _fetch(self, source, destination, branch=None):
        ret = commands.Git.clone(source, destination, args=["--recursive"])
        # cmd = [Config.PATH_GIT, 'clone', '--recursive', source, destination]
        # ret = subprocess.call(cmd)
        # if ret != 0:
        #    raise Exception("command failed")
        return destination


class SvnRepo(LocalPath):
    def __init__(self, source):
        self.uri = source

        self.tmp_local_file = TempFile()
        self.tmp_local_file.mkdirectory()
        source = self._fetch(source, str(self.tmp_local_file))

        LocalPath.__init__(self, source)

    def _fetch(self, source, destination, branch=None):
        commands.Svn.export(source, destination)
        # cmd = [Config.PATH_SVN, 'export', source, destination]
        # ret = subprocess.call(cmd)
        # if ret != 0:
        #    raise Exception("command failed")
        return destination


class Web(LocalPath):

    def __init__(self, source):
        self.uri = source
        self.tmp_local_file = TempFile()
        self.tmp_local_file.mkfile(suffix='.' + source.rsplit('.', 1)[1])
        source = self._fetch(source, str(self.tmp_local_file))
        source = base.UniversalPath.get_path(source)
        LocalPath.__init__(self, source.path.absolute())

    def _fetch(self, source, destination):
        destination, _ = urllib.urlretrieve(source, destination)
        return destination