> Source: c64prg.txt Ch2, "The Commodore 64 Keyboard and Features" and "Screen Editor". Lightly cleaned from the Project 64 etext.

# The Commodore 64 Keyboard, Features, and Screen Editor

  THE COMMODORE 64 KEYBOARD
  AND FEATURES

    The Operating System has a ton-character keyboard "buffer" that is used
  to hold incoming keystrokes until they can be processed. This buffer, or
  queue, holds keystrokes in the order in which they occur so that the
  first one put into the queue is the first one processed. For example, if
  a second keystroke occurs before the first can be processed, the second
  character Is stored in the buffer, while processing of the first
  character continues. After the program has finished with the first
  character, the keyboard buffer is examined for more data, and the second
  keystroke processed. Without this buffer, rapid keyboard input would
  occasionally drop characters.
    In other words, the keyboard buffer allows you to "type-ahead" of the
  system, which means it can anticipate responses to INPUT prompts or GET
  statements. As you type on the keys their character values are lined up,
  single-file (queued) into the buffer to wait for processing in the order
  the keys were struck. This type-ahead feature can give you an occasional
  problem where an accidental keystroke causes a program to fetch an
  incorrect character from the buffer.
    Normally, incorrect keystrokes present no problem, since they can be
  corrected by the CuRSoR-Left <CRSR LEFT> or DELete <INST/DEL> keys and
  then retyping the character, and the corrections will be processed before
  a following carriage-return. However, if you press the <RETURN> key, no
  corrective action is possible, since all characters in the buffer up to
  and including the carriage-return will be processed before any cor-
  rections. This situation can be avoided by using a loop to empty the
  keyboard buffer before reading an intended response:

    10 GET JUNK$: IF JUNK$ <>"" THEN 10: REM EMPTY THE KEYBOARD BUFFER

    In addition to GET and INPUT, the keyboard can also be read using
  PEEK to fetch from memory location 197 ($00C5) the integer value of the
  key currently being pressed. If no key Is being held when the PEEK is
  executed, a value of 64 is returned, The numeric keyboard values,
  keyboard symbols and character equivalents (CHR$) are shown in Ap-
  pendix C. The following example loops until a key is pressed then con-
  verts the integer to a character value.

    10 AA=PEEK(197): IF AA=64 THEN 10
    20 BB$=CHR$(AA)


    The keyboard is treated as a set of switches organized into a matrix
  of 8 columns by 8 rows. The keyboard matrix is scanned for key switch-
  closures by the KERNAL using the CIA #l 1/0 chip (MOS 6526 Complex
  Interface Adapter). Two CIA registers are used to perform the scan:
  register #0 at location 56320 ($DC00) for keyboard columns and
  register #l at location 56321 ($DC01) for keyboard rows.
    Bits 0-7 of memory location 56320 correspond to the columns 0-7. Bits
  0-7 of memory location 56321 correspond to rows 0-7. By writing column
  values in sequence, then reading row values, the KERNAL decodes the
  switch closures into the CHR$ (N) value of the key pressed.
    Eight columns by eight rows yields 64 possible values. However, if you
  first strike the <RVS ON>, <CTRL> or <C=> keys or hold down the <SHIFT>
  key and type a second character, additional values are generated. This is
  because the KERNAL decodes these keys separately and "remembers" when one
  of the control keys was pressed. The result of the keyboard scan is then
  placed in location 197.
    Characters can also be written directly to the keyboard buffer at lo-
  cations 631-640 using a POKE statement. These characters will be
  processed when the POKE is used to set a character count into location
  198. These facts can be used to cause a series of direct-mode commands to
  be executed automatically by printing the statements onto the screen,
  putting carriage-returns into the buffer, and then setting the character
  count. In the example below, the program will LIST itself to the printer
  and then resume execution.

    10 PRINT CHR$(147)"PRINT#1: CLOSE 1: GOTO 50"
    20 POKE 631119: POKE 632,13: POKE 633,13: POKE 198,3
    30 OPEN 114: CMD1: LIST
    40 END
    50 REM PROGRAM RE-STARTS HERE


  SCREEN EDITOR

    The SCREEN EDITOR provides you with powerful and convenient facilities
  for editing program text. Once a section of a program is listed to the
  screen, the cursor keys and other special keys are used to move around
  the screen so that you can make any appropriate changes. After making all
  the changes you want to a specific line-number of text, hitting the
  <RETURN> key anywhere on the line, causes the SCREEN EDITOR to read the
  entire 80-character logical screen line.


    The text is then passed to the Interpreter to be tokenized and stored
  in the program. The edited line replaces the old version of that line in
  memory. An additional copy of any line of text can be created simply by
  changing the line-number and pressing <RETURN>.
    If you use keyword abbreviations which cause a program line to exceed
  80 characters, the excess characters will be lost when that line is
  edited, because the EDITOR will read only two physical screen lines. This
  is also why using INPUT for more than a total of 80 characters is not
  possible. Thus, for all practical purposes, the length of a line of BASIC
  text is limited to 80 characters as displayed on the screen.
    Under certain conditions the SCREEN EDITOR treats the cursor control
  keys differently from their normal mode of handling. If the CuRSoR is
  positioned to the right of an odd number of double-quote marks (") the
  EDITOR operates in what is known as the QUOTE-MODE.
    In quote mode data characters are entered normally but the cursor
  controls no longer move the CuRSoR, instead reversed characters are
  displayed which actually stand for the cursor control being entered. The
  same is true of the color control keys. This allows you to include cursor
  and color controls inside string data items in programs. You will find
  that this is a very important and powerful feature. That's because when
  the text inside the quotes is printed to the screen it performs the
  cursor positioning and color control functions automatically as part of
  the string. An example of using cursor controls in strings is:


    You type -->         10 PRINT"A(R)(R)B(L)(L)(L)C(R)(R)D": REM(R)=CRSR
                            RIGHT, (L)=CRSR LEFT

    Computer prints -->  AC BD


     The <DEL> key is the only cursor control NOT affected by quote mode.
   Therefore, if an error is made while keying in quote mode, the
   <CRSR LEFT> key can't be used to back up and strike over the error -
   even the <INST> key produces a reverse video character. Instead, finish
   entering the line, and then, after hitting the <RETURN> key, you can
   edit the line normally. Another alternative, if no further cursor-
   controls are needed in the string, is to press the <RUN/STOP> and
   <RESTORE> keys which will cancel QUOTE MODE. The cursor control keys
   that you can use in strings are shown in Table 2-2.


             Table 2-2. Cursor Control Characters in QUOTE MODE
  -------------------------------------------------------------------------
                  Control Key                      Appearance
  -------------------------------------------------------------------------

              CRSR up
              CRSR down
              CRSR left
              CRSR right
              CLR
              HOME
              INST

  -------------------------------------------------------------------------

    When you are NOT in quote mode, holding down the <SHIFT> key and then
  pressing the INSerT <INST> key shifts data to the right of the cursor to
  open up space between two characters for entering data between them. The
  Editor then begins operating in INSERT MODE until all of the space opened
  up is filled.
    The cursor controls and color controls again show as reversed char-
  acters in insert mode. The only difference occurs on the DELete and
  INSerT <INST/DEL> key. The <DEL> instead of operating normally as in
  the quote mode, now creates the reversed <T>. The <INST> key, which
  created a reverse character in quote mode, inserts spaces normally.
    This means that a PRINT statement can be created, containing DELetes,
  which can't be done in quote mode. The insert mode is cancelled by
  pressing the <RETURN>, <SHIFT> and <RETURN>, or <RUN/STOP> and <RESTORE>
  keys. Or you can cancel the insert mode by filling all the inserted
  spaces. An example of using DEL characters in strings is:

    10 PRINT"HELLO"<DEL><INST><INST><DEL><DEL>P"
   (Keystroke sequence shown above, appearance when listed below)
   10 PRINT"HELP"

    When the example is RUN, the word displayed will be HELP, because the
  letters LO are deleted before the P is printed. The DELete character in
  strings will work with LIST as well as PRINT. You can use this to "hide"
  part or all of a line of text using this technique. However, trying to
  edit a line with these characters will be difficult if not impossible.


    There are some other characters that can be printed for special func-
  tions, although they are not easily available from the keyboard. In order
  to get these into quotes, you must leave empty spaces for them in the
  line, press <RETURN>, and go back to edit the line. Now you hold down
  the <CTRL> (ConTRoL) key and type <RVS ON> (ReVerSe-ON) to start typing
  reversed characters. Type the keys as shown below:


    Key Function                Key Entered         Appearance

    Shifted RETURN              <SHIFT+M>
    Switch to upper/lower case  <N>
    Switch to upper/graphics    <SHIFT+N>


    Holding down the <SHIFT> key and hitting <RETURN> causes a carriage-
  return and line-feed on the screen but does not end the string. This
  works with LIST as well as PRINT, so editing will be almost impossible if
  this character is used. When output is switched to the printer via the
  CMD statement, the reverse "N" character shifts the printer into its
  upper-lower case character set and the <SHIFT> "N" shifts the printer
  into the upper-case/graphics character set.
    Reverse video characters can be included in strings by holding down
  the ConTRoL <CTRL> key and pressing ReVerSe <RVS>, causing a reversed R
  to appear inside the quotes. This will make all characters print in
  reverse video (like a negative of a photograph). To end the reverse
  printing, press <CTRL> and <RVS OFF> (ReVerSe OFF) by holding down the
  <CTRL> key and typing the <RVS OFF> key, which prints a reverse R.
  Numeric data can be printed in reverse video by first printing a
  CHR$(18). Printing a CHR$(146) or a carriage-return will cancel reverse
  video output.
