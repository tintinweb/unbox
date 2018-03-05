#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Author : <github.com/tintinweb>

from unbox import config
import subprocess
import os
import hashlib
import logging


logger = logging.getLogger(__name__)

CONFIG = config.load_config("..")

from ..utils.shell import Shell
from ..utils.web import download_file
from ..utils.filesystem import get_download_dir


class Git:
    @staticmethod
    def _is_available():
        '''
        Download missing parts or provide instructions on how to do so
        :return:
        '''
        if not Shell.test(Git._get_command()):
            print "=" * 30
            print "=   Please install the >git< command line tools and add them to the PATH variable or configure the specific path in unbox.cfg.json "
            print "=" * 30
            return False
        return True

    @staticmethod
    def _get_command():
        cmd = CONFIG.get("tools",{}).get("git",{}).get("executable","git")
        return cmd

    @staticmethod
    def clone(source, destination, args=[]):
        cmd = [Git._get_command(), 'clone'] + args + [source, destination]
        return Shell.execute(cmd)


class Svn:
    @staticmethod
    def _is_available():
        '''
        Download missing parts or provide instructions on how to do so
        :return:
        '''
        if not Shell.test(Svn._get_command()):
            print "=" * 30
            print "=   Please install the >svn< command line tools and add them to the PATH variable or configure the specific path in unbox.cfg.json "
            print "=" * 30
            return False
        return True

    @staticmethod
    def _get_command():
        cmd = CONFIG.get("tools", {}).get("svn", {}).get("executable", "svn")
        return cmd

    @staticmethod
    def export(source, destination):
        cmd = [Svn._get_command(), 'export', source, destination]
        return Shell.execute(cmd)


class P7Zip:
    """
        @title: 7zip archiver
        @ref: http://www.7-zip.org/
    """

    @staticmethod
    def _is_available():
        '''
        Download missing parts or provide instructions on how to do so
        :return:
        '''
        if not Shell.test(P7Zip._get_command()):
            print "=" * 30
            print "=   Please install the >7zip< command line tools and add them to the PATH variable or configure the specific path in unbox.cfg.json "
            print "=" * 30
            return False
        return True

    @staticmethod
    def _get_command():
        cmd = CONFIG.get("tools", {}).get("7zip", {}).get("executable", "7z")
        return cmd

    @staticmethod
    def extract(source, destination):
        cmd = [P7Zip._get_command(), 'x', '-o%s' % destination, source]
        return Shell.execute(cmd)


class JdCli:
    """
        @title: Command line Java Decompiler
        @ref: https://github.com/kwart/jd-cmd
    """

    @staticmethod
    def _is_available():
        '''
        Download missing parts or provide instructions on how to do so
        :return:
        '''
        if not Shell.test(JdCli._get_command()):
            print "=" * 30
            print "=   Please install the >jd-cli< command line tools and add them to the PATH variable or configure the specific path in unbox.cfg.json "
            print "=" * 30
            return False
        return True

    @staticmethod
    def _get_command():
        cmd = CONFIG.get("tools", {}).get("jd-cli", {}).get("executable", "jd-cli")
        return cmd

    @staticmethod
    def decompile(source, destination):
        cmd = [JdCli._get_command(), '--outputDir', destination, source]
        return Shell.execute(cmd)


class Dex2Jar:
    """
        @title: dextools dex2jar
        @ref: https://github.com/pxb1988/dex2jar
    """

    @staticmethod
    def _is_available():
        '''
        Download missing parts or provide instructions on how to do so
        :return:
        '''
        if not Shell.test(Dex2Jar._get_command()):
            print "=" * 30
            print "=   Please install the >dex2jar< command line tools and add them to the PATH variable or configure the specific path in unbox.cfg.json "
            print "=" * 30
            return False
        return True

    @staticmethod
    def _get_command():
        cmd = CONFIG.get("tools", {}).get("dex2jar", {}).get("executable", "d2j-dex2jar")
        return cmd

    @staticmethod
    def decompile(source, destination):
        cmd = [Dex2Jar._get_command(), '-o', destination, source]
        return Shell.execute(cmd)


class JustDecompileDotNet:
    """
        @title: The decompilation engine of JustDecompile http://www.telerik.com/products/decompiler.aspx
        @ref: https://github.com/telerik/JustDecompileEngine
    """

    @staticmethod
    def _is_available():
        '''
        Download missing parts or provide instructions on how to do so
        :return:
        '''
        if not Shell.test(JustDecompileDotNet._get_command()):
            print "=" * 30
            print "=   Please install the >JustDecompileDotNet< command line tools and add them to the PATH variable or configure the specific path in unbox.cfg.json "
            print "=" * 30
            return False
        return True

    @staticmethod
    def _get_command():
        cmd = CONFIG.get("tools", {}).get("just_decompile_engine", {}).get("executable")
        return cmd

    @staticmethod
    def decompile(source, destination):
        cmd = [JustDecompileDotNet._get_command(), '/out:%s' % destination, '/target:%s' % source]
        return Shell.execute(cmd)


