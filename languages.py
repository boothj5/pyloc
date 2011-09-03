# constants
EXTENSIONS = "extensions"
LINECOMMENTS = "linecomments"
BLOCKSTART = "blockstart"
BLOCKEND = "blockend"

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
                  LINECOMMENTS: "#" } }

