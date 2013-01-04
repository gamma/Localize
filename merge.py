#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Merge Localized Strings files
# Gerry Weißbach 2013
# http://www.gammaproduction.de


from string import replace
import os, sys, shutil

from localizeUtils import *

STRINGS_FILE = 'Localizable.strings';

def usage():
    print >>sys.stderr, 'Usage: python merge.py path-to-merge-with path-to-merge-from1 path-to-merge-from2 ...'

def mergeFiles(path, mergePath):
    
    baseLanguages = [name for name in os.listdir(path + os.path.sep) if name.endswith('.lproj') and os.path.isdir(path + os.path.sep + name)]

    for language in baseLanguages:

        if not os.path.isfile(path + os.path.sep + language + os.path.sep + STRINGS_FILE ):
            print >>sys.stderr, 'Did not find base file in Language: ', path + os.path.sep + language + os.path.sep + STRINGS_FILE
            continue

        original = path + os.path.sep + language + os.path.sep + STRINGS_FILE
        old = original + '.old'
        
        # There is no such language lproj
        if not os.path.isdir(mergePath + os.path.sep + language ):
            print >>sys.stderr, 'Did not find Language in mergePath: ', mergePath + os.path.sep + language
            continue
        
        mergeFiles = [name for name in os.listdir(mergePath + os.path.sep + language ) if name.endswith('.strings') and os.path.isfile(mergePath + os.path.sep + language + os.path.sep +name)]

        for file in mergeFiles:
            toMergeWith = mergePath + os.path.sep + language + os.path.sep + file


            print >>sys.stdout, 'Merging:', original, ' with ', toMergeWith
            destination = open(old, 'wb')
            shutil.copyfileobj(open(original, 'rb'), destination)
            shutil.copyfileobj(open(toMergeWith, 'rb'), destination)
            destination.close

            sortLocale(old, original)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage()
        sys.exit(1)

    if not os.path.isdir(sys.argv[1]):
        print >>sys.stderr, 'Base-Path "', sys.argv[1] , '" is not a directory'
        usage()
        sys.exit(1)

# Cycle through all Parameters; first is base
for i in range(2, len(sys.argv)):
    if not os.path.isdir(sys.argv[i]):
        print >>sys.stderr, 'Merge-Path ' , sys.argv[i], ' is not a directory'
        usage()
        sys.exit(1)

    mergeFiles(sys.argv[1], sys.argv[i])