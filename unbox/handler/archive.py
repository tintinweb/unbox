#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Author : <github.com/tintinweb>

from local import LocalPath
from utils.filesystem import TempFile
import patoolib
import commands
import logging

logger = logging.getLogger(__name__)

patoolib.ArchivePrograms.update({
    'crx': {
        'extract': ('7z',),
        'test': ('7z',),
        'list': ('7z',),
    },
})


class Archive(LocalPath):
    def __init__(self, source, destination=None):
        self.uri = source
        if not destination:
            self.tmp_local_file = TempFile()
            self.tmp_local_file.mkdirectory()
            destination = self._fetch(source, str(self.tmp_local_file))

        source = self._fetch(source, destination)
        LocalPath.__init__(self, source)

    def _fetch(self, source, destination):
        commands.P7Zip.extract(source, destination)
        # cmd = [Config.PATH_7ZIP, 'x', '-o%s' % destination, source]
        # logger.debug(cmd)
        # ret = subprocess.call(cmd)
        # if ret != 0:
        #    raise Exception("command failed")
        return destination


class ArchivePatool(LocalPath):
    def __init__(self, source, destination=None):
        self.uri = source
        destination = destination or self.mkdtemp()
        source = self._fetch(source, destination)
        LocalPath.__init__(self, source)

    def _fetch(self, source, destination, verbosity=-1, interactive=True):
        patoolib.extract_archive(source, verbosity=verbosity,
                                 interactive=interactive,
                                 outdir=destination)
        return destination


class ChromeExtensionCrx(ArchivePatool):
    pass  # just an ordinary zip archive

class FirefoxExtensionXpi(ArchivePatool):
    pass  # just an ordinary zip archive