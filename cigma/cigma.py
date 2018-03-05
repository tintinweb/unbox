#!/usr/bin/env python

import os
import re
import sys
import json
import string
import collections
from pprint import pprint

class Cigma:
  def __init__(self, magicfile="%s/magicbytes.json" % os.path.dirname(__file__), csvfile="%s/sigs.csv" % os.path.dirname(__file__)):
    self.filename = None
    self.data = None
    self.magic = None
    self.magicfile = magicfile
    self.sigs = self._load_json_file(self.magicfile)
    self.csvfile = csvfile
    self.result = dict({
      "source": None,
      "magic": None
    })

  # loads a json file and converts unicode key-value pairs to ascii
  def _load_json_file(self, filename):
    # http://stackoverflow.com/questions/1254454/fastest-way-to-convert-a-dicts-keys-values-from-unicode-to-str
    def unicode_to_string(data):
      if isinstance(data, basestring):
        return data.encode('utf-8')
      elif isinstance(data, collections.Mapping):
        return dict(map(unicode_to_string, data.iteritems()))
      elif isinstance(data, collections.Iterable):
        return type(data)(map(unicode_to_string, data))
      else:
        return data

    with open(filename) as jsonfile:
      return dict(unicode_to_string(json.load(jsonfile)))

  def reload_sigs(self):
    self.sigs = None
    self.sigs = self._load_json_file(self.magicfile)

  def add_sigs(self):
    data = open(self.csvfile, "r").readlines()
    for line in data:
      regex = "\\x%s" % (line.split(";")[0].strip().replace(" ", "\\x"))
      shortname = line.split(";")[1].strip()
      count = len(self.sigs["rules"]) + 1
      self.sigs["rules"].append(dict({
        "id": count,
        "longname": "",
        "mimetype": "",
        "patterns": [
          {
            "offset": 0,
            "regex": regex,
            "size": len(regex.replace("\\x", "")) / 2
          }
        ],
        "shortname": shortname
      }))
    self.sigs["meta"]["rulescount"] = len(self.sigs["rules"])

    with open(self.magicfile, "w") as fo:
      fo.write(json.dumps(self.sigs, indent=2, sort_keys=True))

  def cigma(self, data=None, filename=None):
    if data:
      self.data = data
    elif filename:
      self.filename = filename
      with open(self.filename) as fo:
        self.data = fo.read()
    else:
      raise Exception("Pass a filename or data")

    for sig in self.sigs["rules"]:
      for idx, pattern in enumerate(sig["patterns"]):
        # match upon the size bytes of data extracted from offset
        if not re.search(pattern["regex"], self.data[pattern["offset"]:pattern["offset"]+pattern["size"]]):
          # by default, all regexes in the patterns list have to match
          # we will stop matching at the first failure
          self.result["magic"] = None
          break
        else:
          # load the signature details in case this is the final regex to be matched
          self.result["magic"] = sig

      # stop testing rest of the sigs if we have already found a match
      if self.result["magic"]:
        break

    self.result["source"] = self.filename if self.filename else "databuffer"
    return self.result


if __name__ == "__main__":
  if len(sys.argv) != 2:
    print "USAGE: %s <filename>" % (sys.argv[0])
    sys.exit(1)

  # pass filename or file data via appropriate constructor argument
  # the cigma() method will read data from file (if given)
  # as such, it always works on file data
  #pprint(Cigma().cigma(filename=sys.argv[1]))

  pprint(Cigma().cigma(filename=sys.argv[1]))
