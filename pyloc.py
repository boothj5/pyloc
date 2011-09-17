#!/usr/bin/python
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
    result = ""
    for lang in lang_stats:
        result = result + lang + " (" + format_thousands(lang_stats[lang][SRC_FILES]) + " files) :\n"
        result = result + "\tCode       : " + format_thousands(lang_stats[lang][CODE_LINES]) + "\n"
        result = result + "\tComments   : " + format_thousands(lang_stats[lang][COMM_LINES]) + "\n"
        result = result + "\tWhitespace : " + format_thousands(lang_stats[lang][WHITESPACE]) + "\n"
        result = result + "\n"
        result = result +  "\tPhysical SLOC : " + format_thousands(lang_stats[lang][TOTAL_LINES]) + "\n"
        result = result + "\n"
    return result

def show_summary(lang_stats):
    result = ""
    result = result + "Summary\n"
    result = result + "-------\n"

    total_phyloc = 0
    counts = []
    for lang in lang_stats:
        total_phyloc = total_phyloc + lang_stats[lang][TOTAL_LINES]
        name = lang
        total = lang_stats[lang][TOTAL_LINES]
        counts.append((name, total))

    sorted_counts = reversed(sorted(counts, key=lambda l: l[1]))

    for lang in sorted_counts:
        name, count = lang
        result = result + name + ': {0:.2%}\n'.format(float(count)/total_phyloc)

    result = result + "\n"
    result = result + "TOTAL physical SLOC : " + format_thousands(total_phyloc) + "\n"
    result = result + "\n"
    
    return result

def format_thousands(number):
    return locale.format("%d", number, grouping=True)

def main():
    locale.setlocale(locale.LC_ALL, 'en_US')
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
                result = show_lang_stats(lang_stats)
                print(result)
            result = show_summary(lang_stats)
            print(result)

if __name__ == "__main__":
    main()
