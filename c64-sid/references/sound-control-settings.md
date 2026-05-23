> Source: c64ug.txt Appendix P, "Commodore 64 Sound Control Settings" (User's Guide). Lightly cleaned from the Project 64 etext.


  This  handy  table  gives  you  the key numbers you need to use in your
sound  programs,  according  to  which of the Commodore 64's 3 voices you
want to use. To set or adjust a sound control in your BASIC program, just
POKE  the  number  from  the second column, followed by a comma (,) and a
number  from  the  chart ... like this: POKE 54276,17 (Selects a Triangle
Waveform for VOICE 1).
  Remember  that  you  must set the VOLUME before you can generate sound.
POKE  54296  followed  by a number from 0 to 15 sets the volume for all 3
voices.
  It takes 2 separate POKEs to generate each musical note ... for example
POKE 54273,34: POKE 54272,75 designates low C in the sample scale bellow.
  Also  ...  you aren't limited to the numbers shown in the tables. If 34
doesn't sound "right" for a low C, try 35. To provide a higher SUSTAIN or
ATTACK  rate than those shown,  add two or more SUSTAIN numbers together.
(Examples:  POKE  54277,96  combines  two  attack rates (32 and 64) for a
combined  higher  attack  rate  ...  but ... POKE 54277,20 provides a low
attack rate (16) and a medium decay rate (4).

+----------------------------------------------------------------------------+
|SETTING VOLUME -- SAME FOR ALL 3 VOICES                                     |
+--------------+---------+---------------------------------------------------+
|VOLUME CONTROL|POKE54296| Settings from 0 (off) to 15 (loudest)             |
+--------------+---------+---------------------------------------------------+
                              VOICE NUMBER 1
+--------------+---------+---------------------------------------------------+
|TO CONTROL    |POKE THIS|         FOLLOWED BY ONE OF THESE NUMBERS          |
|THIS SETTING: |NUMBER:  | (0 to 15 ... or ... 0 to 255 depending on range)  |
+--------------+---------+---------------------------------------------------+
|TO PLAY A NOTE|      C  | C#| D | D#| E | F | F#| G | G#| A | A#| B | C | C#|
|HIGH FREQUENCY|54273 34 | 36| 38| 40| 43| 45| 48| 51| 54| 57| 61| 64| 68| 72|
|LOW FREQUENCY |54272 75 | 85|126|200| 52|198|127| 97|111|172|126|188|149|169|
+--------------+---------+------------+------------+------------+------------+
|WAVEFORM      |  POKE   |  TRIANGLE  |  SAWTOOTH  |   PULSE    |   NOISE    |
|              |  54276  |     17     |     33     |     65     |    129     |
+--------------+---------+------------+------------+------------+------------+
|PULSE RATE (Pulse Waveform)                                                 |
|HI POLSE      |  54275  |   A value of 0 to 15  (for Pulse waveform only)   |
|LO POLSE      |  54274  |   A value of 0 to 255 (for Pulse waveform only)   |
+--------------+---------+------+------+------+------+-----+-----+-----+-----+
|ATTACK/       |  POKE   | ATK4 | ATK3 | ATK2 | ATK1 | DEC4| DEC3| DEC2| DEC1|
|       DECAY  |  54277  | 128  |  64  |  32  |  16  |  8  |  4  |  2  |  1  |
+--------------+---------+------+------+------+------+-----+-----+-----+-----+
|SUSTAIN/      |  POKE   | SUS4 | SUS3 | SUS2 | SUS1 | REL4| REL3| REL2| REL1|
|       RELEASE|  54278  | 128  |  64  |  32  |  16  |  8  |  4  |  2  |  1  |
+--------------+---------+------+------+------+------+-----+-----+-----+-----+
                              VOICE NUMBER 2
+--------------+---------+---------------------------------------------------+
|TO CONTROL    |POKE THIS|         FOLLOWED BY ONE OF THESE NUMBERS          |
|THIS SETTING: |NUMBER:  | (0 to 15 ... or ... 0 to 255 depending on range)  |
+--------------+---------+---------------------------------------------------+
|TO PLAY A NOTE|      C  | C#| D | D#| E | F | F#| G | G#| A | A#| B | C | C#|
|HIGH FREQUENCY|54280 34 | 36| 38| 40| 43| 45| 48| 51| 54| 57| 61| 64| 68| 72|
|LOW FREQUENCY |54279 75 | 85|126|200| 52|198|127| 97|111|172|126|188|149|169|
+--------------+---------+------------+------------+------------+------------+
|WAVEFORM      |  POKE   |  TRIANGLE  |  SAWTOOTH  |   PULSE    |   NOISE    |
|              |  54283  |     17     |     33     |     65     |    129     |
+--------------+---------+------------+------------+------------+------------+
|PULSE RATE (Pulse Waveform)                                                 |
|HI POLSE      |  54282  |   A value of 0 to 15  (for Pulse waveform only)   |
|LO POLSE      |  54281  |   A value of 0 to 255 (for Pulse waveform only)   |
+--------------+---------+------+------+------+------+-----+-----+-----+-----+
|ATTACK/       |  POKE   | ATK4 | ATK3 | ATK2 | ATK1 | DEC4| DEC3| DEC2| DEC1|
|       DECAY  |  54284  | 128  |  64  |  32  |  16  |  8  |  4  |  2  |  1  |
+--------------+---------+------+------+------+------+-----+-----+-----+-----+
|SUSTAIN/      |  POKE   | SUS4 | SUS3 | SUS2 | SUS1 | REL4| REL3| REL2| REL1|
|       RELEASE|  54285  | 128  |  64  |  32  |  16  |  8  |  4  |  2  |  1  |
+--------------+---------+------+------+------+------+-----+-----+-----+-----+
                              VOICE NUMBER 3
+--------------+---------+---------------------------------------------------+
|TO CONTROL    |POKE THIS|         FOLLOWED BY ONE OF THESE NUMBERS          |
|THIS SETTING: |NUMBER:  | (0 to 15 ... or ... 0 to 255 depending on range)  |
+--------------+---------+---------------------------------------------------+
|TO PLAY A NOTE|      C  | C#| D | D#| E | F | F#| G | G#| A | A#| B | C | C#|
|HIGH FREQUENCY|54287 34 | 36| 38| 40| 43| 45| 48| 51| 54| 57| 61| 64| 68| 72|
|LOW FREQUENCY |54286 75 | 85|126|200| 52|198|127| 97|111|172|126|188|149|169|
+--------------+---------+------------+------------+------------+------------+
|WAVEFORM      |  POKE   |  TRIANGLE  |  SAWTOOTH  |   PULSE    |   NOISE    |
|              |  54290  |     17     |     33     |     65     |    129     |
+--------------+---------+------------+------------+------------+------------+
|PULSE RATE (Pulse Waveform)                                                 |
|HI POLSE      |  54289  |   A value of 0 to 15  (for Pulse waveform only)   |
|LO POLSE      |  54288  |   A value of 0 to 255 (for Pulse waveform only)   |
+--------------+---------+------+------+------+------+-----+-----+-----+-----+
|ATTACK/       |  POKE   | ATK4 | ATK3 | ATK2 | ATK1 | DEC4| DEC3| DEC2| DEC1|
|       DECAY  |  54291  | 128  |  64  |  32  |  16  |  8  |  4  |  2  |  1  |
+--------------+---------+------+------+------+------+-----+-----+-----+-----+
|SUSTAIN/      |  POKE   | SUS4 | SUS3 | SUS2 | SUS1 | REL4| REL3| REL2| REL1|
|       RELEASE|  54292  | 128  |  64  |  32  |  16  |  8  |  4  |  2  |  1  |
+--------------+---------+------+------+------+------+-----+-----+-----+-----+

TRY THESE SETTINGS TO SIMULATE DIFFERENT INSTRUMENTS

+------------+----------+--------------+---------------+----------------+
| Instrument | Waveform | Attack/Decay |Sustain/Release| Pulse Rate     |
+------------+----------+--------------+---------------+----------------+
| Piano      | Pulse    |       9      |        0      | Hi-0, Lo-255   |
| Flute      | Triangle |      96      |        0      | Not applicable |
| Harpsichord| Sawtooth |       9      |        0      | Not applicable |
| Xylophone  | Triangle |       9      |        0      | Not applicable |
| Organ      | Triangle |       0      |      240      | Not applicable |
| Colliape   | Triangle |       0      |      240      | Not applicable |
| Accordian  | Triangle |     102      |        0      | Not applicable |
| Trumpet    | Sawtooth |      96      |        0      | Not applicable |
+------------+----------+--------------+---------------+----------------+

MEANINGS OF SOUND TERMS

ADSR     -- Attack/Decay/Sustain/Release
Attack   -- Rate sound rises to peak volume
Decay    -- Rate sound falls from peak volume to Sustain level
Sustain  -- Prolong note at certain volume
Release  -- Rate at which volume falls from Sustain level
Waveform -- "Shape" of sound wave
Pulse    -- Tone quality of Pulse Waveform

NOTE: Attack/Decay and Sustain/Release settings should always be POKEd in
your program BEFORE the Waveform is POKEd.

INDEX

A
 Abbreviations, BASIC commands, D
 Accesories, INTRODUCTION, A
 Addition, 2.4-2.5, C
 AND operator, 5.4, C
 Animation, 4.1, 5.6, 6.2, E, G
 Arithmetic, Operators, 2.4-2.5, C
 Arithmetic, Formulas, 2.4-2.5, C, H
 Arrays, 8.3-8.6
 ASC function, 4.8, C, F
 ASCII character codes, F

B
 BASIC
   abbreviations, D
   commands, C
   numeric functions, C
   operators, 2.4, C
   other functions, C
   statements, C
   string functions, C
   variables, 3.3, C
 Bibliography, N
 Binary arithmetic, 6.3-6.4
 Bit, 6.3-6.4
 Business aids, A
 Byte, 6.4

C
 Calculations, 2.4-2.6
 Cassette tape recorder (audio), 1.1, 2.3
 Cassette tape recorder (video), 1.3
 Cassette port, 1.1
 CHR$ function, 3.3, 4.3, 4.8, 5.3, C, F, K
 CLR statement, C
 CLR/HOME key, 2.1, 3.1, 4.2
 Clock, C
 CLOSE statement, B, C
 Color
   adjustment, 1.5
   CHR$ codes, 5.3
   keys, 5.1-5.2
   memory map, 5.5, G
   PEEKS and POKES, 5.4
   screen and border, 5.4-5.5, G
 Commands, BASIC, C
 Commodore key, (see graphic keys)
 Connections
   optional, 1.3
   rear, 1.1
   side panel, 1.1
   TV/Monitor, 1.2
 CONT command, C
 ConTRoL key, 1.5, 2.1
 COSine function, C
 CuRSoR keys, 1.4, 2.1, 3.2
 Correcting errors, 3.2
 Cursor, 1.4

D
 DATASSETTE recorder, (see cassette tape recorder, audio)
 Data, loading and saving (disk), 2.3, C
 Data, loading and saving (tape), 2.3, C
 DATA statement, 6.2, 6.3, 7.4, 7.6, 8.1, C
 DEFine statement, C
 Delay loop, 5.4, 5.8
 DELete key, 2.1
 DIMension statement, 8.4, C
 Division, 2.4-2.5, C
 Duration, (see FOR ... NEXT)

E
 Editing program, 2.1, 3.2
 END statement, 3.4, C
 Equal, not-equal-to, signs, 2.4-2.5, 3.4, C
 Equations, 3.4, C
 Error messages, 2.4, L
 Expansion port, I
 EXPonent function, C
 Exponentiation, 2.4-2.5, C

F
 Files, (tape), 2.3, B, C
 Files, (disk), 2.3, C
 FOR statement, 3.5, C
 FRE function, C
 Functions, C

G
 Game controls and ports, 1.1, I
 GET statement, 4.4, C
 GET# statement, C
 Getting started, 2.1-2.6
 GOSUB statement, C
 GOTO (GO TO) statement, 3.1, C
 Graphic keys, 2.1, 5.1-5.2, 5.4, E
 Graphic symbols, (see graphic keys)
 Greater than, 3.4, C

H
 Hyperbolic functions, H

I
 IEEE-488 Interface, A
 IF ... THEN statement, 3.4, C
 INPUT statement, 4.3, C
 INPUT# statement, C
 INSerT key, 2.1, 3.2
 INTeger function, 4.5, C
 I/O pinouts, I
 I/O ports, 1.1-1.3

J
 Joysticks, 1.1, I

K
 Keyboard, 2.1-2.2

L
 LEFT$ function, C
 LENgth function, 6.4, C
 Less than, 3.4, C
 LET statement, C
 LIST command, 3.1-3.2, C
 LOAD command, 2.3, C
 LOADing programs from tape, 2.3, C
 LOADing programs from disk, 2.3, C
 LOGarithm, C
 Loops, 3.5, 4.2-4.3
 Lower Case characters, 2.1

M
 Mathematics
   formulas, 2.4-2.5
   function table, H
   symbols, 2.4-2.5, 3.4
 Memory maps, 5.5, G, O, P
 MID$ function, 6.4, C
 Modulator, RF, 1.2-1.3
 Multiplication, 2.4-2.5, C
 Music, 7.1-7.8

N
 Names
   program, 2.3, C
   variable, 3.3, C
 NEW command, 3.1, C
 NEXT statement, 3.5, C
 NOT operator, C
 Numeric variables, 3.3

O
 ON statement, C
 OPEN statement, C
 Operators
   arithmetic, 2.4, C
   logical, C
   relational, 3.4, C

P
 Parentheses, 2.5
 PEEK function, 5.4, 5.6
 Peripherals, 1.1-1.3
 POKE statement, 5.4
 Ports, I/O, 1.1, I
 POS function, C
 PRINT statement, 2.4, C
 PRINT# statement, C
 Precedence, 2.5
 Programs
   editing, 2.1, 3.2
   line numbering, 3.1
   loading/saving (tape), 2.3, C
   loading/saving (disk), 2.3, C
 Prompt, 4.3

Q
 Quotation marks, 2.4

R
 RaNDom function, 4.5-4.8, C
 Random numbers, 4.5-4.8
 READ statement, 8.1-8.2, C
 Reading from tape, B
 REMark statement, 4.2, C
 Reserved words, (see Commands, BASIC)
 RESTORE key, 2.1-2.2
 RESTORE statement, 8.1, C
 RETURN key, 2.1-2.2
 RETURN statement, C
 RIGHT$ function, C
 RUN command, C
 RUN/STOP key, 2.1, 3.1

S
 SAVE command, 2.3, C
 Saving programs (tape), 2.3, C
 Saving programs (disk), 2.3, C
 Screen memory maps, 5.5, G
 SGN function, C
 SHIFT key, 2.1-2.2
 SINe function, C
 Sound effects, 7.7-7.8
 SPC function, 8.6, C
 SPRITE EDITOR, INTRODUCTION
 SPRITE graphics, 6.1-6.3
 SQuaRe function, C
 STOP command, C
 STOP key, 2.1
 String variables, 3.3
 STR$ function, C
 Subscripted variables, 8.3
 Subtraction, 2.4-2.5, C
 SYNTAX ERROR, 2.4
 SYS statement, C

T
 TAB function, C
 TAN function, C
 TI variable, C
 TI$ variable, C
 Time clock, C
 TV connections, 1.2-1.3

U
 Upper/Lower Case mode, 2.1, E
 USR function, C
 User defined function, (see DEF)

V
 VALue function, 6.4, C
 Variables
   array, 8.3-8.6, C
   dimensions, 8.4-8.6, C
   floating point, 3.3, C
   integer, 3.3, C
   numeric, 3.3, 4.3, C
   string ($), 3.3, 4.3, C
 VERIFY command, C
 Voice, 7.1-7.8, P

W
 WAIT command, C
 Writing to tape, B

Z,
 Z-80, INTRODUCTION, A

Commodore  hopes  you've enjoyed the COMMODORE 64 USER'S GUIDE.  Although
this  manual  contains  some  programming information and tips, it is NOT
intended to be a Programmer's Reference Manual.  For those of you who are
advanced  programmers  and computer hobbyists Commodore suggests that you
consider  purchasing  COMMODORE 64 PROGRAMMER'S REFERENCE GUIDE available
through your local Commodore dealer.

In addition updates and corrections as well as programming hints and tips
are available in the COMMODORE and POWER PLAY magazines, on the COMMODORE
database  of  the  COMPUSERVE  INFORMATION  NETWORK,  accessed  through a
VICMODEM.

COMMODORE 64 QUICK REFERENCE CARD

SIMPLE VARIABLES

TYPE     NAME    RANGE
Real     XY      +/-1.70141183E+38
                 +/-2.93873588E-39
Integer  XY%     +32767...-32768
String   XY$     0 to 255 characters

X is a letter (A-Z). Y is a letter or number (0-9). Variable names can be
more than 2 characters, but only the first two are recognized.

ARRAY VARIABLES

TYPE                 NAME
Single Dimension     XY(5)
Two-Dimension        XY(5,5)
Three-Dimension      XY(5,5,5)

Arrays  of  up  to  eleven  elements  (subscripts 0-10) can be used where
needed.  Arrays  with  more  than eleven elements need to be DIMensioned.

ALGEBRAIC OPERATIONS

=   Assigns value to variable
-   Negation
^   Exponentiation
*   Multiplication
/   Division
+   Addition
-   Subtraction

RELATION AND LOGICAL OPERATORS

=   Equal
<>  Not Equal
<   Less Than
>   Greater Than
<=  Less Than or Equal To
>=  Greater Than or Equal To
NOT Logical "Not"
AND Logical "And"
OR  Logical "Or"

Expressions equals 1 if true, 0 if false.

SYSTEM COMMANDS

LOAD "NAME"     Loads a program from tape
SAVE "NAME"     Saves a program on tape
LOAD "NAME",8   Loads a program from disk
SAVE "NAME",8   Saves a program to disk
VERIFY "NAME"   Verifies that program was SAVEd without errors
RUN             Executes a program
RUN xxx         Executes program starting at line xxx
STOP            Halts execution
END             Ends execution
CONT            Continues program execution from line
                where program was halted
PEEK(X)         Returns contents of memory location X
POKE X,Y        Changes contents of location X to value Y
SYS xxxxx       Jumps to execute a machine language program,
                starting at xxxxx
WAIT X,Y,Z      Program waits until contents of location X, when EORed
                with Z and ANDed with Y, is nonzero.
USR(X)          Passes value of X to a machine language subroutine

EDITING AND FORMATTING COMMANDS

LIST            Lists entire program
LIST A-B        Lists from line A to line B
REM Message     Comment message can be listed but is ignored
                during program execution
TAB(X)          Used in PRINT statements. Spaces X positions on screen
SPC(X)          PRINTs X blanks on line
POS(X)          Returns current cursor position

CLR/HOME        Positions cursor to left-up corner of screen
SHIFT CLR/HOME  Clears screen and places cursor in "Home" position
SHIFT INS/DEL   Inserts space current cursor position
INST/DEL        Deletes character at current cursor position
CTRL            When used with numeric color key, selects text color. May
                be used in PRINT statement.
CRSR Keys       Moves cursor up, down, left right on screen
Commodore Key   When used with SHIFT selects between upper/lower case and
                graphic display mode. When used with numeric key, selects
                optional text color

ARRAYS AND STRINGS

DIM A(X,Y,Z)    Sets maximum subscripts for A; reserves space for
                (X+1)*(Y+1)*(Z+1) elements starting at A(0,0,0)
LEN(X$)         Returns number of characters in X$
STR$(X)         Returns numeric value of X, converted to a string
VAL(X$)         Returns numeric value of X$, up to first nonnumeric
                character
CHR$(X)         Returns ASCII character whose code is X
ASC(X$)         Returns ASCII code for first character of X$
LEFT$(A$,X)     Returns leftmost X characters of A$
RIGHT$(A$,X)    Returns rightmost X characters of A$
MID$(A$,X,Y)    Returns Y characters of A$ starting at character X

INPUT/OUTPUT COMMANDS

INPUT A$ or A   PRINTs '?' on screen and waits for user to enter
                a string or value
INPUT "ABC";A   PRINTs message and waits for user to enter value.
                Can also INPUT A$
GET A$ or A     Waits for user type one-character value;
                no RETURN needed
DATA A,"B",C    Initializes a set of values that can be used by READ
                statement
READ A$ or A    Assigns next DATA value to A$ or A
RESTORE         Resets data pointer to start READing the DATA list again
PRINT "A=";A    PRINTs string 'A=' and value of A; ';' suppresses spaces;
                ',' tabs data to next field

PROGRAM FLOW

GOTO X          Branches to line X
IF A=3 THEN 10  IF assertion is true THEN execute following part of
                statement. IF false, execute next line number
FOR A=1 to 10   Executes all statements between FOR and corresponding
STEP 2: NEXT    NEXT, with A, going from 1 to 10 by 2. Step size is 1
                unless specified
NEXT A          Defines end of loop. A is optional
GOSUB 2000      Branches to subroutine starting at line 2000
RETURN          Marks end of subroutine. Returns to statement following
                most recent GOSUB
ON X GOTO A,B   Branches to Xth line number on list.
                If X=1 branches to A, etc.
ON X GOSUB A,B  Branches to subroutine at Xth line number in list

ABOUT THE COMMODORE 64 USERS GUIDE...

Outstanding   color  ...  sound  synthesis  ...  graphics  ...  computing
capabilities   ...   the   synergistic   marriage   of   state-of-the-art
technologies.  These  features  make  the  Commodore 64 the most advanced
personal computer in its class.

The Commodore 64 User's Guide helps you get started in computing, even if
you're   never  used  a  computer  before.  Through  clear,  step-by-step
instructions,  you  are  given an insight into the BASIC language and how
the Commodore 64 can be put to a myriad of uses.

For those already familiar with microcomputers,  the advanced programming
sections and appendices explain the enhanced features of the Commodore 64
and how to get the most of these expanded capabilities.

   _____
  /  ___|___
 |  /   |__/  c o m m o d o r e
 |  \___|__\  C O M P U T E R
  \_____|

Commodore Business Machines, Inc. -- Computer Systems Division,
487 Devon Park Drive, Wayne, PA 19087.

DISTRIBUTED BY
Howard W. Sams & Co., Inc.
4300 W. 62nd Street, Indianapolis, Indiana 46268 USA

$12.95/22010

ISBN:0-672-22010-5

*********

End of the Project 64 etext of the Commodore 64 User's Guide.

*********
