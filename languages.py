# constants
EXTENSIONS = "extensions"
LINECOMMENTS = "linecomments"
BLOCKCOMMENTS = "blockcomments"

JAVA = "Java"
JSP = "JSP"
HASKELL = "Haskell"
PYTHON = "Python"
C = "C"
CPP = "C++"
SHELL = "Shell"
SCHEME = "Scheme"
LUA = "Lua"
XML = "XML"
JS = "Javascript"
COMMON_LISP = "Common Lisp"
RUBY = "Ruby"
SMALLTALK = "Smalltalk"

# language definitions
languages = { JAVA:
                { EXTENSIONS:    [ ".java" ] ,
                  LINECOMMENTS:  "//" ,
                  BLOCKCOMMENTS: [ ( "/*" , "*/" ) ] } ,

              JSP:
                { EXTENSIONS:    [ ".jsp" , 
                                   ".jspf" ] ,
                  LINECOMMENTS:  "//" ,
                  BLOCKCOMMENTS: [ ( "/*" , "*/" ) ,
                                   ( "<!--" , "-->" ) ] } ,

              HASKELL:
                { EXTENSIONS:    [ ".hs" ] ,
                  LINECOMMENTS:  "--" ,
                  BLOCKCOMMENTS: [ ( "{-" , "-}" ) ] } ,

              C:
                { EXTENSIONS:    [ ".c" , ".h" ] ,
                  LINECOMMENTS:  "//" ,
                  BLOCKCOMMENTS: [ ( "/*" , "*/" ) ] } ,

              CPP:
                { EXTENSIONS:    [ ".cpp" , ".hpp" ] ,
                  LINECOMMENTS:  "//" ,
                  BLOCKCOMMENTS: [ ( "/*" , "*/" ) ] } ,

              PYTHON:
                { EXTENSIONS:    [ ".py" ] ,
                  LINECOMMENTS:  "#" } ,

              SHELL:
                { EXTENSIONS:    [ ".sh" ] ,
                  LINECOMMENTS:  "#" } ,

              SCHEME:
                { EXTENSIONS:    [ ".scm" ] ,
                  LINECOMMENTS:  ";" ,
                  BLOCKCOMMENTS: [ ( "#|" , "|#" ) ] } ,

              COMMON_LISP:
                { EXTENSIONS:    [ ".lisp" , ".cl" ] ,
                  LINECOMMENTS:  ";" ,
                  BLOCKCOMMENTS: [ ( "#|" , "|#" ) ] } ,
              
              RUBY:
                { EXTENSIONS:    [ ".rb" ] ,
                  LINECOMMENTS:  "#" ,
                  BLOCKCOMMENTS: [ ( "=begin" , "=end" ) ] } ,

              JS:
                { EXTENSIONS:    [ ".js" ] ,
                  LINECOMMENTS:  "//" ,
                  BLOCKCOMMENTS: [ ( "/*" , "*/" ) ] } ,

              XML:
                { EXTENSIONS:    [ ".xml" ] ,
                  BLOCKCOMMENTS: [ ( "<!--" , "-->" ) ] } ,

              SMALLTALK:
                { EXTENSIONS:    [ ".st" ] ,
                  BLOCKCOMMENTS: [ ( "\"" , "\"" ) ] } ,

              LUA :
                { EXTENSIONS:    [ ".lua" ] ,
                  LINECOMMENTS:  "--" ,
                  BLOCKCOMMENTS: [ ( "--[[" , "]]" ) ] } }
