#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# Author : <github.com/tintinweb>


from handler.utils.filesystem import get_download_dir
import os
import json
import logging

logger = logging.getLogger(__name__)

def load_config(prefix=None):
    CONFIG_NAME = "unbox.json"
    home = os.path.expanduser("~")
    candidate_paths = [os.path.join(os.getcwd(), CONFIG_NAME),
                       os.path.join(home, CONFIG_NAME),
                       os.path.join(get_download_dir(), CONFIG_NAME)]

    if prefix:
        candidate_paths.insert(0, os.path.join(prefix, CONFIG_NAME))

    # find first matching path
    for p in candidate_paths:
        logger.debug("config: checking in %s" % p)
        if os.path.exists(p):
            break
    else:
        p = None

    if not p:
        return {}
    with open(p, 'r') as f:
        cfg = json.load(fp=f)
    return cfg
