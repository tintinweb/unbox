#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Author : <github.com/tintinweb>

import subprocess
import platform
import os
import logging

logger = logging.getLogger(__name__)


class Shell:

    @staticmethod
    def test(cmd):
        if os.path.isfile(cmd):
            # just return true if it is a file ;)
            return True
        ret = subprocess.call(["where" if platform.system() == "Windows" else "which", cmd])
        logger.debug("testing for command %s returned %s" % (cmd, ret))
        return True if ret in (0, ) else False

    @staticmethod
    def execute(cmd):
        logger.debug(cmd)
        ret = subprocess.call(cmd)
        if ret != 0:
            raise Exception("command failed")
        return ret