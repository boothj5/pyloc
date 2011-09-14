# constants
EXTENSIONS = "extensions"
LINECOMMENTS = "linecomments"
BLOCKCOMMENTS = "blockcomments"

JAVA = "Java"
JSP = "JSP"
HASKELL = "Haskell"
PYTHON = "Python"
C = "C"
SHELL = "Shell"
SCHEME = "Scheme"
LUA = "Lua"
XML = "XML"

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

              XML:
                { EXTENSIONS:    [ ".xml" ] ,
                  BLOCKCOMMENTS: [ ( "<!--" , "-->" ) ] } ,

              LUA :
                { EXTENSIONS:    [ ".lua" ] ,
                  LINECOMMENTS:  "--" ,
                  BLOCKCOMMENTS: [ ( "--[[" , "]]" ) ] } }
