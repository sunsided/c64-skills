> Source: c64prg.txt Ch6, "Input/Output Guide" (Introduction, Output to the TV, Output to Other Devices, Output to Printer, Output to Modem, The User Port, The Serial Bus, The Expansion Port, Z-80 Microprocessor Cartridge). Lightly cleaned from the Project 64 etext.

# Input/Output Guide

## INTRODUCTION

Computers have three basic abilities: they can calculate, make decisions, and communicate. Calculation is probably the easiest to program. Most of the rules of mathematics are familiar to us. Decision making is not too difficult, since the rules of logic are relatively few, even if you don't know them too well yet.

Communication is the most complex, because it involves the least exacting set of rules. This is not an oversight in the design of computers. The rules allow enough flexibility to communicate virtually anything, and in many possible ways. The only real rule is this: whatever sends information must present the information so that it can be understood by the receiver.

## OUTPUT TO THE TV

The simplest form of output in BASIC is the PRINT statement. PRINT uses the TV screen as the output device, and your eyes are the input device because they use the information on the screen.

When PRINTing on the screen, your main objective is to format the information on the screen so it's easy to read. You should try to think like a graphic artist, using colors, placement of letters, capital and lower case letters, as well as graphics to best communicate the information. Remember, no matter how smart your program, you want to be able to understand what the results mean to you.

The PRINT statement uses certain character codes as "commands" to the cursor. The <CRSR> key doesn't actually display anything, it just makes the cursor change position. Other commands change colors, clear the screen, and insert or delete spaces. The <RETURN> key has a character code number (CHR$) of 13. A complete table of these codes is contained in Appendix C.

There are two functions in the BASIC language that work with the PRINT statement. TAB positions the cursor on the given position from the left edge of the screen, SPC moves the cursor right a given number of spaces from the current position.

Punctuation marks in the PRINT statement serve to separate and format information. The semicolon (;) separates 2 items without any spaces in between. If it is the last thing on a line, the cursor remains after the last thing PRINTed instead of going down to the next line. It suppresses (replaces) the RETURN character that is normally PRINTed at the end of the line.

The comma (,) separates items into columns. The Commodore 64 has 4 columns of 10 characters each on the screen. When the computer PRINTs a comma, it moves the cursor right to the start of the next column. If it is past the last column of the line, it moves the cursor down to the next line. Like the semicolon, if it is the last item on a line the RETURN is suppressed.

The quote marks ("") separate literal text from variables. The first quote mark on the line starts the literal area, and the next quote mark ends it. By the way, you don't have to have a final quote mark at the end of the line.

The RETURN code (CHR$ code of 13) makes the cursor go to the next logical line on the screen. This is not always the very next line. When you type past the end of a line, that line is linked to the next line. The computer knows that both lines are really one long line. The links are held in the line link table (see the memory map for how this is set up).

A logical line can be 1 or 2 screen lines long, depending on what was typed or PRINTed. The logical line the cursor is on determines where the <RETURN> key sends it. The logical line at the top of the screen determines if the screen scrolls 1 or 2 lines at a time. There are other ways to use the TV as an output device. The chapter on graphics describes the commands to create objects that move across the screen. The VIC chip section tells how the screen and border colors and sizes are changed. And the sound chapter tells how the TV speaker creates music and special effects.

## OUTPUT TO OTHER DEVICES

It is often necessary to send output to devices other than the screen, like a cassette deck, printer, disk drive, or modem. The OPEN statement in BASIC creates a "channel" to talk to one of these devices. Once the channel is OPEN, the PRINT# statement will send characters to that device.

EXAMPLE of OPEN and PRINT# Statements:

    100 OPEN 4,4: PRINT# 4, "WRITING ON PRINTER"
    110 OPEN 3,8,3,"0:DISK-FILE,S,W":PRINT#3,"SEND TO DISK"
    120 OPEN 1,1,1,"TAPE-FILE": PRINT#1,"WRITE ON TAPE"
    130 OPEN 2,2,0,CHR$(10):PRINT#2,"SEND TO MODEM"

