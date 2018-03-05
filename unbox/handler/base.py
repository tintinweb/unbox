#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Author : <github.com/tintinweb>



import local, remote, archive, decompilable
from utils.fileformat import PeFileFormat
import urlparse
import os
from cigma.cigma import Cigma


import logging

logger = logging.getLogger(__name__)


class UniversalPath(object):

    def __init__(self, source):
        self.source = source
        self._files = None

    @property
    def files(self):
        self._files = self._files or UniversalPath.get_path(self.source)
        return self._files

    @staticmethod
    def get_path(source):
        uri = urlparse.urlparse(source)

        if uri.scheme and uri.path.endswith(".git"):
            po = remote.GitRepo(source)
        elif uri.scheme.startswith("svn"):
            po = remote.SvnRepo(source)
        elif uri.scheme in ("http", "https", "ftp"):
            po = remote.Web(source)
        elif os.path.isfile(source):
            if any(source.endswith(ext) for ext in ('.zip', '.gz', '.tar')):
                po = archive.Archive(source)
            elif source.endswith('.crx'):
                po = archive.ChromeExtensionCrx(source)
            elif source.endswith('.xpi'):
                po = archive.FirefoxExtensionXpi(source)
            elif source.endswith('.apk'):
                po = decompilable.Apk(source)
            elif source.endswith('.jar'):
                po = decompilable.Jar(source)
            else:
                # we do not know what is is
                logger.debug("unknown: %s" % source)
                c = Cigma()
                try:
                    with open(source, 'rb') as f:
                        data = f.read(384)
                        magic = c.cigma(data=data)
                        logger.debug(magic)
                        d_magic = magic["magic"]
                        if not d_magic:
                            po = local.LocalPath(source)
                        else:
                            mimetype = d_magic.get('mimetype', "")
                            if mimetype.startswith("application/x-executable-32"):
                                po = decompilable.Application32Bits(source)
                            elif mimetype.startswith("application/x-executable-64"):
                                po = decompilable.Application64Bits(source)
                            elif mimetype.startswith("application/"):
                                petype = PeFileFormat.petype(data)
                                logger.debug(petype)
                                if petype == PeFileFormat.TYPE_PE64:
                                    po = decompilable.Application64Bits(source)
                                elif petype == PeFileFormat.TYPE_DOTNET:
                                    po = decompilable.ApplicationDotNet(source)
                                else:
                                    po = decompilable.Application32Bits(source)
                            else:
                                po = local.LocalPath(source)
                except Exception as e:
                    logger.exception("exception!")
                    po = local.LocalPath(source)
        elif os.path.isdir(source):
            po = local.LocalPath(source)

        logger.debug("scheme: %s" % uri.scheme)
        logger.debug(po)
        return po











