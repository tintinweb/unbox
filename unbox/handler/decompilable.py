#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Author : <github.com/tintinweb>

from local import LocalPath
from archive import ArchivePatool
Archive = ArchivePatool  # lets use PaTool
import os
import commands
from utils.filesystem import TempFile
import logging

logger = logging.getLogger(__name__)


class Jar(LocalPath):
    def __init__(self, source, destination=None):
        self.uri = source
        if not destination:
            self.tmp_local_file = TempFile()
            self.tmp_local_file.mkdirectory()
            destination = str(self.tmp_local_file)

        source = self._fetch(source, destination)
        LocalPath.__init__(self, source)

    def _fetch(self, source, destination):
        commands.JdCli.decompile(source, destination)
        # cmd = [Config.PATH_JAR2SRC, '--outputDir', destination, source]
        # logger.debug(cmd)
        # ret = subprocess.call(cmd)
        # if ret != 0:
        #    raise Exception("command failed")
        return destination


class ApplicationDotNet(LocalPath):
    def __init__(self, source, destination=None):
        self.uri = source
        if not destination:
            self.tmp_local_file = TempFile()
            self.tmp_local_file.mkdirectory()
            destination = str(self.tmp_local_file)

        source = self._fetch(source, destination)
        LocalPath.__init__(self, source)

    def _fetch(self, source, destination):
        commands.JustDecompileDotNet.decompile(source, destination)
        return destination


class Apk(LocalPath):
    def __init__(self, source):
        self.uri = source
        self.tmp_local_file = TempFile()
        self.tmp_local_file.mkdirectory()

        source = self._fetch(source, str(self.tmp_local_file))
        LocalPath.__init__(self, source)

    def _fetch(self, source, destination):
        '''
        1) create tempfolder
        2) unpack .apk to tempfolder .apk
        3) convert .apk to tempfolder .jar
        4) decompile .jar to tempfolder .java

        dex2jar -o <output_jar> <input_apk>

        '''
        path, fname = os.path.split(source)

        destination_jar = os.path.join(destination, fname + ".jar")
        logger.debug("destination: %s" % destination_jar)
        # 1) convert .apk to .jar
        commands.Dex2Jar.decompile(source, destination_jar)
        # cmd = [Config.PATH_DEX2JAR, '-o', destination_jar, source]
        # logger.debug(cmd)
        # ret = subprocess.call(cmd)
        # if ret != 0:
        #    raise Exception("command failed")

        # 2) unpack .apk
        destination_dir_apk = os.path.join(destination, '.apk')
        os.makedirs(destination_dir_apk)
        logger.debug("unpack .apk to %s" % destination_dir_apk)
        apk_unpacked = Archive(source, destination_dir_apk)
        # 3) decompile .jar
        destination_dir_source = os.path.join(destination, '.source')
        os.makedirs(destination_dir_source)
        logger.debug("decompile .jar to %s" % destination_dir_source)
        jar_decompiled = Jar(destination_jar, destination_dir_source)

        logger.debug("remove .jar - we do not need it anymore")
        os.unlink(destination_jar)
        return destination


class Application32Bits(LocalPath):  # ida32
    # https://www.hex-rays.com/products/ida/support/idadoc/417.shtml
    """
    https://www.hex-rays.com/products/ida/support/idadoc/417.shtml

    idc.wait()
    idaapi.decompile_many(outfile, None, flags=0xffffffff)

    see idaallthethings
    + https://www.hex-rays.com/products/ida/support/idadoc/417.shtml
    1) get os type (windows,linux) (idaw vs idal)
    2) idaw -B -S"myscript.idc argument1 \"argument 2\" argument3"

    idaw|idal -B -S"ida-allthethings.py" "C:\_tmp\telnet.exe"

    https://www.hex-rays.com/products/decompiler/manual/batch.shtml
    """

    def __init__(self, source):
        self.uri = source
        self.tmp_local_file = TempFile()
        self.tmp_local_file.mkdirectory()

        source = self._fetch(source, str(self.tmp_local_file))
        LocalPath.__init__(self, source)

    def _fetch(self, source, destination, branch=None):
        commands.Ida32.decompile(source, destination)
        '''
        idascript = os.path.abspath(r'ida-allthethings.py')
        print (destination)
        destination_file = os.path.join(destination, os.path.split(source)[1].rsplit(".", 1)[0] + '.c')

        decompile_script_cmd = '%s \\"%s\\"' % (idascript, destination_file)
        cmd = [Config.PATH_IDA32, '-B', '-M', '-S"%s"' % decompile_script_cmd, '"' + source + '"']
        logger.debug(cmd)
        print (' '.join(cmd))
        ret = subprocess.call(' '.join(cmd), shell=True)
        # ret = subprocess.call(cmd, shell=True)
        # subprocess.call()
        if ret != 0:
            raise Exception("command failed: %s" % ret)
        '''
        return destination


class Application64Bits(LocalPath):
    def __init__(self, source):
        self.uri = source
        self.tmp_local_file = TempFile()
        self.tmp_local_file.mkdirectory()

        source = self._fetch(source, str(self.tmp_local_file))
        LocalPath.__init__(self, source)

    def _fetch(self, source, destination, branch=None):
        commands.Ida64.decompile(source, destination)
        return destination

class SoliditySmartContract(LocalPath):
    def __init__(self, source):
        self.uri = source
        self.tmp_local_file = TempFile()
        self.tmp_local_file.mkdirectory()

        source = self._fetch(source, str(self.tmp_local_file))
        LocalPath.__init__(self, source)

    def _fetch(self, source, destination, branch=None):
        commands.Porosity.decompile(source, destination)
        return destination