class Ida32:
    """
        @title: Hex-Ray's IDA x64 batch decompiler
        @ref: https://github.com/tintinweb/ida-batch_decompile
    """
    SUPPORT_SCRIPT = ("https://raw.githubusercontent.com/tintinweb/ida-batch_decompile/v0.1/ida_batch_decompile.py",
                      "SHA-1",
                      "694ae11e3502bc0d017c194b0f54fd377c0276d3")


    @staticmethod
    def _is_available():
        '''
        Download missing parts or provide instructions on how to do so
        :return:
        '''
        if not Shell.test(Ida32._get_command()):
            print "=" * 30
            print "=   Please install the >IDA Pro including Hexrays Decompiler< command line tools and add them to the PATH variable or configure the specific path in unbox.cfg.json "
            print "=" * 30
            return False

        if not os.path.exists(os.path.join(get_download_dir(), "ida_batch_decompile.py")):
            yn = raw_input("Download '%s'? [y|n]" % Ida32.SUPPORT_SCRIPT[0])
            if yn.strip() == "n":
                return False
            dl = Ida32.SUPPORT_SCRIPT[0]
            file = download_file(dl, get_download_dir())
        else:
            file = os.path.join(get_download_dir(), "ida_batch_decompile.py")
        with open(file, 'rb') as f:
            this_hash = hashlib.sha1()
            this_hash.update(f.read())
            if not Ida32.SUPPORT_SCRIPT[2] == this_hash.hexdigest():
                raise Exception("Checksum Failed for ida_batch_decompile.py!")
            #raise Exception("requests download file")

        return True

    @staticmethod
    def _get_command():
        cmd = CONFIG.get("tools", {}).get("ida32", {}).get("executable","idaw")
        return cmd

    @staticmethod
    def decompile(source, destination):
        idascript = os.path.abspath(os.path.join(get_download_dir(), "ida_batch_decompile.py"))
        destination_file = os.path.join(destination, os.path.split(source)[1].rsplit(".", 1)[0] + '.c')

        decompile_script_cmd = '%s -o\\"%s\\"' % (idascript, destination_file)
        cmd = [Ida32._get_command(), '-B', '-M', '-S"%s"' % decompile_script_cmd, '"' + source + '"']
        logger.debug(cmd)
        ret = subprocess.call(' '.join(cmd), shell=True)
        # ret = subprocess.call(cmd, shell=True)
        # subprocess.call()
        if ret != 0:
            raise Exception("command failed: %s" % ret)
        return destination


class Ida64:
    """
        @title: Hex-Ray's IDA x64 batch decompiler
        @ref: https://github.com/tintinweb/ida-batch_decompile
    """

    @staticmethod
    def _is_available():
        '''
        Download missing parts or provide instructions on how to do so
        :return:
        '''
        if not Shell.test(Ida64._get_command()):
            print "=" * 30
            print "=   Please install the >IDA Pro including Hexrays Decompiler< command line tools and add them to the PATH variable or configure the specific path in unbox.cfg.json "
            print "=" * 30
            return False

        if not os.path.exists(os.path.join(get_download_dir(), "ida_batch_decompile.py")):
            yn = raw_input("Download '%s'? [y|n]" % Ida32.SUPPORT_SCRIPT[0])
            if yn.strip() == "n":
                return False
            dl = Ida32.SUPPORT_SCRIPT[0]
            file = download_file(dl, get_download_dir())
        else:
            file = os.path.join(get_download_dir(), "ida_batch_decompile.py")
        with open(file, 'rb') as f:
            this_hash = hashlib.sha1()
            this_hash.update(f.read())
            if not Ida32.SUPPORT_SCRIPT[2] == this_hash.hexdigest():
                raise Exception("Checksum Failed for ida_batch_decompile.py!")
            #raise Exception("requests download file")

        return True

    @staticmethod
    def _get_command():
        cmd = CONFIG.get("tools", {}).get("ida64", {}).get("executable", "idaw64")
        return cmd

    @staticmethod
    def decompile(source, destination):
        idascript = os.path.abspath(os.path.join(get_download_dir(), "ida_batch_decompile.py"))
        destination_file = os.path.join(destination, os.path.split(source)[1].rsplit(".", 1)[0] + '.c')

        decompile_script_cmd = '%s -o\\"%s\\"' % (idascript, destination_file)
        cmd = [Ida64._get_command(), '-B', '-M', '-S"%s"' % decompile_script_cmd, '"' + source + '"']
        logger.debug(cmd)
        ret = subprocess.call(' '.join(cmd), shell=True)
        # ret = subprocess.call(cmd, shell=True)
        # subprocess.call()
        if ret != 0:
            raise Exception("command failed: %s" % ret)
        return destination


class RetDec:
    """
        @title: RetDec is a retargetable machine-code decompiler based on LLVM. https://retdec.com/
        @ref: # https://github.com/avast-tl/retdec
    """

    @staticmethod
    def _is_available():
        '''
        Download missing parts or provide instructions on how to do so
        :return:
        '''
        if not Shell.test(RetDec._get_command()):
            print "=" * 30
            print "=   Please install the >RETDEC< command line tools and add them to the PATH variable or configure the specific path in unbox.cfg.json "
            print "=" * 30
            return False

        return True

    @staticmethod
    def _get_command():
        cmd = CONFIG.get("tools", {}).get("retdec", {}).get("executable", "retdec")
        return cmd

    @staticmethod
    def decompile(source, destination):
        pass


class Porosity:
    """
        @title: Decompiler and Security Analysis tool for Blockchain-based Ethereum Smart-Contracts https://www.comae.io
        @ref: # https://github.com/comaeio/porosity
    """

    @staticmethod
    def _is_available():
        '''
        Download missing parts or provide instructions on how to do so
        :return:
        '''
        if not Shell.test(Porosity._get_command()):
            print "=" * 30
            print "=   Please install the >Porosity< command line tools and add them to the PATH variable or configure the specific path in unbox.cfg.json "
            print "=" * 30
            return False

        return True

    @staticmethod
    def _get_command():
        cmd = CONFIG.get("tools", {}).get("porosity", {}).get("executable", "porosity")
        return cmd

    @staticmethod
    def decompile(source, destination):
        # porosity --abi $abi --code $code --decompile --verbose 0 > output.sol
        pass

