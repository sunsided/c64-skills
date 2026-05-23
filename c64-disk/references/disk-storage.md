> Source: c64prg.txt Ch6, "Data Storage on Floppy Diskettes", plus the LOAD and OPEN keyword definitions from Ch2 BASIC Language Vocabulary (disk-relevant portions). Lightly cleaned from the Project 64 etext.

# Data Storage on Floppy Diskettes

Diskettes allow 3 different forms of data storage. Sequential files are similar to those on tape, but several can be used at the same time. Relative files let you organize the data into records, and then read and replace individual records within the file. Random files let you work with data anywhere on the disk. They are organized into 256 byte sections called blocks.

The PRINT# statement's limitations are discussed in the section on cassette tape. The same limitations to format apply on the disk. RETURNs or commas are needed to separate your data. The CHR$(0) is still read by the GET# statement as an empty string.

Relative and random files both make use of separate data and command "channels." Data written to the disk goes through the data channel, where it is stored in a temporary buffer in the disk's RAM. When the record or block is complete, a command is sent through the command channel that tells the drive where to put the data, and the entire buffer is written.

Applications that require large amounts of data to be processed are best stored in relative disk files. These will use the least amount of time and provide the best flexibility for the programmer. Your disk drive manual gives a complete programming guide to use of disk files.

## OPEN parameters for disk (from the OPEN Statement table)

    FORMAT: OPEN file#, device#, number, string

    +--------+---------+---------------------+------------------------------+
    | DEVICE | DEVICE# |       NUMBER        |            STRING            |
    +--------+---------+---------------------+------------------------------+
    | DISK   | 8 to 11 | 2-14 = Data Channel | Drive #, File Name           |
    |        |         |                     | File Type, Read/Write        |
    |        |         | 15 = Command        | Command                      |
    |        |         |      Channel        |                              |
    +--------+---------+---------------------+------------------------------+

## LOAD (disk-relevant portions)

TYPE: Command

FORMAT: LOAD["<file-name>"][,<device>][,<address>]

Action: The LOAD statement reads the contents of a program file from tape or disk into memory. That way you can use the information LOADed or change the information in some way. The device number is optional, but when it is left out the computer will automatically default to 1, the cassette unit. The disk unit is normally device number 8. The LOAD closes all open files and, if it is used in direct mode, it performs a CLR (clear) before reading the program. If LOAD is executed from within a program, the program is RUN. This means that you can use LOAD to "chain" several programs together. None of the variables are cleared during a chain operation.

If you are using file-name pattern matching, the first file which matches the pattern is loaded. The asterisk in quotes by itself ("*") causes the first file-name in the disk directory to be loaded. If the filename used does not exist or if it is not a program file, the BASIC error message ?FILE NOT FOUND occurs.

Programs will LOAD starting at memory location 2048 unless a secondary <address> of 1 is used. If you use the secondary address of 1 this will cause the program to LOAD to the memory location from which it was saved.

EXAMPLES of LOAD Command (disk):

    LOAD"*",8                    (LOADs first program from disk)

    LOAD"FUN",8                  (LOAD a file from disk)
    SEARCHING FOR FUN
    LOADING
    READY.

    LOAD"GAME ONE",8,1           (LOAD a file to the specific
    SEARCHING FOR GAME ONE        memory location from which the
    LOADING                       program was saved on the disk)
    READY.

## OPEN (disk-relevant portions)

TYPE: I/O Statement

FORMAT: OPEN <file-num>,[<device>][,<address>][,"<File-name> [,<type>] [,<mode>]"]

Action: This statement OPENs a channel for input and/or output to a peripheral device.

The <file-num> is the logical file number, which relates the OPEN, CLOSE, CMD, GET#, INPUT#, and PRINT# statements to each other and associates them with the file-name and the piece of equipment being used. The logical file number can range from 1 to 255 and you can assign it any number you want in that range.

NOTE: File numbers over 128 were really designed for other uses so it's good practice to use only numbers below 127 for file numbers.

Each peripheral device (printer, disk drive, cassette) in the system has its own number which it answers to. The <device> number is used with OPEN to specify on which device the data file exists. Peripherals like cassette decks, disk drives or printers also answer to several secondary addresses. Think of these as codes which tell each device what operation to perform. The device logical file number is used with every GET#, INPUT#, and PRINT#.

For disk files, the secondary addresses 2 thru 14 are available for data-files, but other numbers have special meanings in DOS commands. You must use a secondary address when using your disk drive(s). (See your disk drive manual for DOS command details.)

The <file-name> is a string of 1-16 characters and is optional for cassette or printer files. If the file <type> is left out the type of file will automatically default to the Program file unless the <mode> is given. Sequential files are OPENed for reading <mode>=R unless you specify that files should be OPENed for writing <mode>=W is specified. A file <type> can be used to OPEN an existing Relative file. Use REL for <type> with Relative files. Relative and Sequential files are for disk only.

If you try to access a file before it is OPENed the BASIC error message ?FILE NOT OPEN will occur. If you try to OPEN a file for reading which does not exist the BASIC error message ?FILE NOT FOUND will occur. If a file is OPENed to disk for writing and the file-name already exists, the DOS error message FILE EXISTS occurs. If a file is OPENed that is already OPEN, the BASIC error message FILE OPEN occurs.

EXAMPLES of OPEN Statements (disk):

    10 OPEN 2,8,4,"DISK-OUTPUT,SEQ,W"  (Opens sequential file on disk)

    110 OPEN 3,8,3,"0:DISK-FILE,S,W"   (Opens sequential write channel)
