> Source: c64prg.txt Appendix J, "Converting Standard BASIC Programs to Commodore 64 BASIC". Lightly cleaned from the Project 64 etext.

  CONVERTING STANDARD
  BASIC PROGRAMS TO
  COMMODORE 64 BASIC

    If you have programs written in a BASIC other than Commodore BASIC,
  some minor adjustments may be necessary before running them on the
  Commodore-64. We've included some hints to make the conversion easier.


  String Dimensions

    Delete all statements that are used to declare the length of strings.
  A statement such as DIM A$(I,J), which dimensions a string array for J
  elements of length I, should be converted to the Commodore BASIC
  statement DIM A$(J).
    Some BASICs use a comma or an ampersand for string concatenation. Each
  of these must be changed to a plus sign, which is the Commodore BASIC
  operator for string concatenation.
    In Commodore-64 BASIC, the MID$, RIGHT$, and LEFT$ functions are used
  to take substrings of strings. Forms such as A$(I) to access the Ith
  character in A$, or A$(I,J) to take a substring of A$ from position I to
  J, must be changed as follows:

  Other BASIC     Commodore 64 BASIC

  A$(I)=X$        A$=LEFT$(A$,I-1)+X$+MID$(A$,I+1)
  A$(I,J)=X$      A$=LEFT$(A$,I-1)+X$+MID$(A$,J+1)

  Multiple Assignments

    To set B and C equal to zero, some BASICs allow statements of the form:

  10 LET B=C=0


    Commodore 64 BASIC would interpret the second equal sign as a logical
  operator and set B = -1 if C = 0. Instead, convert this statement to:

  10 C=0:B=0

  Multiple Statements

    Some BASICs use a backslash to separate multiple statements on a line.
  With Commodore 64 BASIC, separate all statements by a colon (:).

  MAT Functions

    Programs using the MAT functions available on some BASICs must be
  rewritten using FOR...NEXT loops to execute properly.
