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


def guess_lang(lang_stats):
    result = None
    highest = 0

    for lang in lang_stats:
        if lang_stats[lang][SRC_FILES] > highest:
            result = lang ;
            highest = lang_stats[lang][SRC_FILES]
    
    return result

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
        print "LANG : " + lang
        print "\tfiles: " + str(lang_stats[lang][SRC_FILES])
        print "\tSrc lines : " + str(lang_stats[lang][CODE_LINES])
        print "\tcmnt lines : " + str(lang_stats[lang][COMM_LINES])
        print "\twht lines : " + str(lang_stats[lang][WHITESPACE])

def main():
    global in_comment

    lang_stats = {}

    code_lines = 0
    comment_lines = 0
    whitespace = 0 
    paths = []
    directory = parse_opts()
    in_comment = False
    init_stats(directory, lang_stats)
    language = guess_lang(lang_stats)
    show_lang_stats(lang_stats)

    print
    print "PYLOC"
    print "-----"
    print
    if language == None:
        print "Could not find any code!"
    else:
        for dirname, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                if is_source(filename, language):
                    paths.append(dirname + "/" + filename)

        for path in paths:
            f = open(path)
            for line in f:
                ltype = line_type(line, language)
                if ltype == CODE:
                    code_lines = code_lines + 1
                elif ltype == COMMENT:
                    comment_lines = comment_lines + 1
                else:
                    whitespace = whitespace + 1          

        print "Folder   : " + directory
        print "Language : " + language
        print
        print
        print "Source files      : " + str(lang_stats[language][SRC_FILES])
        print "Lines of code     : " + str(code_lines)
        print "Lines of comments : "  + str(comment_lines)
        print "Whitespace        : " + str(whitespace)
        print
        print "Physical SLOC : " + str(code_lines + comment_lines + whitespace)
    print

if __name__ == "__main__":
    main()