The OPEN statement is somewhat different for each device. The parameters in the OPEN statement are shown in the table below for each device.

TABLE of OPEN Statement Parameters:

    FORMAT: OPEN file#, device#, number, string

    +--------+---------+---------------------+------------------------------+
    | DEVICE | DEVICE# |       NUMBER        |            STRING            |
    +--------+---------+---------------------+------------------------------+
    |CASSETTE|    1    | 0 = Input           | File Name                    |
    |        |         | 1 = Output          |                              |
    |        |         | 2 = Output with EOT |                              |
    | MODEM  |    2    | 0                   | Control Registers            |
    | SCREEN |    3    | 0,1                 |                              |
    | PRINTER|  4 or 5 | 0 = Upper/Graphics  | Text Is PRINTed              |
    |        |         | 7 = Upper/Lower Case|                              |
    | DISK   | 8 to 11 | 2-14 = Data Channel | Drive #, File Name           |
    |        |         |                     | File Type, Read/Write        |
    |        |         | 15 = Command        | Command                      |
    |        |         |      Channel        |                              |
    +--------+---------+---------------------+------------------------------+

## OUTPUT TO PRINTER

The printer is an output device similar to the screen. Your main concern when sending output to the printer is to create a format that is easy on the eyes. Your tools here include reversed, double-width, capital and lower case letters, as well as dot-programmable graphics.

The SPC function works for the printer in the same way it works for the screen. However, the TAB function does not work correctly on the printer, because it calculates the current position on the line based on the cursor's position on the screen, not on the paper.

The OPEN statement for the printer creates the channel for communication. It also specifies which character set will be used, either upper case with graphics or upper and lower case.

EXAMPLES of OPEN Statement for Printer:

    OPEN 1,4: REM UPPER CASE/GRAPHICS
    OPEN 1,4,7: REM UPPER AND LOWER CASE

When working with one character set, individual lines can be PRINTed in the opposite character set. When in upper case with graphics, the cursor down character (CHR$(17)) switches the characters to the upper and lower case set. When in upper and lower case, the cursor up character (CHR$(145)) allows upper case and graphics characters to be PRINTed.

Other special functions in the printer are controlled through character codes. All these codes are simply PRINTed just like any other character.

TABLE of Printer Control Character Codes:

    +----------+------------------------------------------------------------+
    | CHR$ CODE|                         PURPOSE                            |
    +----------+------------------------------------------------------------+
    |    10    |   Line feed                                                |
    |    13    |   RETURN (automatic line feed on CBM printers)             |
    |    14    |   Begin double-width character mode                        |
    |    15    |   End double-width character mode                          |
    |    18    |   Begin reverse character mode                             |
    |   146    |   End reverse character mode                               |
    |    17    |   Switch to upper/lower case character set                 |
    |   145    |   Switch to upper case/graphics character set              |
    |    16    |   Tab to position in next 2 characters                     |
    |    27    |   Move to specified dot position                           |
    |     8    |   Begin dot-programmable graphic mode                      |
    |    26    |   Repeat graphics data                                     |
    +----------+------------------------------------------------------------+

See your Commodore printer's manual for details on using the command codes.

## OUTPUT TO MODEM

The modem is a simple device that can translate character codes into audio pulses and vice-versa, so that computers can communicate over telephone lines. The OPEN statement for the modem sets up the parameters to match the speed and format of the other computer you are communicating with. Two characters can be sent in the string at the end of the OPEN statement.

The bit positions of the first character code determine the baud rate, number of data bits, and number of stop bits. The second code is optional, and its bits specify the parity and duplex of the transmission. See the RS-232 section or your VICMODEM manual for specific details on this device.

EXAMPLE of OPEN Statement for Modem:

    OPEN 1,2,0,CHR$(6): REM 300 BAUD
    100 OPEN 2,2,0,CHR$(163) CHR$(112): REM 110 BAUD, ETC.

Most computers use the American Standard Code for Information Interchange, known as ASCII (pronounced ASK-KEY). This standard set of character codes is somewhat different from the codes used in the Commodore 64. When communicating with other computers, the Commodore character codes must be translated into their ASCII counterparts. A table of standard ASCII codes is included in this book in Appendix C.

