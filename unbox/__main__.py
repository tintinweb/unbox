#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Author : <github.com/tintinweb>

import cli
import sys
import logging

logger = logging.getLogger("unbox")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="[%(name)s/%(process)s][%(levelname)-10s] [%(module)s.%(funcName)-14s] %(message)s")
    sys.exit(cli.main()())
