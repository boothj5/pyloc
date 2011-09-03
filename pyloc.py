#!/usr/bin/python
import os
from optparse import OptionParser

from languages import *

# globals
in_comment = False

# functions
def is_source(filename, language, include_tests):
    result = False ;
    correct_ext = False ;

    for ext in languages[language][EXTENSIONS]:
        if filename.endswith(ext):
            correct_ext = True
    is_test = "test" in filename.lower()

    if correct_ext:
        result = True
    if not include_tests and is_test:
        result = False   

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

def is_code(line, language):
    if is_comment(line, language):
        return False
    elif line.strip() == "":
        return False
    else:
        return True

def guess_lang(directory):
    for dirname, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            basename, extension = os.path.splitext(filename) ;
            for lang in languages:
                if extension in languages[lang][EXTENSIONS]:
                    languages[lang][COUNT] = languages[lang][COUNT] + 1

    result = None
    highest = 0

    for lang in languages:
        if languages[lang][COUNT] > highest:
            result = lang ;
            highst = languages[lang][COUNT]
    
    return result

def parse_opts():
    guessed_lang = False 
    parser = OptionParser()
    parser.add_option("-d", "", dest="directory",
                      help="Directory to search")
    parser.add_option("-l", "", dest="language",
                      help="Source language (java, haskell, python, c), will guess if not specified")
    parser.add_option("-t", "",
                      action="store_true", dest="tests", default=False,
                      help="Include tests")
    (options, args) = parser.parse_args()

    if not options.directory:
        parser.error("You must specify at least a directory, try pyloc.py -h")
    directory = options.directory

    if options.language:
        language = options.language
    else:
        language = guess_lang(directory)
        guessed_lang = True

    include_tests = options.tests

    return (directory, language, guessed_lang, include_tests)

def main():
    global in_comment
    loc = 0 
    paths = []
    (directory, language, guessed_lang, include_tests) = parse_opts()
    in_comment = False

    print
    print "PYLOC"
    print "-----"
    print
    if language == None:
        print "Could not find any code!"
    else:
        for lang in languages:
            languages[lang][COUNT] = 0

        for dirname, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                if is_source(filename, language, include_tests):
                    languages[language][COUNT] = languages[language][COUNT] + 1
                    paths.append(dirname + "/" + filename)

        for path in paths:
            f = open(path)
            for line in f:
                if is_code(line, language):
                    loc = loc + 1         

        print "Folder   : " + directory
        print "Language : " + language + (lambda g : " (guessed)" if g else "")(guessed_lang)
        print "Tests    : " + str(include_tests)
        print
        print
        print "Source files  : " + str(languages[language][COUNT])
        print "Lines of code : " + str(loc)
    print

if __name__ == "__main__":
    main()
