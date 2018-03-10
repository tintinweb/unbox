#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Author : <github.com/tintinweb>

'''

Decompile the Shit out of things.

'''

import sys
import argparse
import os, glob
from distutils.dir_util import copy_tree
import logging
import handler.commands
from handler.base import UniversalPath

logger = logging.getLogger(__name__)

def auto_prompt(s, options):
    q = "\n\n[i] %s" %s
    if options.yes:
        print "%s\n<--yes"%q
        return True
    elif options.no:
        print "%s\n<--no" % q
        return False
    yn = raw_input(q).strip()
    if yn=="y":
        return True
    return False

def cmd_extract(options):
    ret = 0
    for fglob in glob.glob(options.args[0]):
        dst = UniversalPath(fglob)
        try:
            for p in dst.files.walk():
                print p.path
            if len(options.args) >= 2:
                if os.path.exists(options.args[1]) and \
                        auto_prompt("Destination %s already exists. Overwrite? [y|n]" % options.args[1], options):
                    copy_tree(str(dst.files.path), options.args[1])
                    logger.info("moved files to %s" % options.args[1])
        finally:
            logger.debug("--cleanup--")
            if os.path.exists(str(dst.files.path)):
                logger.debug("deleting tempfolder")
                dst.files.unlink()
            ret = 1
    logger.info("--done--")
    return ret


def cmd_list(options):
    for fglob in glob.glob(options.args[0]):
        dst = UniversalPath(fglob)
        try:
            for p in dst.files.walk():
                print p.path
        finally:
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
                       -y, --yes    ...   answer prompts with yes
                       -n, --no     ...   answer prompts with no

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
        parser.add_argument("-y", "--yes",
                            action="store_true",
                            dest="yes", default=False,
                            help="answer prompts with yes")
        parser.add_argument("-n", "--n",
                            action="store_true",
                            dest="no", default=False,
                            help="answer prompts with no")
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