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

# localizeUtils.py
# Extracted by Gerry Weißbach 2011 http://www.gammaproduction.de
# Changes
# - extract util methods
# - add sorting of the strings files - genstrings does this, but the plist2text does not
# - improved Error messaging

from string import replace
import os, sys

from localizeUtils import *

def localize(path, STRINGS_FILE):
    languages = [name for name in os.listdir(path + os.path.sep + 'i18n') if name.endswith('.lproj') and os.path.isdir(path + os.path.sep + 'i18n' + os.path.sep + name)]

    for language in languages:
    	language = 'i18n' + os.path.sep + language
        original = merged = path + os.path.sep + language + os.path.sep + STRINGS_FILE
        old = original + '.old'
        new = original + '.new'
        
        if os.path.isfile(original):
            iconvFile(original, old)
            os.system('genstrings -q -o "%s" `find . -name "*.m"`' % language)
            iconvFile(original, new)
            merge(merged, old, new)
        else:
            os.system('genstrings -q -o "%s" `find . -name "*.m"`' % language)
            iconvFile(original, old)
            sortLocale(old, merged)

        if os.path.isfile(old):
        	os.remove(old)
        if os.path.isfile(new):
        	os.remove(new)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        localize(os.getcwd(), sys.argv[1])
    else:
        localize(os.getcwd(), 'Localizable.strings')