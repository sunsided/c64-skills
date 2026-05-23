> Source: c64prg.txt §Appendix D "Screen and Color Memory Maps". Lightly cleaned from the Project 64 etext.

  APPENDIX D

  SCREEN AND COLOR MEMORY MAPS

    The following charts list which memory locations control placing char-
  acters on the screen, and the locations used to change individual char-
  acter colors, as well as showing character color codes.

                             SCREEN MEMORY MAP

                                   COLUMN                             1063
        0             10             20             30            39 /
       +------------------------------------------------------------/
  1024 |                                                            |  0
  1064 |                                                            |
  1104 |                                                            |
  1144 |                                                            |
  1184 |                                                            |
  1224 |                                                            |
  1264 |                                                            |
  1304 |                                                            |
  1344 |                                                            |
  1384 |                                                            |
  1424 |                                                            | 10
  1464 |                                                            |
  1504 |                                                            |   ROW
  1544 |                                                            |
  1584 |                                                            |
  1624 |                                                            |
  1664 |                                                            |
  1704 |                                                            |
  1744 |                                                            |
  1784 |                                                            |
  1824 |                                                            | 20
  1864 |                                                            |
  1904 |                                                            |
  1944 |                                                            |
  1984 |                                                            | 24
       +------------------------------------------------------------\
                                                                     \
                                                                      2023

    The actual values to POKE into a color memory location to change a
  character's color are:

             0  BLACK   4  PURPLE     8  ORANGE     12  GRAY 2
             1  WHITE   5  GREEN      9  BROWN      13  Light GREEN
             2  RED     6  BLUE      10  Light RED  14  Light BLUE
             3  CYAN    7  YELLOW    11  GRAY 1     15  GRAY 3

    For example, to change the color of a character located at the upper
  left-hand corner of the screen to red, type: POKE 55296,2.

                              COLOR MEMORY MAP
                                   COLUMN                             55335
        0             10             20             30            39 /
       +------------------------------------------------------------/
  55296|                                                            |  0
  55336|                                                            |
  55376|                                                            |
  55416|                                                            |
  55456|                                                            |
  55496|                                                            |
  55536|                                                            |
  55576|                                                            |
  55616|                                                            |
  55656|                                                            |
  55696|                                                            | 10
  55736|                                                            |
  55776|                                                            |   ROW
  55816|                                                            |
  55856|                                                            |
  55896|                                                            |
  55936|                                                            |
  55976|                                                            |
  56016|                                                            |
  56056|                                                            |
  56096|                                                            | 20
  56136|                                                            |
  56176|                                                            |
  56216|                                                            |
  56256|                                                            | 24
       +------------------------------------------------------------\
                                                                     56295