Output to the modem is a fairly uncomplicated task, aside from the need for character translation. However, you must know the receiving device fairly well, especially when writing programs where your computer "talks" to another computer without human intervention. An example of this would be a terminal program that automatically types in your account number and secret password. To do this successfully, you must carefully count the number of characters and RETURN characters. Otherwise, the computer receiving the characters won't know what to do with them.

## THE USER PORT

The user port is meant to connect the Commodore 64 to the outside world. By using the lines available at this port, you can connect the Commodore 64 to a printer, a Votrax Type and Talk, a MODEM, even another computer.

The port on the Commodore 64 is directly connected to one of the 6526 CIA chips. By programming, the CIA will connect to many other devices.

### PORT PIN DESCRIPTION

                                             1 1 1
                           1 2 3 4 5 6 7 8 9 0 1 2
                        +--@-@-@-@-@-@-@-@-@-@-@-@--+
                        |                           |
                        +--@-@-@-@-@-@-@-@-@-@-@-@--+
                           A B C D E F H J K L M N

    +-----------+-----------+-----------------------------------------------+
    |    PIN    |           |                                               |
    +-----------+DESCRIPTION|                     NOTES                     |
    | TOP SIDE  |           |                                               |
    +-----------+-----------+-----------------------------------------------+
    |     1     |  GROUND   |                                               |
    |     2     |   +5V     |  (100 mA MAX.)                                |
    |     3     |  RESET    |  By grounding this pin, the Commodore 64 will |
    |           |           |  do a COLD START, resetting completely. The   |
    |           |           |  pointers to a BASIC program will be reset,   |
    |           |           |  but memory will not be cleared. This is also |
    |           |           |  a RESET output for the external devices.     |
    |     4     |    CNT1   |  Serial port counter from CIA#1(SEE CIA SPECS)|
    |     5     |    SP1    |  Serial port from CIA #1 (SEE 6526 CIA SPECS) |
    |     6     |    CNT2   |  Serial port counter from CIA#2(SEE CIA SPECS)|
    |     7     |    SP2    |  Serial port from CIA #2 (SEE 6526 CIA SPECS) |
    |     8     |    PC2    |  Handshaking line from CIA #2 (SEE CIA SPECS) |
    |     9     |SERIAL ATN |  This pin is connected to the ATN line of the |
    |           |           |  serial bus.                                  |
    |    10     |9 VAC+phase|  Connected directly to the Commodore          |
    |    11     |9 VAC-phase|  64 transformer (50 mA MAX.).                 |
    |    12     |    GND    |                                               |
    |           |           |                                               |
    |BOTTOM SIDE|           |                                               |
    |           |           |                                               |
    |     A     |    GND    |  The Commodore 64 gives you control over      |
    |     B     |   FLAG2   |  PORT B on CIA chip #1. Eight lines for input |
    |     C     |    PB0    |  or output are available, as well as 2 lines  |
    |     D     |    PB1    |  for handshaking with an outside device. The  |
    |     E     |    PB2    |  I/O lines for PORT B are controlled by two   |
    |     F     |    PB3    |  locations. One is the PORT itself, and is    |
    |     H     |    PB4    |  located at 56577 ($DD01 HEX). Naturally you  |
    |     I     |    PB5    |  PEEK it to read an INPUT, or POKE it to set  |
    |     K     |    PB6    |  an OUTPUT. Each of the eight I/O lines can   |
    |     L     |    PB7    |  be set up as either an INPUT or an OUTPUT by |
    |     M     |    PA2    |  by setting the DATA DIRECTION REGISTER       |
    |     N     |    GND    |  properly.                                    |
    +-----------+-----------+-----------------------------------------------+

The DATA DIRECTION REGISTER has its location at 56579 ($DD03 hex). Each of the eight lines in the PORT has a BIT in the eight-bit DATA DIRECTION REGISTER (DDR) which controls whether that line will be an input or an output. If a bit in the DDR is a ONE, the corresponding line of the PORT will be an OUTPUT. If a bit in the DDR is a ZERO, the corresponding line of the PORT will be an INPUT. For example, if bit 3 of the DDR is set to 1, then line 3 of the PORT will be an output. A further example:

