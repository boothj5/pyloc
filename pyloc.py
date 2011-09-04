#!/usr/bin/python
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
in_comment = False

# functions
def parse_opts():
    parser = OptionParser()
    parser.add_option("-v", "",
                      action="store_true", dest="verbose", default=False,
                      help="Verbose output")    

    return parser.parse_args()

def is_source(filename, language):
    result = False ;
    correct_ext = False ;

    for ext in languages[language][EXTENSIONS]:
        if filename.endswith(ext):
            correct_ext = True

    if correct_ext:
        result = True

    return result

def is_comment(line, language):
    global in_comment
    linecmnt = languages[language][LINECOMMENTS]

    if BLOCKSTART in languages[language]:
        blkstart = languages[language][BLOCKSTART]
        blkend = languages[language][BLOCKEND]

        if in_comment:
            if line.strip().endswith(blkend):
                in_comment = False
                return True

        if line.strip().startswith(blkstart) and line.strip().endswith(blkend):
            return True

        if line.strip().startswith(blkstart):
            in_comment = True
            return True

    if line.strip().startswith(linecmnt):
        return True

    if in_comment:
        return True
    
    return False

def line_type(line, language):
    if is_comment(line, language):
        return COMMENT
    elif line.strip() == "":
        return SPACE
    else:
        return CODE

def init_stats(directory, lang_stats):
    for dirname, dirnames, filenames in os.walk(directory):
        for filename in filenames:
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
    for lang in lang_stats:
        print "Language : " + lang
        print "\tFiles         : " + str(lang_stats[lang][SRC_FILES])
        print "\tCode lines    : " + str(lang_stats[lang][CODE_LINES])
        print "\tComment lines : " + str(lang_stats[lang][COMM_LINES])
        print "\tWhitespace    : " + str(lang_stats[lang][WHITESPACE])
        print
        print "\tPhysical SLOC : " + str(lang_stats[lang][TOTAL_LINES])
        print

def show_summary(lang_stats):
    print "Summary"
    print "-------"

    total_phyloc = 0
    for lang in lang_stats:
        total_phyloc = total_phyloc + lang_stats[lang][TOTAL_LINES]

    counts = []
    for lang in lang_stats:
        name = lang
        total = lang_stats[lang][TOTAL_LINES]
        counts.append((name, total))

    sorted_counts = reversed(sorted(counts, key=lambda l: l[1]))

    for lang in sorted_counts:
        name, count = lang
        print name + ': {:.2%}'.format(float(count)/total_phyloc)

    print
    print "TOTAL physical SLOC : " + str(total_phyloc)
    print

def main():
    lang_stats = {}
    (options, args) = parse_opts()
    directory = args[0]

    if not directory:
        print "You must specify a directory"
    else:
        init_stats(directory, lang_stats)
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
                show_lang_stats(lang_stats)
            show_summary(lang_stats)

if __name__ == "__main__":
    main()
