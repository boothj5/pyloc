#!/usr/bin/python
# 
# pylocstats.py
#
# Copyright (C) 2012 James Booth <boothj5@gmail.com>
# 
# This file is part of Pyloc.
#
# Pyloc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyloc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pyloc.  If not, see <http://www.gnu.org/licenses/>.

import locale
import os
import sys
import operator
from optparse import OptionParser

from languages import *

# constants
CODE = 1
COMMENT = 2
SPACE = 3

SRC_FILES = "src_files"
CODE_LINES = "code_lines"
COMM_LINES = "comm_lines"
WHITESPACE = "whitespace"
TOTAL_LINES = "total_lines"

# globals
in_comment = ""

# functions
def parse_opts():
    parser = OptionParser()
    parser.add_option("-v", "",
                      action="store_true", dest="verbose", default=False,
                      help="Verbose output")    

    return parser.parse_args()

def is_source(filename, lang):
    for ext in languages[lang][EXTENSIONS]:
        if filename.endswith(ext):
            return True
    return False

def is_comment(line, lang):
    global in_comment

    if BLOCKCOMMENTS in languages[lang]:
        for blockstart, blockend in languages[lang][BLOCKCOMMENTS]:
            if in_comment == blockstart:
                if line.strip().endswith(blockend):
                    in_comment = ""
                    return True

            if line.strip().startswith(blockstart) and line.strip().endswith(blockend):
                return True

            if line.strip().startswith(blockstart):
                in_comment = blockstart
                return True

    if LINECOMMENTS in languages[lang]:
        linecmnt = languages[lang][LINECOMMENTS]
        if line.strip().startswith(linecmnt):
            return True

    if in_comment:
        return True
    
    return False

def line_type(line, lang):
    if is_comment(line, lang):
        return COMMENT
    elif line.strip() == "":
        return SPACE
    else:
        return CODE

def init_stats(directory, lang_stats):
    count = 0
    for dirname, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            count += 1
            yield count
            basename, extension = os.path.splitext(filename)
            for lang in languages:
                if extension in languages[lang][EXTENSIONS]:
                    if not lang in lang_stats:
                        lang_stats[lang] = { SRC_FILES: 0 , 
                                             CODE_LINES: 0 , 
                                             COMM_LINES: 0 ,
                                             WHITESPACE: 0 ,
                                             TOTAL_LINES: 0 } 
                    lang_stats[lang][SRC_FILES] = lang_stats[lang][SRC_FILES] + 1
                    process_file(dirname + "/" + filename, lang, lang_stats)

def process_file(full_path, lang, lang_stats):
    f = open(full_path)
    for line in f:
        lang_stats[lang][TOTAL_LINES] = lang_stats[lang][TOTAL_LINES] + 1
        ltype = line_type(line, lang)
        if ltype == CODE:
            lang_stats[lang][CODE_LINES] = lang_stats[lang][CODE_LINES] + 1
        elif ltype == COMMENT:
            lang_stats[lang][COMM_LINES] = lang_stats[lang][COMM_LINES]  + 1
        else:
            lang_stats[lang][WHITESPACE] = lang_stats[lang][WHITESPACE] + 1

def show_lang_stats(lang_stats):
    result = ""
    for lang in lang_stats:
        result += lang + " (" + format_thousands(lang_stats[lang][SRC_FILES]) + " files) :\n"
        result += "\tCode       : " + format_thousands(lang_stats[lang][CODE_LINES]) + "\n"
        result += "\tComments   : " + format_thousands(lang_stats[lang][COMM_LINES]) + "\n"
        result += "\tWhitespace : " + format_thousands(lang_stats[lang][WHITESPACE]) + "\n\n"
        result += "\tPhysical SLOC : " + format_thousands(lang_stats[lang][TOTAL_LINES]) + "\n\n"
    return result

def calc_total(lang_stats):
    total = 0
    for lang in lang_stats:
        total += lang_stats[lang][TOTAL_LINES]
    return total

def show_summary(lang_stats):
    result = "Summary\n-------\n"
    
    total_phyloc = calc_total(lang_stats)

    counts = []
    for lang in lang_stats:
        counts.append((lang, lang_stats[lang][TOTAL_LINES]))

    sorted_counts = reversed(sorted(counts, key=lambda l: l[1]))

    for lang in sorted_counts:
        name, count = lang
        result += name + ': {0:.2%}\n'.format(float(count)/total_phyloc)

    result += "\nTOTAL physical SLOC : " + format_thousands(total_phyloc) + "\n\n"
    
    return result

def format_thousands(number):
    return locale.format("%d", number, grouping=True)

def main():
    locale.setlocale(locale.LC_ALL, '')
    lang_stats = {}
    (options, args) = parse_opts()
    directory = args[0]

    if not directory:
        print "You must specify a directory"
    else:
        for _ in init_stats(directory, lang_stats) : pass
        print
        print "PYLOC"
        print "-----"
        print "Folder   : " + directory
        print
        if not lang_stats:
            print "Could not find any code!"
            print
        else:
            if options.verbose:
                result = show_lang_stats(lang_stats)
                print(result)
            result = show_summary(lang_stats)
            print(result)

if __name__ == "__main__":
    main()