If the DDR is set like this:

                          BIT #: 7 6 5 4 3 2 1 0
                          VALUE: 0 0 1 1 1 0 0 0

You can see that lines 5, 4, and 3 will be outputs since those bits are ones. The rest of the lines will be inputs, since those lines are zeros.

To PEEK or POKE the USER port, it is necessary to use both the DDR and the PORT itself.

Remember that the PEEK and POKE statements want a number from 0-255. The numbers given in the example must be translated into decimal before they can be used. The value would be:

                     2^5 + 2^4 + 2^3 = 32 + 16 + 8 = 56

Notice that the bit # for the DDR is the same number that = 2 raised to a power to turn the bit value on.

                      (16 = 2^4=2*2*2*2, 8 = 2^3=2*2*2)

The two other lines, FLAG1 and PA2 are different from the rest of the USER PORT. These two lines are mainly for HANDSHAKING, and are programmed differently from port B.

Handshaking is needed when two devices communicate. Since one device may run at a different speed than another device it is necessary to give the devices some way of knowing what the other device is doing. Even when the devices are operating at the same speed, handshaking is necessary to let the other know when data is to be sent, and if it has been received. The FLAG1 line has special characteristics which make it well suited for handshaking.

FLAG1 is a negative edge sensitive input which can be used as a general purpose interrupt input. Any negative transition on the FLAG line will set the FLAG interrupt bit. If the FLAG interrupt is enabled, this will cause an INTERRUPT REQUEST. If the FLAG bit is not enabled, it can be polled from the interrupt register under program control.

PA2 is bit 2 of PORT A of the CIA. It is controlled like any other bit in the port. The port is located at 56576 ($DD00). The data direction register is located at 56578 ($DD02).

FOR MORE INFORMATION ON THE 6526 SEE THE CHIP SPECIFICATIONS IN APPENDIX M.

## THE SERIAL BUS

The serial bus is a daisy chain arrangement designed to let the Commodore 64 communicate with devices such as the VIC-1541 DISK DRIVE and the VIC-1525 GRAPHICS PRINTER. The advantage of the serial bus is that more than one device can be connected to the port. Up to 5 devices can be connected to the serial bus at one time.

There are three types of operation over a serial bus-CONTROL, TALK, and LISTEN. A CONTROLLER device is one which controls operation of the serial bus. A TALKER transmits data onto the bus. A LISTENER receives data from the bus.

The Commodore 64 is the controller of the bus. It also acts as a TALKER (when sending data to the printer, for example) and as a LISTENER (when loading a program from the disk drive, for example). Other devices may be either LISTENERS (the printer), TALKERS, or both (the disk drive). Only the Commodore 64 can act as the controller.

All devices connected on the serial bus will receive all the data transmitted over the bus. To allow the Commodore 64 to route data to its intended destination, each device has a bus ADDRESS. By using this device address, the Commodore 64 can control access to the bus. Addresses on the serial bus range from 4 to 31.

The Commodore 64 can COMMAND a particular device to TALK or LISTEN. When the Commodore 64 commands a device to TALK, the device will begin putting data onto the serial bus. When the Commodore 64 commands a device to LISTEN, the device addressed will get ready to receive data (from the Commodore 64 or from another device on the bus). Only one device can TALK on the bus at a time; otherwise, the data will collide and the system will crash in confusion. However, any number of devices can LISTEN at the same time to one TALKER.

                         COMMON SERIAL BUS ADDRESSES
                    +--------+--------------------------+
                    | NUMBER |        DEVICE            |
                    +--------+--------------------------+
                    | 4 or 5 | VIC-1525 GRAPHIC PRINTER |
                    | 8      | VIC-1541 DISK DRIVE      |
                    +--------+--------------------------+

Other device addresses are possible. Each device has its own address. Certain devices (like the Commodore 64 printer) provide a choice between two addresses for the convenience of the user.

