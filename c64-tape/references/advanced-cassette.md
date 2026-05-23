> Source: c64ug.txt App B, "Advanced Cassette Operation". Lightly cleaned from the Project 64 etext.

# Advanced Cassette Operation

Besides saving copies of your programs on tape, the Commodore 64 can also store the values of variables and other items of data, in a group called a FILE. This allows you to store even more information than could be held in the computer's main memory at one time.

Statements used with data files are OPEN, CLOSE, PRINT#, INPUT# and GET#. The system variable ST (status) is used to check for tape markers.

In writing data to tape, the same concepts are used as when displaying information on the computer's screen. But instead of PRINTing information on the screen, the information is PRINTed on tape using a variation of the PRINT command -- PRINT#.

The following program illustrates how this works:

    10 PRINT "WRITE-TO-TAPE-PROGRAM"
    20 OPEN 1,1,1, "DATA FILE"
    30 PRINT "TYPE DATA TO BE STORED OR TYPE STOP"
    40 PRINT
    50 INPUT "DATA"; A$
    60 PRINT#1, A$
    70 IF A$ <> "STOP" THEN 40
    80 PRINT
    90 PRINT "CLOSING FILE"
   100 CLOSE 1

The first thing that you must do is OPEN a file (in this case DATA FILE). Line 10 handles that.

The program prompts for the data you want to save on tape in line 50. Line 60 writes what you typed -- held in A$ -- onto the tape. And the process continues.

If you type STOP, line 100 CLOSEs the file.

To retrieve the information, rewind the tape, and try this:

    10 PRINT "READ-TAPE-PROGRAM"
    20 OPEN 1,1,0, "DATA FILE"
    30 PRINT "FILE OPEN"
    40 PRINT
    50 INPUT#1, A$
    60 PRINT A$
    70 IF A$ <> "STOP" THEN 40
    80 PRINT
    90 PRINT "CLOSING FILE"
   100 CLOSE 1

Again, this file "DATA FILE" first must be OPENed. In line 50 the program INPUTs A$ from tape and also PRINTs A$ on the screen. Then the whole process is repeated until "STOP" is found, which ENDs the program.

A variation of GET-GET# can also be used to read the data back from tape. Replace lines 50-70 in the program above with:

    50 GET#1, A$
    60 IF A$ <> "" THEN 50
    70 PRINT A$, ASC(A$)
