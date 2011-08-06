#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Localize.py - Incremental localization on XCode projects
# João Moreno 2009
# http://joaomoreno.com/

# Modified by Steve Streeting 2010 http://www.stevestreeting.com
# Changes
# - Use .strings files encoded as UTF-8
#   This is useful because Mercurial and Git treat UTF-16 as binary and can't
#   diff/merge them. For use on iPhone you can run an iconv script during build to
#   convert back to UTF-16 (Mac OS X will happily use UTF-8 .strings files).
# - Clean up .old and .new files once we're done

# localize-plist.py
# Extracted by Gerry Weißbach 2011 http://www.gammaproduction.de
# Changes
# - extract util methods
# - add sorting of the strings files - genstrings does this, but the plist2text does not
# - improved Error messaging

from string import replace
import os, sys

from localizeUtils import *

def localize(self_path, path):
    plist2txt = self_path + os.path.sep + 'plist2text.sh'
    files = [name for name in os.listdir(path + os.path.sep) if name.endswith('plist') and os.path.isfile(path + os.path.sep + name)]

    for fileName in files:
        fullFileName = path + os.path.sep + fileName
        fileName = replace(fileName, '.plist', '.strings')

        languages = [name for name in os.listdir(path + os.path.sep) if name.endswith('.lproj') and os.path.isdir(path + os.path.sep + name)]
		

        for language in languages:
            language = path + os.path.sep + language
            original = merged = language + os.path.sep + fileName
			
            old = original + '.old'
            new = original + '.new'

            if os.path.isfile(original):
                os.rename(original, old)
                os.system('bash "%s" "%s" "%s"' % (plist2txt, fullFileName, original))
                os.system('iconv -f UTF-8 -t UTF-8 "%s" > "%s"' % (original, new))
                merge(merged, old, new)
            else:
                os.system('bash "%s" "%s" "%s"' % (plist2txt, fullFileName, old))
                sortLocale(old, new)
                os.system('iconv -f UTF-8 -t UTF-8 "%s" > "%s"' % (new, original))

            if os.path.isfile(old):
                os.remove(old)
            if os.path.isfile(new):
                os.remove(new)

if __name__ == '__main__':
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        print >>sys.stderr, 'Usage: python localize-plist.py path-to-plists'
        sys.exit(2)

    localize(os.path.dirname(sys.argv[0]), os.path.dirname(sys.argv[1]))