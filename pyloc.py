import os
from optparse import OptionParser

def is_source(filename):
    include = False ;
    correct_ext = filename.endswith(extensions[language])
    is_test = "test" in filename or "Test" in filename
    
    if correct_ext:
        include = True
    if not tests and is_test:
        include = False   

    return include

srcfiles = 0 ;
loc = 0 ;
paths = [] ;

extensions = { "java": ".java", 
               "haskell": ".hs",
               "c": ".c",
               "python": ".py" }
comments = { "java": "//",
             "haskell": "--",
             "c": "//",
             "python": "#" }

parser = OptionParser()
parser.add_option("-d", "--directory", dest="directory",
                  help="Directory to search")
parser.add_option("-l", "--language", dest="language",
                  help="Source language")
parser.add_option("-t", "--tests",
                  action="store_true", dest="tests", default=False,
                  help="Include tests")

(options, args) = parser.parse_args()

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
        if not line.strip().startswith(comments[language]):
            loc = loc + 1         

print
print "Source files  : " + str(srcfiles)
print "Lines of code : " + str(loc)


