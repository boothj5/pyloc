#!/usr/bin/python
import os
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

# globals
in_comment = False

# functions
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
                                             WHITESPACE: 0 } 
                    lang_stats[lang][SRC_FILES] = lang_stats[lang][SRC_FILES] + 1
                    f = open(dirname + "/" + filename)
                    for line in f:
                        ltype = line_type(line, lang)
                        if ltype == CODE:
                            lang_stats[lang][CODE_LINES] = lang_stats[lang][CODE_LINES] + 1
                        elif ltype == COMMENT:
                            lang_stats[lang][COMM_LINES] = lang_stats[lang][COMM_LINES]  + 1
                        else:
                            lang_stats[lang][WHITESPACE] = lang_stats[lang][WHITESPACE] + 1

def parse_opts():
    guessed_lang = False 
    parser = OptionParser()
    parser.add_option("-d", "", dest="directory",
                      help="Directory to search")
    (options, args) = parser.parse_args()

    if not options.directory:
        parser.error("You must specify a directory, try pyloc.py -h")
    
    directory = options.directory

    return directory

def show_lang_stats(lang_stats):
    for lang in lang_stats:
        print "Language : " + lang
        print "\tFiles         : " + str(lang_stats[lang][SRC_FILES])
        print "\tCode lines    : " + str(lang_stats[lang][CODE_LINES])
        print "\tComment lines : " + str(lang_stats[lang][COMM_LINES])
        print "\tWhitespace    : " + str(lang_stats[lang][WHITESPACE])
        print
        print "\tPhysical SLOC : " + str(lang_stats[lang][CODE_LINES] + 
                                    lang_stats[lang][COMM_LINES] + 
                                    lang_stats[lang][WHITESPACE])
        print

def show_summary(lang_stats):
    total_phyloc = 0
    for lang in lang_stats:
        total_phyloc = total_phyloc + (lang_stats[lang][CODE_LINES] + 
                                      lang_stats[lang][COMM_LINES] + 
                                      lang_stats[lang][WHITESPACE])

    print "TOTAL physical SLOC : " + str(total_phyloc)
    print

def main():
    global in_comment
    lang_stats = {}
    directory = parse_opts()
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
        show_lang_stats(lang_stats)
        show_summary(lang_stats)


if __name__ == "__main__":
    main()
