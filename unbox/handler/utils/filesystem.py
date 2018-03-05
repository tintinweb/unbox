#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Author : <github.com/tintinweb>

import pathlib2
import tempfile
import os, shutil
import logging

logger = logging.getLogger(__name__)


class TempFile(object):

    def __init__(self):
        self.tmp = None

    def __str__(self):
        return str(self.tmp)

    def __repr__(self):
        return repr(self.tmp)

    def mkdirectory(self, prefix="unbox", force=False):
        if self.tmp and not force:
            return self.tmp
        self.tmp = pathlib2.Path(tempfile.mkdtemp(prefix=prefix))
        return self.tmp

    def mkfile(self, prefix="", suffix="None", force=False):
        if self.tmp and not force:
            return self.tmp

        _, tempname = tempfile.mkstemp(suffix=suffix, prefix=prefix)
        os.close(_)  # close the fd, we only want that name

        self.tmp = pathlib2.Path(tempname)
        return self.tmp

    def remove(self):
        def shutil_errorhandler(function, path, excinfo):
            logger.error("could not remove path: %s (%r) (%r)" % (path, function, excinfo))

        if self.tmp:
            shutil.rmtree(str(self.tmp.absolute()), ignore_errors=False, onerror=shutil_errorhandler)


def get_download_dir():
    return os.path.join(os.path.expanduser("~"), ".unbox")