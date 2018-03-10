#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Author : <github.com/tintinweb>

from utils.filesystem import TempFile
import base
import pathlib2
import codecs, chardet
import os
import shutil
import re
import logging

logger = logging.getLogger(__name__)


class LocalPath(object):
    def __init__(self, source):
        self.encoding = None
        self.fd = None
        self.source = source
        self.path = pathlib2.Path(source)
        self.tmp = TempFile()

    def __repr__(self):
        return "<%s encoding=%r path=%r>"% (self.__class__.__name__, self.encoding, self.path)

    def open(self):
        ''' open file from fs
        '''
        self.fd = codecs.open(str(self.path.absolute()), mode='r')
        # probe for encoding
        self.encoding = chardet.detect(self.fd.read(512))
        self.fd.seek(0)  # rewind
        return self.fd

    def close(self):
        if self.fd:
            self.fd.close()

    def read(self):
        return self.fd.read()

    def walk(self, exclude_rex=[re.compile(r'.*/.git.*'), ], include_rex=[]):
        logger.debug("walk: %s"%self.path.absolute())
        for root, _, files in os.walk(str(self.path.absolute())):
            for filename in files:
                abspath = os.path.join(root, filename)
                normalized_abspath = abspath.replace("\\", '//')
                if not any(regex.match(normalized_abspath) for regex in include_rex):
                    # if we do not want to force inclusion, check exclusion list
                    if any(regex.match(normalized_abspath) for regex in exclude_rex):
                        continue
                gp = base.UnboxPath.get_path(abspath)
                if gp.path.is_file():
                    yield gp
                elif gp.path.is_dir():
                    # recurse into subpath
                    for sub_f in gp.walk():
                        yield sub_f

    def remove(self):
        def shutil_errorhandler(function, path, excinfo):
            logger.error("could not remove path: %s (%r) (%r)" % (path, function, excinfo))

        self.close()
        if self.path.is_dir():
            shutil.rmtree(str(self.path.absolute()), ignore_errors=False, onerror=shutil_errorhandler)
        else:
            self.path.unlink()

    def unlink(self):
        self.remove()