#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Author : <github.com/tintinweb>

'''

Decompile the Shit out of things.

'''

import sys
import argparse
import logging
import handler.commands
from handler.base import UniversalPath

logger = logging.getLogger(__name__)


def cmd_extract(options):
    dst = UniversalPath(options.args[0])
    try:
        for p in dst.files.walk():
            print p.path
    finally:
        pass
       #dst.files.unlink()
    return 0


def cmd_list(options):
    dst = UniversalPath(options.args[0])
    try:
        for p in dst.files.walk():
            print p.path
    finally:
        pass
        dst.files.unlink()
    return 0


def cmd_check(options):

    for name, cls in handler.commands.__dict__.iteritems():
        f_isAvailable = getattr(cls, "_is_available", None)
        f_isAvailable and f_isAvailable()


COMMANDS = {
    'list': cmd_list,
    'extract': cmd_extract,
    'check-dependencies': cmd_check,
}

def main():
    usage = """poc.py [options]
              example: poc.py <command> [options] <target> [<target>, ...]
              options:

              command  ... list <target>
                       ... extract <target> <destination path>

                       ... check-dependencies

              target   ... file
                       """
    if len(sys.argv) <= 1:
        print "invalid command.\n"
        print usage
        return 1

    command = sys.argv.pop(1)   # pop command arg
    if len(sys.argv) <= 1 and command == "check-dependencies":
        options = {}
    else:
        # parse the rest
        parser = argparse.ArgumentParser(usage=usage)
        parser.add_argument("-v", "--verbose",
                            action="store_true",
                            dest="verbose", default=False,
                            help="verbose output")
        parser.add_argument("-u", "--unpack",
                            action="store_true",
                            dest="unpack", default=False,
                            help="unpack/decompile file")
        parser.add_argument("-c", "--decompile",
                            action="store_true",
                            dest="decompile", default=False,
                            help="decompile")
        parser.add_argument("args", nargs="+")

        options = parser.parse_args()

        if options.verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

    logger.debug("start")

    f_cmd = COMMANDS.get(command.lower())
    if not f_cmd:
        print "invalid command.\n"
        print usage
        return 1

    return f_cmd(options)

    return 0

if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG, format="[%(name)s/%(process)s][%(levelname)-10s] [%(module)s.%(funcName)-14s] %(message)s")
    sys.exit(main())