The SECONDARY ADDRESS is to let the Commodore 64 transmit setup information to a device. For example, to OPEN a connection on the bus to the printer, and have it print in UPPER/LOWER case, use the following

    OPEN 1,4,7

where,
  1 is the logical file number (the number you PRINT# to),
  4 is the ADDRESS of the printer, and
  7 is the SECONDARY ADDRESS that tells the printer to go into UPPER/LOWER case mode.

There are 6 lines used in serial bus operations - input and 3 output. The 3 input lines bring data, control, and timing signals into the Commodore 64. The 3 output lines send data, control, and timing signals from the Commodore 64 to external devices on the serial bus.

    Serial I/O
                                                       ++ ++
    +-------+----------------------+                    / +-+ \
    |  Pin  |         Type         |                   /5     1\
    +-------+----------------------+                  +  O   O  +
    |   1   |  /SERIAL SRQ IN      |                  |    6    |
    |   2   |  GND                 |                  |    O    |
    |   3   |  SERIAL ATN OUT      |                  |         |
    |   4   |  SERIAL CLK IN/OUT   |                  +  O   O  +
    |   5   |  SERIAL DATA IN/OUT  |                   \4  O  2/
    |   6   |  /RESET              |                    \  3  /
    +-------+----------------------+                     +---+

### SERIAL SRQ IN: (SERIAL SERVICE REQUEST IN)

Any device on the serial bus can bring this signal LOW when it requires attention from the Commodore 64. The Commodore 64 will then take care of the device.

### SERIAL ATN OUT: (SERIAL ATTENTION OUT)

The Commodore 64 uses this signal to start a command sequence for a device on the serial bus. When the Commodore 64 brings this signal LOW, all other devices on the bus start listening for the Commodore 64 to transmit an address. The device addressed must respond in a preset period of time; otherwise, the Commodore 64 will assume that the device addressed is not on the bus, and will return an error in the STATUS WORD.

                              SERIAL BUS TIMING
    +-----------------------------+-------+-------+-------+-----------------+
    |     Description             | Symbol|  Min. |  Typ. |       Max.      |
    +-----------------------------+-------+-------+-------+-----------------+
    | ATN RESPONSE (REQUIRED) (1) |  Tat  |   -   |   -   |     1000us      |
    | LISTENER HOLD-OFF           |  Th   |   0   |   -   |    infinite     |
    | NON-EOI RESPONSE TO RFD (2) |  Tne  |   -   |  40us |      200us      |
    | BIT SET-UP TALKER (4)       |  Ts   |  20us |  70us |        -        |
    | DATA VALID                  |  Tv   |  20us |  20us |        -        |
    | FRAME HANDSHAKE (3)         |  Tf   |   0   |  20   |     1000us      |
    | FRAME TO RELEASE OF ATN     |  Tr   |  20us |   -   |        -        |
    | BETWEEN BYTES TIME          |  Tbb  | 100us |   -   |        -        |
    | EOI RESPONSE TIME           |  Tye  | 200us | 250us |        -        |
    | EOI RESPONSE HOLD TIME (5)  |  Tei  |  60us |   -   |        -        |
    | TALKER RESPONSE LIMIT       |  Try  |   0   |  30us |       60us      |
    | BYTE-ACKNOWLEDGE (4)        |  Tpr  |  20us |  30us |        -        |
    | TALK-ATTENTION RELEASE      |  Ttk  |  20us |  30us |      100us      |
    | TALK-ATTENTION ACKNOWLEDGE  |  Tdc  |   0   |   -   |        -        |
    | TALK-ATTENTION ACK. HOLD    |  Tda  |  80us |   -   |        -        |
    | EOI ACKNOWLEDGE             |  Tfr  |  60us |   -   |        -        |
    +-----------------------------+-------+-------+-------+-----------------+
       Notes:
       1. If maximum time exceeded, device not present error.
       2. If maximum time exceeded, EOI response required.
       3. If maximum time exceeded, frame error.
       4. Tv and Tpr minimum must be 60us for external device to be a talker.
       5. Tei minimum must be 80us for external device to be a listener.

### SERIAL CLK IN/OUT: (SERIAL CLOCK IN/OUT)

This signal is used for timing the data sent on the serial bus.

### SERIAL DATA IN/OUT:

Data on the serial bus is transmitted one bit at a time on this line.

## THE EXPANSION PORT

The expansion connector is a 44-pin (22/22) female edge connector on the back of the Commodore 64. With the Commodore 64 facing you, the expansion connector is on the far right of the back of the computer. To use the connector, a 44-pin (22/22) male edge connector is required.

This port is used for expansions of the Commodore 64 system which require access to the address bus or the data bus of the computer. Caution is necessary when using the expansion bus, because it's possible to damage the Commodore 64 by a malfunction of your equipment.

The expansion bus is arranged as follows:

                 2 2 2 1 1 1 1 1 1 1 1 1 1
                 2 1 0 9 8 7 6 5 4 3 2 1 0 9 8 7 6 5 4 3 2 1
             +---@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@---+
             |                                                 |
             +---@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@---+
                 Z Y X W V U T S R P N M L K J H F E D C B A

The signals available on the connector are as follows:

    +---------+---+---------------------------------------------------------+
    |   NAME  |PIN|                       DESCRIPTION                       |
    +---------+---+---------------------------------------------------------+
    |   GND   | 1 |  System ground                                          |
    |  +5VDC  | 2 |  (Total USER PORT and CARTRIDGE devices can             |
    |  +5VDC  | 3 |  draw no more than 450 mA.)                             |
    |  /IRQ   | 4 |  Interrupt Request line to 6502 (active low)            |
    |   R/W   | 5 |  Read/Write (write active low)                          |
    |DOT CLOCK| 6 |  8.18 MHz video dot clock                               |
    |  /I/O1  | 7 |  I/O block 1 @ $DE00-$DEFF (active low) unbuffered I/O  |
    |  /GAME  | 8 |  active low ls ttl input                                |
    |  /EXROM | 9 |  active low ls ttl input                                |
    |  /I/O2  |10 |  I/O block 2 @ $DF00-$DFFF (active low) buff'ed ls ttl  |
    |         |   |                                                  output |
    |  /ROML  |11 |  8K decoded RAM/ROM block @ $8000 (active low) buffered |
    |         |   |  ls ttl output                                          |
    |   BA    |12 |  Bus available signal from the VIC-II chip unbuffered   |
    |         |   |    1 ls load max.                                       |
    |  /DMA   |13 |  Direct memory access request line (active low input)   |
    |         |   |  ls ttl input                                           |
    |   D7    |14 |  Data bus bit 7 \                                       |
    |   D6    |15 |  Data bus bit 6  +                                      |
    |   D5    |16 |  Data bus bit 5  |                                      |
    |   D4    |17 |  Data bus bit 4  +-  unbuffered, 1 ls ttl load max      |
    |   D3    |18 |  Data bus bit 3  +-                                     |
    |   D2    |19 |  Data bus bit 2  |                                      |
    |   D1    |20 |  Data bus bit 1  +                                      |
    |   D0    |21 |  Data bus bit 0 /                                       |
    |   GND   |22 |  System ground                                          |
    |   GND   | A |                                                         |
    |  /ROMH  | B |  8K decoded RAM/ROM block @ $E000 buffered              |
    |  /RESET | C |  6502 RESET pin(active low) buff'ed ttl out/unbuff'ed in|
    |  /NMI   | D |  6502 Non Maskable Interrupt (active low) buff'ed ttl   |
    |         |   |  out, unbuff'ed in                                      |
    |   02    | E |  Phase 2 system clock                                   |
    |   A15   | F |  Address bus bit 15 \                                   |
    |   A14   | H |  Address bus bit 14  +                                  |
    |   A13   | J |  Address bus bit 13  |                                  |
    |   A12   | K |  Address bus bit 12  |                                  |
    |   A11   | L |  Address bus bit 11  |                                  |
    |   A10   | M |  Address bus bit 10  |                                  |
    |   A9    | N |  Address bus bit 9   |                                  |
    |   A8    | P |  Address bus bit 8   +--  unbuffered, 1 ls ttl load max |
    |   A7    | R |  Address bus bit 7   +--                                |
    |   A6    | S |  Address bus bit 6   |                                  |
    |   A5    | T |  Address bus bit 5   |                                  |
    |   A4    | U |  Address bus bit 4   |                                  |
    |   A3    | V |  Address bus bit 3   |                                  |
    |   A2    | W |  Address bus bit 2   |                                  |
    |   A1    | X |  Address bus bit 1   +                                  |
    |   A0    | Y |  Address bus bit 0  /                                   |
    |   GND   | Z |  System ground                                          |
    +---------+---+---------------------------------------------------------+

Following is a description of some important lines on the expansion port:

Pins 1, 22, A, Z are connected to the system ground.

Pin 6 is the DOT CLOCK. This is the 8.18-MHz video dot clock. All system timing is derived from this clock.

Pin 12 is the BA (BUS AVAILABLE) signal from the VIC-II chip. This line will go low 3 cycles before the VIC-II takes over the system busses, and remains low until the VIC-II is finished fetching display information.

Pin 13 is the DMA (DIRECT MEMORY ACCESS) line. When this line is pulled low, the address bus, the data bus, and the Read/Write line of the 6510 processor chip enter high-impedance state mode. This allows an external processor to take control of the system busses. This line should only be pulled low when the 02 clock is low. Also, since the VIC-II chip will continue to perform display DMA, the external device must conform to the VIC-II timing. (See VIC-II timing diagram.) This line is pulled up on the Commodore 64.

## Z-80 MICROPROCESSOR CARTRIDGE

Reading this book and using your computer has shown you just how versatile your Commodore 64 really is. But what makes this machine even more capable of meeting your needs is the addition of peripheral equipment. Peripherals are things like Datassette(TM) recorders, disk drives, printers, and modems. All these items can be added to your Commodore 64 through the various ports and sockets on the back of your machine. The thing that makes Commodore peripherals so good is the fact that our peripherals are "intelligent." That means that they don't take up valuable Random Access Memory space when they're in use. You're free to use all 64K of memory in your Commodore 64.

Another advantage of your Commodore 64 is the fact most programs you write on your Commodore 64 today will be upwardly compatible with any new Commodore computer you buy in the future. This is partially because of the qualities of the computer's Operating System (OS).

However, there is one thing that the Commodore OS can't do: make your programs compatible with a computer made by another company.

Most of the time you won't even have to think about using another company's computer, because your Commodore 64 is so easy to use. But for the occasional user who wants to take advantage of software that may not be available in Commodore 64 format we have created a Commodore CP/M(R) cartridge.

CP/M(R) is not a "computer dependent" operating system. Instead it uses some of the memory space normally available for programming to run its own operating system. There are advantages and disadvantages to this. The disadvantages are that the programs you write will have to be shorter than the programs you can write using the Commodore 64's built-in operating system. In addition, you can NOT use the Commodore 64's powerful screen editing capabilities. The advantages are that you can now use a large amount of software that has been specifically designed for CP/M(R) and the Z-80 microprocessor, and the programs that you write using the CP/M(R) operating system can be transported and run on any other computer that has CP/M(R) and a Z-80 card.

By the way, most computers that have a Z-80 microprocessor require that you go inside the computer to actually install a Z-80 card. With this method you have to be very careful not to disturb the delicate circuitry that runs the rest of the computer. The Commodore CP/M(R) cartridge eliminates this hassle because our Z-80 cartridge plugs into the back of your Commodore 64 quickly and easily, without any messy wires that can cause problems later.

### USING COMMODORE CP/M(R)

The Commodore Z-80 cartridge lets you run programs designed for a Z-80 microprocessor on your Commodore 64. The cartridge is provided with a diskette containing the Commodore CP/M(R) operating system.

### RUNNING COMMODORE CP/M(R)

To run CP/M(R):

      1) LOAD the CP/M(R) program from your disk drive.
      2) Type RUN.
      3) Hit the <RETURN> key.

