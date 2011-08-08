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

from sys import argv
from codecs import open
from re import compile
from copy import copy
import os

re_translation = compile(r'^"(.+)" = "(.*)";$')
re_comment_single = compile(r'^/\*.*\*/$')
re_comment_start = compile(r'^/\*.*$')
re_comment_end = compile(r'^.*\*/$')

class LocalizedString():
    def __init__(self, comments, translation):
        self.comments, self.translation = comments, translation
        self.key, self.value = re_translation.match(self.translation).groups()
        self.lowerKey = self.key.lower();

    def __unicode__(self):
        return u'%s%s\n' % (u''.join(self.comments), self.translation)

    def __eq__(self, other):
        return self.lowerKey==other.lowerKey

    def __hash__(self):
        return hash(('key', self.lowerKey))

class LocalizedFile():
    def __init__(self, fname=None, auto_read=False):
        self.fname = fname
        self.strings = []
        self.strings_d = {}

        if auto_read:
            self.read_from_file(fname)

    def read_from_file(self, fname=None):
        fname = self.fname if fname == None else fname
        try:
            f = open(fname, encoding='utf_8', mode='r')
        except:
            print 'File %s does not exist.' % fname
            exit(-1)

        line = f.readline()
        while line:
            comments = [line]

            if not re_comment_single.match(line):
                while line and not re_comment_end.match(line):
                    line = f.readline()
                    comments.append(line)

            line = f.readline()
            if line and re_translation.match(line):
                translation = line
            else:
                raise Exception('input file %s have invalid format\n"%s"' % (fname, line))

            line = f.readline()
            while line and line == u'\n':
                line = f.readline()

            string = LocalizedString(comments, translation)
            self.strings.append(string)
            self.strings_d[string.key] = string

        f.close()

    def save_to_file(self, fname=None):
        fname = self.fname if fname == None else fname
        try:
            f = open(fname, encoding='utf_8', mode='w')
        except:
            raise Exception('Couldn\'t open file %s.' % fname)
            exit(-1)

        for string in self.strings:
            f.write(string.__unicode__())

        f.close()

    def merge_with(self, new):
        merged = LocalizedFile()

        for string in set(new.strings):
            if self.strings_d.has_key(string.key):
                new_string = copy(self.strings_d[string.key])
                new_string.comments = string.comments
                string = new_string

            merged.strings.append(string)
            merged.strings_d[string.key] = string

        return merged

    def sort(self):
        self.strings = sorted(list(set(self.strings)), key=lambda LocalizedString: LocalizedString.lowerKey)
        return self
 
def merge(merged_fname, old_fname, new_fname):
    
    print 'Merging into file %s' % merged_fname
    try:
        old = LocalizedFile(old_fname, auto_read=True)
        new = LocalizedFile(new_fname, auto_read=True)
        try:
            merged = old.merge_with(new)
            merged.sort().save_to_file(merged_fname)
        except Exception, e:
            print 'cannot merge with Error: %s' %e
    except Exception, e:
        print 'Error in file: %s' % merged_fname
        print 'Error: %s' % e
        os.rename(old_fname, merged_fname)
        exit(-1)

def sortLocale(old_fname, new_fname):

    print 'Sorting file %s' % old_fname
    try:
        old = LocalizedFile(old_fname, auto_read=True)
        old.sort().save_to_file(new_fname)
    except Exception, e:
        print 'Error in file: %s' % old_fname
        print 'Error: %s' % e
        os.rename(old_fname, merged_fname)
        exit(-1)

def iconvFile(old_fname, new_fname):
    os.system('iconv -f `file -I %s | awk -F= \'{OFS="="; print toupper($2)}\'` -t UTF-8 "%s" > "%s"' % (old_fname, old_fname, new_fname))
