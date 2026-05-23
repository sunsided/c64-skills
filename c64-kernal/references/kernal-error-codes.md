> Source: c64prg.txt §Ch5 "Error Codes". Lightly cleaned from the Project 64 etext.

  ERROR CODES

    The following is a list of error messages which can occur when using
  the KERNAL routines. If an error occurs during a KERNAL routine , the
  carry bit of the accumulator is set, and the number of the error message
  is returned in the accumulator.
  +-----------------------------------------------------------------------+
  | NOTE: Some KERNAL I/O routines do not use these codes for error       |
  | messages. Instead, errors are identified using the KERNAL READST      |
  | routine.                                                              |
  +-----------------------------------------------------------------------+
  +-------+---------------------------------------------------------------+
  | NUMBER|                          MEANING                              |
  +-------+---------------------------------------------------------------+
  |   0   |  Routine terminated by the <STOP> key                         |
  |   1   |  Too many open files                                          |
  |   2   |  File already open                                            |
  |   3   |  File not open                                                |
  |   4   |  File not found                                               |
  |   5   |  Device not present                                           |
  |   6   |  File is not an input file                                    |
  |   7   |  File is not an output file                                   |
  |   8   |  File name is missing                                         |
  |   9   |  Illegal device number                                        |
  |  240  |  Top-of-memory change RS-232 buffer allocation/deallocation   |
  +-------+---------------------------------------------------------------+