At this point the 64K bytes of RAM in the Commodore 64 are accessible by the built-in 6510 central processor, OR 48K bytes of RAM are available for the Z-80 central processor. You can shift back and forth between these two processors, but you can NOT use them at the same time in a single program. This is possible because of your Commodore 64's sophisticated timing mechanism.

Below is the memory address translation that is performed on the Z-80 cartridge. You should notice that by adding 4096 bytes to the memory locations used in CP/M(R) $1000 (hex) you equal the memory addresses of the normal Commodore 64 operating system. The correspondence between Z-80 and 6510 memory addresses is as follows:

    +-----------------------------------+-----------------------------------+
    |          Z-80 ADDRESSES           |           6510 ADDRESSES          |
    +-----------------+-----------------+-----------------+-----------------+
    |     DECIMAL     |       HEX       |     DECIMAL     |       HEX       |
    +-----------------+-----------------+-----------------+-----------------+
    |    0000-4095    |    0000-0FFF    |    4096-8191    |    1000-1FFF    |
    |    4096-8191    |    1000-1FFF    |    8192-12287   |    2000-2FFF    |
    |    8192-12287   |    2000-2FFF    |   12288-16383   |    3000-3FFF    |
    |   12288-16383   |    3000-3FFF    |   16384-20479   |    4000-4FFF    |
    |   16384-20479   |    4000-4FFF    |   20480-24575   |    5000-5FFF    |
    |   20480-24575   |    5000-5FFF    |   24576-28671   |    6000-6FFF    |
    |   24576-28671   |    6000-6FFF    |   28672-32767   |    7000-7FFF    |
    |   28672-32767   |    7000-7FFF    |   32768-36863   |    8000-8FFF    |
    |   32768-36863   |    8000-8FFF    |   36864-40959   |    9000-9FFF    |
    |   36864-40959   |    9000-9FFF    |   40960-45055   |    A000-AFFF    |
    |   40960-45055   |    A000-AFFF    |   45056-49151   |    B000-BFFF    |
    |   45056-49151   |    B000-BFFF    |   49152-53247   |    C000-CFFF    |
    |   49152-53247   |    C000-CFFF    |   53248-57343   |    D000-DFFF    |
    |   53248-57343   |    D000-DFFF    |   57344-61439   |    E000-EFFF    |
    |   57344-61439   |    E000-EFFF    |   61440-65535   |    F000-FFFF    |
    |   61440-65535   |    F000-FFFF    |    0000-4095    |    0000-0FFF    |
    +-----------------+-----------------+-----------------+-----------------+

