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
SHELL = "shell"

# language definitions
languages = { JAVA:
                { EXTENSIONS:   [ ".java" ] ,
                  LINECOMMENTS: "//" ,
                  BLOCKSTART:   "/*" ,
                  BLOCKEND:     "*/" ,
                  COUNT: 0 } ,
              HASKELL:
                { EXTENSIONS:   [ ".hs" ] ,
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
                  COUNT: 0 } ,
              SHELL:
                { EXTENSIONS:   [ ".sh" ] ,
                  LINECOMMENTS: "#" ,
                  COUNT: 0 } }

