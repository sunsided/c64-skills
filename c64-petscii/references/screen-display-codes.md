> Source: c64prg.txt Appendix B, "Screen Display Codes". Lightly cleaned from the Project 64 etext.

  SCREEN DISPLAY CODES

    The following chart lists all of the characters built into the
  Commodore 64 character sets. It shows which numbers should be POKED into
  screen memory (locations 1024-2023) to get a desired character. Also
  shown is which character corresponds to a number PEEKed from the screen.
    Two character sets are available, but only one set at a time. This
  means that you cannot have characters from one set on the screen at the
  same time you have characters from the other set displayed. The sets are
  switched by holding down the <SHIFT> and <C=> keys simultaneously.
    From BASIC, POKE 53272,21 will switch to upper case mode and
  POKE 53272,23 switches to lower case.
    Any number on the chart may also be displayed in REVERSE. The reverse
  character code may be obtained by adding 128 to the values shown.
    If you want to display a solid circle at location 1504, POKE the code
  for the circle (81) into location 1504: POKE 1504,81.
    There is a corresponding memory location to control the color of each
  character displayed on the screen (locations 55296-56295). To change the
  color of the circle to yellow (color code 7) you would POKE the corre-
  sponding memory location (55776) with the character color: POKE 55776,7.
    Refer to Appendix D for the complete screen and color memory maps,
  along with color codes.

  +-----------------------------------------------------------------------+
  | NOTE: The following POKEs display the same symbol in set 1 and 2: 1,  |
  | 27-64, 91-93, 96-104, 106-121, 123-127.                               |
  +-----------------------------------------------------------------------+


  SCREEN CODES

    SET 1   SET 2   POKE  |  SET 1   SET 2   POKE  |  SET 1   SET 2   POKE
  ------------------------+------------------------+-----------------------
                          |                        |
      @               0   |    C       c       3   |    F       f       6
      A       a       1   |    D       d       4   |    G       g       7
      B       b       2   |    E       e       5   |    H       h       8


    SET 1   SET 2   POKE  |  SET 1   SET 2   POKE  |  SET 1   SET 2   POKE
  ------------------------+------------------------+-----------------------
                          |                        |
      I       i       9   |    %              37   |            A      65
      J       j      10   |    &              38   |            B      66
      K       k      11   |    '              39   |            C      67
      L       l      12   |    (              40   |            D      68
      M       m      13   |    )              41   |            E      69
      N       n      14   |    *              42   |            F      70
      O       o      15   |    +              43   |            G      71
      P       p      16   |    ,              44   |            H      72
      Q       q      17   |    -              45   |            I      73
      R       r      18   |    .              46   |            J      74
      S       s      19   |    /              47   |            K      75
      T       t      20   |    0              48   |            L      76
      U       u      21   |    1              49   |            M      77
      V       v      22   |    2              50   |            N      78
      W       w      23   |    3              51   |            O      79
      X       x      24   |    4              52   |            P      80
      Y       y      25   |    5              53   |            Q      81
      Z       z      26   |    6              54   |            R      82
      [              27   |    7              55   |            S      83
    pound            28   |    8              56   |            T      84
      ]              29   |    9              57   |            U      85
      ^              30   |    :              58   |            V      86
      <-             31   |    ;              59   |            W      87
    SPACE            32   |    <              60   |            X      88
      !              33   |    =              61   |            Y      89
      "              34   |    >              62   |            Z      90
      #              35   |    ?              63   |                   91
      $              36   |                   64   |                   92


    SET 1   SET 2   POKE  |  SET 1   SET 2   POKE  |  SET 1   SET 2   POKE
  ------------------------+------------------------+-----------------------
                          |                        |
                     93   |                  105   |                  117
                     94   |                  106   |                  118
                     95   |                  107   |                  119
    SPACE            96   |                  108   |                  120
                     97   |                  109   |                  121
                     98   |                  110   |                  122
                     99   |                  111   |                  123
                    100   |                  112   |                  124
                    101   |                  113   |                  125
                    102   |                  114   |                  126
                    103   |                  115   |                  127
                    104   |                  116   |

            Codes from 128-255 are reversed images of codes 0-127.
