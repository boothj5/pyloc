#!/usr/bin/python

import os
from optparse import OptionParser

# constants
EXTENSIONS = "extensions"
LINECOMMENTS = "linecomments"
BLOCKSTART = "blockstart"
BLOCKEND = "blockend"
COUNT = "count"
JAVA = "java"
HASKELL = "haskell"
PYTHON = "python"
C = "c"

# language definitions
languages = { JAVA: 
                { EXTENSIONS:   [ ".java" ] ,
                  LINECOMMENTS: "//" ,
                  BLOCKSTART:   "/*" ,
                  BLOCKEND:     "*/" ,
                  COUNT: 0 } ,
              HASKELL:
                { EXTENSIONS:   [ ".hs" , ".lhs" ] ,
                  LINECOMMENTS: "--" ,
                  BLOCKSTART:   "{-" ,
                  BLOCKEND:     "-}"  ,
                  COUNT: 0 } ,
              C:
                { EXTENSIONS:   [ ".c" , ".h" ] ,
                  LINECOMMENTS: "//" ,
                  BLOCKSTART:   "/*" ,
                  BLOCKEND:     "*/" ,
                  COUNT: 0 } ,
              PYTHON:
                { EXTENSIONS:   [ ".py" ] ,
                  LINECOMMENTS: "#" ,
                  COUNT: 0 } } 

# globals
guessed_lang = False
srcfiles = 0
loc = 0
paths = []

# functions
def is_source(filename):
    result = False ;
    correct_ext = False ;

    for ext in languages[language][EXTENSIONS]:
        if filename.endswith(ext):
            correct_ext = True
    is_test = "test" in filename or "Test" in filename
    
    if correct_ext:
        result = True
    if not tests and is_test:
        result = False   

    return result

def is_comment(line):
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

def is_code(line):
    if is_comment(line):
        return False
    elif line.strip() == "":
        return False
    else:
        return True

def guess_lang():
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

# handle arguments
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
    language = guess_lang()
    guessed_lang = True
tests = options.tests

# main script

print
print "PYLOC"
print "-----"
print

in_comment = False

if language == None:
    print "Could not find any code!"
else:

    print "Folder   : " + directory
    guessed = "" ;

    if guessed_lang:
        guessed = " (guessed)"

    print "Language : " + language + guessed

    print "Tests    : " + str(tests)
    print

    for lang in languages:
        languages[lang][COUNT] = 0

    for dirname, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if is_source(filename):
                languages[language][COUNT] = languages[language][COUNT] + 1
                paths.append(dirname + "/" + filename)

    for path in paths:
        f = open(path)
        for line in f:
            if is_code(line):
                loc = loc + 1         

    print
    print "Source files  : " + str(languages[language][COUNT])
    print "Lines of code : " + str(loc)

print
