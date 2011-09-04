# constants
EXTENSIONS = "extensions"
LINECOMMENTS = "linecomments"
BLOCKSTART = "blockstart"
BLOCKEND = "blockend"

JAVA = "Java"
HASKELL = "Haskell"
PYTHON = "Python"
C = "C"
SHELL = "Shell"
SCHEME = "Scheme"
LUA = "Lua"

# language definitions
languages = { JAVA:
                { EXTENSIONS:   [ ".java" ] ,
                  LINECOMMENTS: "//" ,
                  BLOCKSTART:   "/*" ,
                  BLOCKEND:     "*/" } ,
              HASKELL:
                { EXTENSIONS:   [ ".hs" ] ,
                  LINECOMMENTS: "--" ,
                  BLOCKSTART:   "{-" ,
                  BLOCKEND:     "-}" } ,
              C:
                { EXTENSIONS:   [ ".c" , ".h" ] ,
                  LINECOMMENTS: "//" ,
                  BLOCKSTART:   "/*" ,
                  BLOCKEND:     "*/" } ,
              PYTHON:
                { EXTENSIONS:   [ ".py" ] ,
                  LINECOMMENTS: "#" } ,
              SHELL:
                { EXTENSIONS:   [ ".sh" ] ,
                  LINECOMMENTS: "#" } ,
              SCHEME:
                { EXTENSIONS:   [ ".scm" ] ,
                  LINECOMMENTS: ";" ,
                  BLOCKSTART:   "#|" ,
                  BLOCKEND:     "|#" } ,
              LUA :
                { EXTENSIONS:   [ ".lua" ] ,
                  LINECOMMENTS: "--" ,
                  BLOCKSTART:   "--[[" ,
                  BLOCKEND:     "]]" } }

