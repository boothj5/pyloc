#!/usr/bin/python

import os
from optparse import OptionParser

EXTENSIONS = "extensions"
LINECOMMENTS = "linecomments"
JAVA = "java"
HASKELL = "haskell"
PYTHON = "python"
C = "c"

languages = { JAVA: 
                { EXTENSIONS:   [ ".java" ] ,
                  LINECOMMENTS: [ "//", "/*", "*", "*/" ] } ,
              HASKELL:
                { EXTENSIONS:   [ ".hs" , ".lhs" ] ,
                  LINECOMMENTS: [ "--" ] } ,
              C:
                { EXTENSIONS:   [ ".c" , ".h" ] ,
                  LINECOMMENTS: [ "//" ] } ,
              PYTHON:
                { EXTENSIONS:   [ ".py" ] ,
                  LINECOMMENTS: [ "#" ] } } 

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
    for comment in languages[language][LINECOMMENTS]:
        if line.strip().startswith(comment):
            return True
    return False

srcfiles = 0 ;
loc = 0 ;
paths = [] ;

parser = OptionParser()
parser.add_option("-d", "", dest="directory",
                  help="Directory to search")
parser.add_option("-l", "", dest="language",
                  help="Source language, (java, haskell, python, c)")
parser.add_option("-t", "",
                  action="store_true", dest="tests", default=False,
                  help="Include tests")

(options, args) = parser.parse_args()

if not options.directory and not options.language:
    parser.error("You must specify at least a directory and language, try pyloc.py -h")

directory = options.directory
language = options.language
tests = options.tests

print "Folder = " + directory
print "Language = " + language
print "Tests = " + str(tests)
print

for dirname, dirnames, filenames in os.walk(directory):
    for filename in filenames:
        if is_source(filename):
            srcfiles = srcfiles + 1
            paths.append(dirname + "/" + filename)

print "Files:"

for path in paths:
    print path

for path in paths:
    f = open(path)
    for line in f:
        if not is_comment(line):
            loc = loc + 1         

print
print "Source files  : " + str(srcfiles)
print "Lines of code : " + str(loc)