To TURN ON the Z-80 and TURN OFF the 6510 chip, type in the following program:

    10 rem this program is to be used with the z80 card
    20 rem it first stores z80 data at $1000 (Z80=$0000)
    30 rem then it turns off the 6510 irq's and enables
    40 rem the z80 card. the z80 card must be turned off
    50 rem to reenable the 6510 system.
    100 rem store z80 data
    110 read b: rem get size of z80 code to be moved
    120 for i=4096 to 4096+b-1:rem move code
    130 read a:poke i,a
    140 next i
    200 rem run z80 code
    210 poke 56333,127: rem turn of 6510 irq's
    220 poke 56832,00 : rem turn on z80 card
    230 poke 56333,129: rem turn on 6510 irq's when z80 done
    240 end
    1000 rem z80 machine language code data section
    1010 data 18 : rem size of data to be passed
    1100 rem z80 turn on code
    1110 data 00,00,00 : rem our z80 card requires turn on time at $0000
    1200 rem z80 task data here
    1210 data 33,02,245: rem ld hl,nn (location on screen)
    1220 data 52 : rem inc hl (increment that location)
    1300 rem z80 self-turn off data here
    1310 data 62,01 : rem ld a,n
    1320 data 50,00,206 : rem ld (nn),a :i/o location
    1330 data 00,00,00  : rem nop, nop, nop
    1340 data 195,00,00 : rem jmp $0000

For more details about Commodore CP/M(R) and the Z-80 microprocessor look for the cartridge and the Z-80 Reference Guide at your local Commodore computer dealer.
