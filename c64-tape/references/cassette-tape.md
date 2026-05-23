> Source: c64prg.txt Ch6, "Working With Cassette Tape", plus the tape-relevant portions of the LOAD and OPEN keyword definitions from Ch2 BASIC Language Vocabulary. Lightly cleaned from the Project 64 etext.

# Working With Cassette Tape

Cassette tapes have an almost unlimited capacity for data. The longer the tape, the more information it can store. However, tapes are limited in time. The more data on the tape, the longer the time it takes to find the information.

The programmer must try to minimize the time factor when working with tape storage. One common practice is to read the entire cassette data file into RAM, then process it, and then re-write all the data on the tape. This allows you to sort, edit, and examine your data. However, this limits the size of your files to the amount of available RAM.

If your data file is larger than the available RAM, it is probably time to switch to using the floppy disk. The disk can read data at any position on the disk, without needing to read through all the other data. You can write data over old data without disturbing the rest of the file. That's why the disk is used for all business applications like ledgers and mailing lists.

The PRINT# statement formats data just like the PRINT statement does. All punctuation works the same. But remember, you're not working with the screen now. The formatting must be done with the INPUT# statement constantly in mind.

Consider the statement PRINT# 1, A$, B$, C$. When used with the screen, the commas between the variables provide enough blank space between items to format them into columns ten characters wide. On cassette, anywhere from 1 to 10 spaces will be added, depending on the length of the strings. This wastes space on your tape.

Even worse is what happens when the INPUT# statement tries to read these strings. The statement INPUT# 1, A$, B$, C$ will discover no data for B$ and C$. A$ will contain all three variables, plus the spaces between them. What happens? Here's a look at the tape file:

    A$="DOG" B$="CAT" C$="TREE"
    PRINT# 1, A$, B$, C$

    1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25
    D O G                 C  A  T                       T  R  E  E  RETURN

The INPUT# statement works like the regular INPUT statement. When typing data into the INPUT statement, the data items are separated, either by hitting the <RETURN> key or using commas to separate them. The PRINT# statement puts a RETURN at the end of a line just like the PRINT statement. A$ fills up with all three values because there's no separator on the tape between them, only after all three.

A proper separator would be a comma (,) or a RETURN on the tape. The RETURN code is automatically put at the end of a PRINT or PRINT# statement. One way to put the RETURN code between each item is to use only one item per PRINT# statement. A better way is to set a variable to the RETURN CHR$ code, which is CHR$(13), or use a comma. The statement for this is R$=",":PRINT#1, A$ R$ B$ R$ C$. Don't use commas or any other punctuation between the variable names, since the Commodore 64 can tell them apart and they'll only use up space in your program.

A proper tape file looks like this:

    1 2 3 4 5 6 7 8 9 10 11 12 13

    D O G , C A T , T  R  E  E  RETURN

The GET# statement will pick data from the tape one character at a time. It will receive each character, including the RETURN code and other punctuation. The CHR$(0) code is received as an empty string, not as a one character string with a code of 0. If you try to use the ASC function on an empty string, you get the error message ILLEGAL QUANTITY ERROR.

The line GET# 1, A$: A=ASC(A$) is commonly used in programs to examine tape data. To avoid error messages, the line should be modified to GET#1, A$: A=ASC(A$+CHR$(0)). The CHR$(0) at the end acts as insurance against empty strings, but doesn't affect the ASC function when there are other characters in A$.

## OPEN parameters for cassette (from the OPEN Statement table)

    FORMAT: OPEN file#, device#, number, string

    +--------+---------+---------------------+------------------------------+
    | DEVICE | DEVICE# |       NUMBER        |            STRING            |
    +--------+---------+---------------------+------------------------------+
    |CASSETTE|    1    | 0 = Input           | File Name                    |
    |        |         | 1 = Output          |                              |
    |        |         | 2 = Output with EOT |                              |
    +--------+---------+---------------------+------------------------------+

## LOAD (tape-relevant portions)

TYPE: Command

FORMAT: LOAD["<file-name>"][,<device>][,<address>]

Action: The LOAD statement reads the contents of a program file from tape or disk into memory. The device number is optional, but when it is left out the computer will automatically default to 1, the cassette unit.

When LOADing programs from tape, the <file-name> can be left out, and the next program file on the tape will be read. The Commodore 64 will blank the screen to the border color after the PLAY key is pressed. When the program is found, the screen clears to the background color and the "FOUND" message is displayed. When the <C=> key, <CTRL> key, <ARROW LEFT> key, or <SPACE BAR> is pressed, the file will be loaded. Programs will LOAD starting at memory location 2048 unless a secondary <address> of 1 is used. If you use the secondary address of 1 this will cause the program to LOAD to the memory location from which it was saved.

EXAMPLES of LOAD Command (tape):

    LOAD                         (Reads the next program on tape)

    LOAD A$                      (Uses the name in A$ to search)

    LOAD"",1,1                   (Looks for the first program on
                                  tape, and LOADs it into the same
                                  part of memory that it came from)

    LOAD"STAR TREK"              (LOAD a file from tape)
    PRESS PLAY ON TAPE
    FOUND STAR TREK
    LOADING
    READY.

## OPEN (tape-relevant portions)

TYPE: I/O Statement

FORMAT: OPEN <file-num>,[<device>][,<address>][,"<File-name> [,<type>] [,<mode>]"]

If the <device> number is left out the computer will automatically assume that you want your information to be sent to and received from the Datassette(TM), which is device number 1. The file-name can also be left out, but later on in your program, you can NOT call the file by name if you have not already given it one. When you are storing files on cassette tape, the computer will assume that the secondary <address> is zero (0) if you omit the secondary address (a READ operation).

A secondary address value of one (1) OPENs cassette tape files for writing. A secondary address value of two (2) causes an end-of-tape marker to be written when the file is later closed. The end-of-tape marker prevents accidentally reading past the end of data which results in the BASIC error message ?DEVICE NOT PRESENT.

The <file-name> is a string of 1-16 characters and is optional for cassette or printer files. There is no check available for tape files that a name already exists, so be sure that the tape is properly positioned or you might accidentally write over some data that had previously been SAVED.

EXAMPLES of OPEN Statements (cassette):

    10 OPEN 1,1,2,"TAPE-WRITE"         (Write End-of-File on Close)
    10 OPEN 1,1,0,"NAME"               (Read from cassette)
    10 OPEN 1,1,1,"NAME"               (Write to cassette)
