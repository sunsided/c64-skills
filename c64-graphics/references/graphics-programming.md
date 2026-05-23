> Source: c64prg.txt §Chapter 3 "Programming Graphics on the Commodore 64", graphics-modes portion (Graphics Overview through Smooth Scrolling, i.e. everything before the Sprites section). Lightly cleaned from the Project 64 etext.

  GRAPHICS OVERVIEW

  All of the graphics abilities of the Commodore 64 come from the 6567
  Video Interface Chip (also known as the VIC-II chip). This chip gives a
  variety of graphics modes, including a 40 column by 25 line text display,
  a 320 by 200 dot high resolution display, and SPRITES, small movable
  objects which make writing games simple. And if this weren't enough,
  many of the graphics modes can be mixed on the same screen. It is
  possible, for example, to define the top half of the screen to be in
  high resolution mode, while the bottom half is in text mode. And SPRITES
  will combine with anything! More on sprites later. First the other
  graphics modes.
    The VIC-II chip has the following graphics display modes:

  A) CHARACTER DISPLAY MODES

     1) Standard Character Mode
            a)ROM characters
            b)RAM programmable characters
     2) Multi-Color Character Mode
            a)ROM characters
            b)RAM programmable characters

     3) Extended Background Color Mode
            a)ROM characters
            b)RAM programmable characters

  B) BIT MAP MODES

     1) Standard Bit Map Mode
     2) Multi-Color Bit Map Mode

  C) SPRITES

     1) Standard Sprites
     2) Multi-Color Sprites

  GRAPHICS LOCATIONS

    Some general information first. There are 1000 possible locations on
  the Commodore 64 screen. Normally, the screen starts at location 1024
  ($0400 in HEXadecimal notation) and goes to location 2023. Each of
  these locations is 8 bits wide. This means that it can hold any integer
  number from 0 to 255. Connected with screen memory is a group of 1000
  locations called COLOR MEMORY or COLOR RAM. These start at location 55296
  ($D800 in HEX) and go up to 56295. Each of the color RAM locations is 4
  bits wide, which means that it can hold any integer number from 0 to 15.
  Since there are 16 possible colors that the Commodore 64 can use, this
  works out well.
    In addition, there are 256 different characters that can be displayed
  at any time. For normal screen display, each of the 1000 locations in
  screen memory contains a code number which tells the VIC-II chip which
  character to display at that screen location.
    The various graphics modes are selected by the 47 CONTROL registers in
  the VIC-II chip. Many of the graphics functions can be controlled by
  POKEing the correct value into one of the registers. The VIC-II chip is
  located starting at 53248 ($D000 in HEX) through 53294 ($D02E in HEX).

  VIDEO BANK SELECTION

    The VIC-II chip can access ("see") 16K of memory at a time. Since there
  is 64K of memory in the Commodore 64, you want to be able to have the
  VIC-II chip see all of it. There is a way. There are 4 possible BANKS
  (or sections) of 16K of memory. All that is needed is some means of
  controlling which 16K bank the VIC-II chip looks at. In that way, the
  chip can "see" the entire 64K of memory. The BANK SELECT bits that allow
  you access to all the different sections of memory are located in the
  6526 COMPLEX INTERFACE ADAPTER CHIP #2 (CIA #2). The POKE and PEEK BASIC
  statements (or their machine language versions) are used to select a
  bank, by controlling bits 0 and 1 of PORT A of CIA#2 (location 56576 (or
  $DD00 HEX)). These 2 bits must be set to outputs by setting bits 0 and 1
  of location 56578 ($DD02,HEX) to change banks. The following example
  shows this:

    POKE 56578,PEEK(56578)OR 3: REM MAKE SURE BITS 0 AND 1 ARE OUTPUTS
    POKE 56576,(PEEK(56576)AND 252)OR A: REM CHANGE BANKS

    "A" should have one of the following values:

  +-------+------+-------+----------+-------------------------------------+
  | VALUE | BITS |  BANK | STARTING |  VIC-II CHIP RANGE                  |
  |  OF A |      |       | LOCATION |                                     |
  +-------+------+-------+----------+-------------------------------------+
  |   0   |  00  |   3   |   49152  | ($C000-$FFFF)*                      |
  |   1   |  01  |   2   |   32768  | ($8000-$BFFF)                       |
  |   2   |  10  |   1   |   16384  | ($4000-$7FFF)*                      |
  |   3   |  11  |   0   |       0  | ($0000-$3FFF) (DEFAULT VALUE)       |
  +-------+------+-------+----------+-------------------------------------+

    This 16K bank concept is part of everything that the VIC-II chip does.
  You should always be aware of which bank the VIC-II chip is pointing at,
  since this will affect where character data patterns come from, where the
  screen is, where sprites come from, etc. When you turn on the power of
  your Commodore 64, bits 0 and 1 of location 56576 are automatically set
  to BANK 0 ($0000-$3FFF) for all display information.

  +-----------------------------------------------------------------------+
  | *NOTE: The Commodore 64 character set is not available to the VIC-II  |
  | chip in BANKS 1 and 3. (See character memory section.)                |
  +-----------------------------------------------------------------------+

  SCREEN MEMORY

    The location of screen memory can be changed easily by a POKE to
  control register 53272 ($D018 HEX). However, this register is also used
  to control which character set is used, so be careful to avoid disturbing
  that part of the control register. The UPPER 4 bits control the location
  of screen memory. To move the screen, the following statement should be
  used:

  POKE53272,(PEEK(53272)AND15)OR A

  Where "A" has one of the following values:
  +---------+------------+-----------------------------+
  |         |            |         LOCATION*           |
  |    A    |    BITS    +---------+-------------------+
  |         |            | DECIMAL |        HEX        |
  +---------+------------+---------+-------------------+
  |     0   |  0000XXXX  |      0  |  $0000            |
  |    16   |  0001XXXX  |   1024  |  $0400 (DEFAULT)  |
  |    32   |  0010XXXX  |   2048  |  $0800            |
  |    48   |  0011XXXX  |   3072  |  $0C00            |
  |    64   |  0100XXXX  |   4096  |  $1000            |
  |    80   |  0101XXXX  |   5120  |  $1400            |
  |    96   |  0110XXXX  |   6144  |  $1800            |
  |   112   |  0111XXXX  |   7168  |  $1C00            |
  |   128   |  1000XXXX  |   8192  |  $2000            |
  |   144   |  1001XXXX  |   9216  |  $2400            |
  |   160   |  1010XXXX  |  10240  |  $2800            |
  |   176   |  1011XXXX  |  11264  |  $2C00            |
  |   192   |  1100XXXX  |  12288  |  $3000            |
  |   208   |  1101XXXX  |  13312  |  $3400            |
  |   224   |  1110XXXX  |  14336  |  $3800            |
  |   240   |  1111XXXX  |  15360  |  $3C00            |
  +---------+------------+---------+-------------------+
  +-----------------------------------------------------------------------+
  | * Remember that the BANK ADDRESS of the VIC-II chip must be added in. |
  | You must also tell the KERNAL'S screen editor where the screen is as  |
  | follows: POKE 648, page (where page = address/256, e.g., 1024/256= 4, |
  | so POKE 648,4).                                                       |
  +-----------------------------------------------------------------------+

  COLOR MEMORY

    Color memory can NOT move. It is always located at locations 55296
  ($D800) through 56295 ($DBE7). Screen memory (the 1000 locations starting
  at 1024) and color memory are used differently in the different graphics
  modes. A picture created in one mode will often look completely different
  when displayed in another graphics mode.

  CHARACTER MEMORY

    Exactly where the VIC-II gets it character information is important to
  graphic programming. Normally, the chip gets the shapes of the characters

  you want to be displayed from the CHARACTER GENERATOR ROM. In this chip
  are stored the patterns which make up the various letters, numbers,
  punctuation symbols, and the other things that you see on the keyboard.
  One of the features of the Commodore 64 is the ability to use patterns
  located in RAM memory. These RAM patterns are created by you, and that
  means that you can have an almost infinite set of symbols for games,
  business applications, etc.
    A normal character set contains 256 characters in which each character
  is defined by 8 bytes of data. Since each character takes up 8 bytes this
  means that a full character set is 256*8=2K bytes of memory. Since the
  VIC-II chip looks at 16K of memory at a time, there are 8 possible
  locations for a complete character set. Naturally, you are free to use
  less than a full character set. However, it must still start at one of
  the 8 possible starting locations.
    The location of character memory is controlled by 3 bits of the VIC-II
  control register located at 53272 ($D018 in HEX notation). Bits 3,2, and
  1 control where the characters' set is located in 2K blocks. Bit 0 is ig-
  nored. Remember that this is the same register that determines where
  screen memory is located so avoid disturbing the screen memory bits. To
  change the location of character memory, the following BASIC statement
  can be used:

    POKE 53272,(PEEK(53272)AND240)OR A

  Where A is one of the following values:
  +-----+----------+------------------------------------------------------+
  |VALUE|          |            LOCATION OF CHARACTER MEMORY*             |
  | of A|   BITS   +-------+----------------------------------------------+
  |     |          |DECIMAL|         HEX                                  |
  +-----+----------+-------+----------------------------------------------+
  |   0 | XXXX000X |     0 | $0000-$07FF                                  |
  |   2 | XXXX001X |  2048 | $0800-$0FFF                                  |
  |   4 | XXXX010X |  4096 | $1000-$17FF ROM IMAGE in BANK 0 & 2 (default)|
  |   6 | XXXX011X |  6144 | $1800-$1FFF ROM IMAGE in BANK 0 & 2          |
  |   8 | XXXX100X |  8192 | $2000-$27FF                                  |
  |  10 | XXXX101X | 10240 | $2800-$2FFF                                  |
  |  12 | XXXX110X | 12288 | $3000-$37FF                                  |
  |  14 | XXXX111X | 14336 | $3800-$3FFF                                  |
  +-----+----------+-------+----------------------------------------------+
  +-----------------------------------------------------------------------+
  | * Remember to add in the BANK address.                                |
  +-----------------------------------------------------------------------+

    The ROM IMAGE in the above table refers to the character generator ROM.
  It appears in place of RAM at the above locations in bank 0. it  also
  appears in the corresponding RAM at locations 36864-40959 ($9000-$9FFF)
  in bank 2. Since the VIC-II chip can only access 16K of memory at a time,
  the ROM character patterns appear in the 16K block of memory the VIC-II
  chip looks at. Therefore, the system was designed to make the VIC-II chip
  think that the ROM characters are at 4096-8191 ($1000-$1FFF) when your
  data is in bank 0, and 36864-40959 ($9000-$9FFF) when your data is in
  bank 2, even though the character ROM is actually at location 53248-57343
  ($D000-$DFFF). This imaging only applies to character data as seen by the
  VIC-II chip. It can be used for programs, other data, etc., just like any
  other RAM memory.

  +-----------------------------------------------------------------------+
  | NOTE: If these ROM images got in the way of your own graphics, then   |
  | set the BANK SELECT BITS to one of the BANKS without the images       |
  | (BANKS 1 or 3). The ROM patterns won't be there.                      |
  +-----------------------------------------------------------------------+

   The location and contents of the character set in ROM are as follows:

  +-----+-------------------+-----------+---------------------------------+
  |     |       ADDRESS     |   VIC-II  |                                 |
  |BLOCK+-------+-----------+   IMAGE   |            CONTENTS             |
  |     |DECIMAL|    HEX    |           |                                 |
  +-----+-------+-----------+-----------+---------------------------------+
  |  0  | 53248 | D000-D1FF | 1000-11FF | Upper case characters           |
  |     | 53760 | D200-D3FF | 1200-13FF | Graphics characters             |
  |     | 54272 | D400-D5FF | 1400-15FF | Reversed upper case characters  |
  |     | 54784 | D600-D7FF | 1600-17FF | Reversed graphics characters    |
  |     |       |           |           |                                 |
  |  1  | 55296 | D800-D9FF | 1800-19FF | Lower case characters           |
  |     | 55808 | DA00-DBFF | 1A00-1BFF | Upper case & graphics characters|
  |     | 56320 | DC00-DDFF | 1C00-1DFF | Reversed lower case characters  |
  |     | 56832 | DE00-DFFF | 1E00-1FFF | Reversed upper case &           |
  |     |       |           |           | graphics characters             |
  +-----+-------+-----------+-----------+---------------------------------+

    Sharp-eyed readers will have just noticed something. The locations
  occupied by the character ROM are the same as the ones occupied by the
  VIC-II chip control registers. This is possible because they don't occupy
  the same locations at the same time. When the VIC-II chip needs to access

  character data the ROM is switched in. It becomes an image in the 16K
  bank of memory that the VIC-II chip is looking at. Otherwise, the area is
  occupied by the I/O control registers, and the character ROM is only
  available to the VIC-II chip.
    However, you may need to get to the character ROM if you are going to
  use programmable characters and want to copy some of the character ROM
  for some of your character definitions. In this case you must switch out
  the I/O register, switch in the character ROM, and do your copying. When
  you're finished, you must switch the 1/0 registers back in again. During
  the copying process (when I/O is switched out) no interrupts can be
  allowed to take place. This is because the I/O registers are needed to
  service the interrupts. If you forget and perform an interrupt, really
  strange things happen. The keyboard should not be read during the copying
  process. To turn off the keyboard and other normal interrupts that occur
  with your Commodore 64, the following POKE should be used:

    POKE 56334,PEEK(56334)AND254   (TURNS INTERRUPTS OFF)

    After you are finished getting characters from the character ROM, and
  are ready to continue with your program, you must turn the keyboard scan
  back on by the following POKE:

    POKE 56334,PEEK(56334)OR1      (TURNS INTERRUPTS ON)

    The following POKE will switch out 1/0 and switch the CHARACTER ROM in:

    POKE 1,PEEK(1)AND251

    The character ROM is now in the locations from 53248-57343 ($D000-
  $DFFF).
    To switch I/O back into $D000 for normal operation use the following
  POKE:

    POKE 1,PEEK(1)OR 4

  STANDARD CHARACTER MODE

    Standard character mode is the mode the Commodore 64 is in when you
  first turn it on. It is the mode you will generally program in.
    Characters can be taken from ROM or from RAM, but normally they are
  taken from ROM. When you want special graphics characters for a program,
  all you have to do is define the new character shapes in RAM, and tell
  the VIC-II chip to get its character information from there instead of
  the character ROM. This is covered in more detail in the next section.
    In order to display characters on the screen in color, the VIC-II chip
  accesses the screen memory to determine the character code for that
  location on the screen. At the same time, it accesses the color memory to
  determine what color you want for the character displayed. The character
  code is translated by the VIC-II into the starting address of the 8-byte
  block holding your character pattern. The 8-byte block is located in
  character memory.
    The translation isn't too complicated, but a number of items are com-
  bined to generate the desired address. First the character code you use
  to POKE screen memory is multiplied by 8. Next add the start of char-
  acter memory (see CHARACTER MEMORY section). Then the Bank Select Bits
  are taken into account by adding in the base address (see VIDEO BANK
  SELECTION section). Below is a simple formula to illustrate what happens:

  CHARACTER ADDRESS = SCREEN CODE*8+(CHARACTER SET*2048)+(BANK*16384)

  CHARACTER DEFINITIONS

    Each character is formed in an 8 by 8 grid of dots, where each dot may
  be either on or off. The Commodore 64 character images are stored in the
  Character Generator ROM chip. The characters are stored as a set of 8
  bytes for each character, with each byte representing the dot pattern of
  a row in the character, and each bit representing a dot. A zero bit means
  that dot is off, and a one bit means the dot is on.
    The character memory in ROM begins at location 53248 (when the I/O
  is switched off). The first 8 bytes from location 53248 ($D000) to 53255
  ($D007) contain the pattern for the @ sign, which has a character code
  value of zero in the screen memory. The next 8 bytes, from location

  53256 ($D008) to 53263 ($D00F), contain the information for forming the
  letter A.

       IMAGE     BINARY       PEEK

        **      00011000       24
       ****     00111100       60
      **  **    01100110      102
      ******    01111110      126
      **  **    01100110      102
      **  **    01100110      102
      **  **    01100110      102
		00000000	0

    Each complete character set takes up 2K (2048 bits) of memory, 8 bytes
  per character and 256 characters. Since there are two character sets, one
  for upper case and graphics and the other with upper and lower case, the
  character generator ROM takes up a total of 4K locations.

  PROGRAMMABLE CHARACTERS

    Since the characters are stored in ROM, it would seem that there is no
  way to change them for customizing characters. However, the memory
  location that tells the VIC-II chip where to find the characters is a
  programmable register which can be changed to point to many sections of
  memory. By changing the character memory pointer to point to RAM, the
  character set may be programmed for any need.
    If you want your character set to be located in RAM, there are a few
  VERY IMPORTANT things to take into account when you decide to actually
  program your own character sets. In addition, there are two other
  important points you must know to create your own special characters:

    1) It is an all or nothing process. Generally, if you use your own
       character set by telling the VIC-II chip to get the character
       information from the area you have prepared in RAM, the standard
     Commodore 64 characters are unavailable to you. To solve this, you
     must copy any letters, numbers, or standard Commodore 64 graphics you
     intend to use into your own character memory in RAM. You can pick and
     choose, take only the ones you want, and don't even have to keep them
     in order!

    2) Your character set takes memory space away from your BASIC program.
       Of course, with 38K available for a BASIC program, most applications
       won't have problems.

  +-----------------------------------------------------------------------+
  | WARNING: You must be careful to protect the character set from being  |
  | overwritten by your BASIC program, which also uses the RAM.           |
  +-----------------------------------------------------------------------+

    There are two locations in the Commodore 64 to start your character set
  that should NOT be used with BASIC: location 0 and location 2048. The
  first should not be used because the system stores important data on
  page 0. The second can't be used because that is where your BASIC program
  starts! However, there are 6 other starting positions for your custom
  character set.
    The best place to put your character set for use with BASIC while
  experimenting is beginning at 12288 ($3000 in HEX). This is done by
  POKEing the low 4 bits of location 53272 with 12. Try the POKE now, like
  this:

    POKE 53272,(PEEK(53272)AND240)+12

    Immediately, all the letters on the screen turn to garbage, This is
  because there are no characters set up at location 12288 right now...
  only random bytes. Set the Commodore 64 back to normal by hitting the
  <RUN/STOP> key and then the <RESTORE> key.
    Now let's begin creating graphics characters. To protect your char-
  acter set from BASIC, you should reduce the amount of memory BASIC
  thinks it has. The amount of memory in your computer stays the same...
  it's just that you've told BASIC not to use some of it. Type:

    PRINT FRE(0)-(SGN(FRE(0))<0)*65535

    The number displayed is the amount of memory space left unused. Now
  type the following:

    POKE 52148:POKE56,48:CLR

  Now type:

    PRINT FRE(0)-(SGN(FRE(0))<0)*65535

  See the change? BASIC now thinks it has less memory to work with. The
  memory you just claimed from BASIC is where you are going to put your
  character set, safe from actions of BASIC.
    The next step is to put your characters into RAM. When you begin, there
  is random data beginning at 12288 ($3000 HEX). You must put character
  patterns in RAM (in the same style as the ones in ROM) for the VIC-II
  chip to use.
    The following program moves 64 characters from ROM to your character
  set RAM:

  5 printchr$(142)               :rem switch to upper case
  10 poke52,48:poke 56,48:clr    :rem reserve memory for characters
  20 poke56334,peek(56334)and254 :rem turn off keyscan interrupt timer
  30 poke1,peek(1)and251         :rem switch in character
  40 fori=0to511:pokei+12288,peek(i+53248):next
  50 poke1,peek(1)or4            :rem switch in i/o
  60 poke56334,peek(56334)or1    :rem restart keyscan interrupt timer
  70 end

    Now POKE location 53272 with (PEEK(53272)AND240)+12. Nothing happens,
  right? Well, almost nothing. The Commodore 64 is now getting it's
  character information from your RAM, instead of from ROM. But since we
  copied the characters from ROM exactly, no difference can be seen... yet.
    You can easily change the characters now. Clear the screen and type
  an @ sign. Move the cursor down a couple of lines, then type:

  FOR I=12288 TO 12288+7:POKE 1,255-PEEK(I):NEXT

  You just created a reversed @ sign!

  +-----------------------------------------------------------------------+
  | TIP: Reversed characters are just characters with their bit patterns  |
  | in character memory reversed.                                         |
  +-----------------------------------------------------------------------+

    Now move the cursor up to the program again and hit <RETURN> again to
  re-reverse the character (bring it back to normal). By looking at the
  table of screen display codes, you can figure out where in RAM each
  character is. Just remember that each character takes eight memory
  locations to store. Here's a few examples just to get you started:

  +-----------+--------------+--------------------------------------------+
  | CHARACTER | DISPLAY CODE |      CURRENT STARTING LOCATION IN RAM      |
  +-----------+--------------+--------------------------------------------+
  |     @     |       0      |                    1228                    |
  |     A     |       1      |                   12296                    |
  |     !     |      33      |                   12552                    |
  |     >     |      62      |                   12784                    |
  +-----------+--------------+--------------------------------------------+

    Remember that we only took the first 64 characters. Something else will
  have to be done if you want one of the other characters.
    What if you wanted character number 154, a reversed Z? Well, you could
  make it yourself, by reversing a Z, or you could copy the set of reversed
  characters from the ROM, or just take the one character you want from ROM
  and replace one of the characters you have in RAM that you don't need.

    Suppose you decide that you won't need the > sign. Let's replace the
  > sign with the reversed Z. Type this:

    FOR I=0 TO 7:POKE 12784+I,255-PEEK(I+12496):NEXT

    Now type a > sign. It comes up as a reversed Z. No matter how many
  times you type the >, it comes out as a reversed Z. (This change is
  really an illusion. Though the > sign looks like a reversed Z, it still
  acts like a > in a program. Try something that needs a > sign. It will
  still work fine, only it will look strange.)
    A quick review: You can now copy characters from ROM into RAM. You can
  even pick and choose only the ones you want. There's only one step left
  in programmable characters (the best step!)... making your own
  characters.
    Remember how characters are stored in ROM? Each character is stored as
  a group of eight bytes. The bit patterns of the bytes directly control
  the character. If you arrange 8 bytes, one on top of another, and write
  out each byte as eight binary digits, it forms an eight by eight matrix,
  looking like the characters. When a bit is a one, there is a dot at that
  location. When a bit is a zero, there is a space at that location. When
  creating your own characters, you set up the same kind of table in
  memory. Type NEW and then type this program:

    10 FOR I=12448 TO 12455: READ A:POKE I,A:NEXT
    20 DATA 60, 66, 165, 129, 165, 153, 66, 60

  Now type RUN. The program will replace the letter T with a smile face
  character. Type a few T's to see the face. Each of the numbers in the
  DATA statement in line 20 is a row in the smile face character. The
  matrix for the face looks like this:

           76543210          BINARY      DECIMAL

          +--------+
    ROW 0 |  ****  |        00111100        60
        1 | *    * |        01000010        66
        2 |* *  * *|        10100101       165
        3 |*      *|        10000001       129
        4 |* *  * *|        10100101       165
        5 |*  **  *|        10011001       153
        6 | *    * |        01000010        66
    ROW 7 |  ****  |        00111100        60
          +--------+

                               7 6 5 4 3 2 1 0

                              +-+-+-+-+-+-+-+-+
                            0 | | | | | | | | |
                              +-+-+-+-+-+-+-+-+
                            1 | | | | | | | | |
                              +-+-+-+-+-+-+-+-+
                            2 | | | | | | | | |
                              +-+-+-+-+-+-+-+-+
                            3 | | | | | | | | |
                              +-+-+-+-+-+-+-+-+
                            4 | | | | | | | | |
                              +-+-+-+-+-+-+-+-+
                            5 | | | | | | | | |
                              +-+-+-+-+-+-+-+-+
                            6 | | | | | | | | |
                              +-+-+-+-+-+-+-+-+
                            7 | | | | | | | | |
                              +-+-+-+-+-+-+-+-+

                 Figure 3-1. Programmable Character Worksheet.

    The Programmable Character Worksheet (Figure 3-1) will help you design
  your own characters. There is an 8 by 8 matrix on the sheet, with row
  numbers, and numbers at the top of each column. (if you view each row as
  a binary word, the numbers are the value of that bit position. Each is a
  power of 2. The leftmost bit is equal to 128 or 2 to the 7th power, the
  next is equal to 64 or 2 to the 6th, and so on, until you reach the
  rightmost bit (bit 0) which is equal to 1 or 2 to the 0 power.)
    Place an X on the matrix at every location where you want a dot to be
  in your character. When your character is ready you can create the DATA
  statement for your character.
    Begin with the first row. Wherever you placed an X, take the number at
  the top of the column (the power-of-2 number, as explained above) and
  write it down. When you have the numbers for every column of the first
  row, add them together. \Mite this number down, next to the row. This is
  the number that you will put into the DATA statement to draw this row.
    Do the same thing with all of the other rows (1-7). When you are
  finished you should have 8 numbers between 0 and 255. If any of your
  numbers are not within range, recheck your addition. The numbers must be
  in this range to be correct! If you have less than 8 numbers, you missed
  a row. It's OK if some are 0. The 0 rows are just as important as the
  other numbers.
    Replace the numbers in the DATA statement in line 20 with the numbers
  you just calculated, and RUN the program. Then type a T. Every time you
  type it, you'll see your own character!
    If you don't like the way the character turned out, just change the
  numbers in the DATA statement and re-RUN the program until you are happy
  with your character.
    That's all there is to it!

  +-----------------------------------------------------------------------+
  | HINT: For best results, always make any vertical lines in your        |
  | characters at least 2 dots (bits) wide. This helps prevent CHROMA     |
  | noise (color distortion) on your characters when they are displayed   |
  | on a TV screen.                                                       |
  +-----------------------------------------------------------------------+

    Here is an example of a program using standard programmable characters:

  10 rem * example 1 *
  20 rem creating programmable characters
  31 poke 56334,peek(56334)and254: rem turn off kb
  32 poke 1,peek(1)and251: rem turn off i/o
  35 for i=0to63: rem character range to be copied
  36 for j=0to7: rem copy all 8 bytes per character
  37 poke 12288+I*8+j,peek(53248+i*8+j): rem copy a byte
  38 next j:next i: rem goto next byte or character
  39 poke 1,peek(1)or4:poke 56334,peek(56334)or1: rem turn on i/O and kb
  40 poke 53272,(peek(53272)and240)+12: rem set char pointer to mem. 12288
  60 for char=60to63: rem program characters 60 thru 63
  80 for byte=0to7: rem do all 8 bytes of a character
  100 read number: rem read in 1/8th of character data
  120 poke 12288+(8*char)+byte,number: rem store the data in memory
  140 next byte:next char: rem also could be next byte, char
  150 print chr$(147)tab(255)chr$(60);
  155 print chr$(61)tab(55)chr$(62)chr$(63)
  160 rem line 150 puts the newly defined characters on the screen
  170 get a$: rem wait for user to press a key
  180 if a$=""then goto170: rem if no keys were pressed, try again!
  190 poke 53272,21: rem return to normal characters
  200 data 4,6,7,5,7,7,3,3: rem data for character 60
  210 data 32,96,224,160,224,224,192,192: rem data for character 61
  220 data 7,7,7,31,31,95,143,127: rem data for character 62
  230 data 224,224,224,248,248,248,240,224: rem data for character 63
  240 end

  MULTI-COLOR MODE GRAPHICS

    Standard high-resolution graphics give you control of very small dots
  on the screen. Each dot in character memory can have 2 possible values,
  1 for on and 0 for off. When a dot is off, the color of the screen is
  used in the space reserved for that dot. If the dot is on, the dot is
  colored with the character color you have chosen for that screen posi-
  tion. When you're using standard high-resolution graphics, all the dots
  within each 8X8 character can either have background color or foreground
  color. In some ways this limits the color resolution within that space.
  For example, problems may occur when two different colored lines cross.
    Multi-color mode gives you a solution to this problem. Each dot in
  multi-color mode can be one of 4 colors: screen color (background color
  register #0), the color in background register #1, the color in back-
  ground color register #2, or character color. The only sacrifice is in
  the horizontal resolution, because each multi-color mode dot is twice as
  wide as a high-resolution dot. This minimal loss of resolution is more
  than compensated for by the extra abilities of multi-color mode.

  MULTI-COLOR MODE BIT

    To turn on multi-color character mode, set bit 4 of the VIC-II control
  register at 53270 ($D016) to a 1 by using the following POKE:

    POKE 53270,PEEK(53270)OR 16

    To turn off multi-color character mode, set bit 4 of location 53270 to
  a 0 by the following POKE:

    POKE 53270,PEEK(53270)AND 239

    Multi-color mode is set on or off for each space on the screen, so that
  multi-color graphics can be mixed with high-resolution (hi-res) graphics.
  This is controlled by bit 3 in color memory. Color memory begins at
  location 55296 ($D800 in HEX). If the number in color memory is less than
  8 (0-7) the corresponding space on the video screen will be standard
  hi-res, in the color (0-7) you've chosen. If the number located in color
  memory is greater or equal to 8 (from 8 to 15), then that space will be
  displayed in multi-color mode.

    By POKEing a number into color memory, you can change the color of the
  character in that position on the screen. POKEing a number from 0 to 7
  gives the normal character colors. POKEing a number between 8 and 15 puts
  the space into multi-color mode. In other words, turning BIT 3 ON in
  color memory, sets MULTI-COLOR MODE. Turning BIT 3 OFF in color memory,
  sets the normal, HIGH-RESOLUTION mode.
    Once multi-color mode is set in a space, the bits in the character
  determine which colors are displayed for the dots. For example, here is
  a picture of the letter A, and its bit pattern:

                          IMAGE    BIT PATTERN

                            **       00011000
                           ****      00111100
                          **  **     01100110
                          ******     01111110
                          **  **     01100110
                          **  **     01100110
                          **  **     01100110
                                     00000000

    In normal or high-resolution mode, the screen color is displayed
  everywhere there is a 0 bit, and the character color is displayed where
  the bit is a 1. Multi-color mode uses the bits in pairs, like so:

                          IMAGE    BIT PATTERN

                           AABB      00011000
                           CCCC      00111100
                         AABBAABB    01100110
                         AACCCCBB    01111110
                         AABBAABB    01100110
                         AABBAABB    01100110
                         AABBAABB    01100110
                                     00000000

    In the image area above, the spaces marked AA are drawn in the
  background #1 color, the spaces marked BB use the background #2 color,
  and the spaces marked CC use the character color. The bit pairs determine
  this, according to the following chart:

  +----------+--------------------------------------+---------------------+
  | BIT PAIR |          COLOR REGISTER              |       LOCATION      |
  +----------+--------------------------------------+---------------------+
  |    00    |  Background #0 color (screen color)  |   53281 ($D021)     |
  |    01    |  Background #l color                 |   53282 ($D022)     |
  |    10    |  Background #2 color                 |   53283 ($D023)     |
  |    11    |  Color specified by the              |   color RAM         |
  |          |  lower 3 bits in color memory        |                     |
  +----------+--------------------------------------+---------------------+

  Type NEW and then type this demonstration program:

  100 poke 53281,1: rem set background color #0 to white
  110 poke 53282,3: rem set background color #1 to cyan
  120 poke 53282,8: rem set background color #2 to orange
  130 poke 53270,peek(53270)or16: rem turn on multicolor mode
  140 c=13*4096+8*256: rem set c to point to color memory
  150 printchr$(147)"aaaaaaaaaa"
  160 forl=0to9
  170 pokec+l,8: rem use multi black
  180 next

    The screen color is white, the character color is black, one color
  register is cyan (greenish blue), the other is orange. You're not really
  putting color codes in the space for character color, you're actually
  using references to the registers associated with those colors. This
  conserves memory, since 2 bits can be used to pick 16 colors (background)
  or 8 colors (character). This also makes some neat tricks possible.
  Simply changing one of the indirect registers will change every dot drawn
  in that color. Therefore everything drawn in the screen and background

  colors can be changed on the whole screen instantly. Here is an example
  of changing background color register #1:

  100 poke53270,peek(53270)or16: rem turn on multicolor mode
  110 print chr$(147)chr$(18);
  120 print"{orange*2}";: rem type c= & 1 for orange or multicolor black bg
  130 forl=1to22:printchr$(65);:next
  135 fort=1to500:next
  140 print"{blue*2}";: rem type ctrl & 7 for blue color change
  145 fort=1to500:next
  150 print"{black}hit a key"
  160 get a$:if a$=""then160
  170 x=int(rnd(1)*16)
  180 poke 53282,x
  190 goto 160

    By using the <C=> key and the COLOR keys the characters can be changed
  to any color, including multi-color characters. For example, type this
  command:

    POKE 53270,PEEK(53270)OR 16:PRINT"<CTRL+3>";: rem lt.red/ multi-color
  red

    The word READY and anything else you type will be displayed in multi-
  color mode. Another color control can set you back to regular text.

    Here is an example of a program using multi-color programmable
  characters:

  10 rem * example 2 *
  20 rem creating multi color programmable characters
  31 poke 56334,peek(56334)and254:poke1,peek(1)and251
  35 fori=0to63:rem character range to be copied from rom
  36 forj=0to7:rem copy all 8 bytes per character
  37 poke 12288+i*8+j,peek(53248+i*8+j):rem copy a byte
  38 next j,i:rem goto next byte or character
  39 poke 1,peek(1)or4:poke 56334,peek(56334)or1:rem turn on i/o and kb
  40 poke 53272,(peek(53272)and240)+12:rem set char pointer to mem. 12288
  50 poke 53270,peek(53270)or16
  51 poke 53281,0:rem set background color #0 to black
  52 poke 53282,2:rem set background color #1 to red
  53 poke 53283,7:rem set background color #2 to yellow
  60 for char=60to63:rem program characters 60 thru 63
  80 for byte=0to7:rem do all 8 bytes of a character
  100 read number:rem read 1/8th of the character data
  120 poke 12288+(8*char)+byte,number:rem store the data in memory
  140 next byte,char
  150 print"{clear}"tab(255)chr$(60)chr$(61)tab(55)chr$(62)chr$(63)
  160 rem line 150 puts the newly defined characters on the screen
  170 get a$:rem wait for user to press a key
  180 if a$=""then170:rem if no keys were pressed, try again
  190 poke53272,21:poke53270,peek(53270)and239:rem return to normal chars
  200 data129,37,21,29,93,85,85,85: rem data for character 60
  210 data66,72,84,116,117,85,85,85: rem data for character 61
  220 data87,87,85,21,8,8,40,0: rem data for character 62
  230 data213,213,85,84,32,32,40,0: rem data for character 63
  240 end

  EXTENDED BACKGROUND COLOR MODE

    Extended background color mode gives you control over the background
  color of each individual character, as well as over the foreground color.
  For example, in this mode you could display a blue character with a
  yellow background on a white screen.
    There are 4 registers available for extended background color mode.
  Each of the registers can be set to any of the 16 colors.
    Color memory is used to hold the foreground color in extended back-
  ground mode. It is used the same as in standard character mode.
    Extended character mode places a limit on the number of different
  characters you can display, however. When extended color mode is on, only
  the first 64 characters in the character ROM (or the first 64 characters
  in your programmable character set) can be used. This is because two of
  the bits of the character code are used to select the background color.
  It might work something like this:
    The character code (the number you would POKE to the screen) of the
  letter "A" is a 1. When extended color mode is on, if you POKED a 1 to
  the screen, an "A" would appear. If you POKED a 65 to the screen
  normally, you would expect the character with character code (CHR$) 129
  to appear, which is a reversed "A." This does NOT happen in extended
  color mode. Instead you get the same unreversed "A" as before, but on a
  different background color. The following chart gives the codes:

  +------------------------+---------------------------+
  |     CHARACTER CODE     | BACKGROUND COLOR REGISTER |
  +------------------------+---------------------------+
  |  RANGE   BIT 7   BIT 6 |  NUMBER       ADDRESS     |
  +------------------------+---------------------------+
  |   0- 63   0       0    |    0       53281 ($D021)  |
  |  64-127   0       1    |    1       53282 ($D022)  |
  | 128-191   1       0    |    2       53283 ($D023)  |
  | 192-255   1       1    |    3       53284 ($D024)  |
  +------------------------+---------------------------+

    Extended color mode is turned ON by setting bit 6 of the VIC-II regis-
  ter to a 1 at location 53265 ($D011 in HEX). The following POKE does it:

    POKE 53265,PEEK(53265)OR 64

    Extended color mode is turned OFF by setting bit 6 of the VIC-II regis-
  ter to a 0 at location 53265 ($D011). The following statement will do
  this:

    POKE 53265,PEEK(53265)AND 191

  BIT MAPPED GRAPHICS

    When writing games, plotting charts for business applications, or other
  types of programs, sooner or later you get to the point where you want
  high-resolution displays.
    The Commodore 64 has been designed to do just that: high resolution is
  available through bit mapping of the screen. Bit mapping is the method in
  which each possible dot (pixel) of resolution on the screen is assigned
  its own bit (location) in memory. If that memory bit is a one, the dot it
  is assigned to is on. If the bit is set to zero, the dot is off.
    High-resolution graphic design has a couple of drawbacks, which is why
  it is not used all the time. First of all, it takes lots of memory to bit
  map the entire screen. This is because every pixel must have a memory bit
  to control it. You are going to need one bit of memory for each pixel
  (or one byte for 8 pixels). Since each character is 8 by 8, and there are
  40 lines with 25 characters in each line, the resolution is 320 pixels
  (dots) by 200 pixels for the whole screen. That gives you 64000 separate
  dots, each of which requires a bit in memory. In other words, 8000 bytes
  of memory are needed to map the whole screen.
    Generally, high-resolution operations are made of many short, simple,
  repetitive routines. Unfortunately, this kind of thing is usually rather
  slow if you are trying to write high-resolution routines in BASIC. How-
  ever, short, simple, repetitive routines are exactly what machine lan-
  guage does best. The solution is to either write your programs entirely
  in machine language, or call machine language, high-resolution sub-
  routines from your BASIC program using the SYS command from BASIC. That
  way you get both the ease of writing in BASIC, and the speed of machine
  language for graphics. The VSP cartridge is also available to add high-
  resolution commands to COMMODORE 64 BASIC.
    All of the examples given in this section will be in BASIC to make them
  clear. Now to the technical details.

    BIT MAPPING is one of the most popular graphics techniques in the
  computer world. It is used to create highly detailed pictures. Basically,
  when the Commodore 64 goes into bit map mode, it directly displays an

  8K section of memory on the TV screen. When in bit map mode, you can
  directly control whether an individual dot on the screen is on or off.
    There are two types of bit mapping available on the Commodore 64.
  They are:

    1) Standard (high-resolution) bit mapped mode (320-dot by 200-dot
       resolution)

    2) Multi-color bit mapped mode (160-dot by 200-dot resolution)

    Each is very similar to the character type it is named for: standard
  has greater resolution, but fewer color selections. On the other hand,
  multi-color bit mapping trades horizontal resolution for a greater number
  of colors in an 8-dot by 8-dot square.

  STANDARD HIGH-RESOLUTION BIT MAP MODE

    Standard bit map mode gives you a 320 horizontal dot by 200 vertical
  dot resolution, with a choice of 2 colors in each 8-dot by 8-dot section.
  Bit map mode is selected (turned ON) by setting bit 5 of the VIC-II
  control register to a 1 at location 53265 ($D011 in HEX). The following
  POKE will do this:

    POKE 53265,PEEK(53265)OR 32

    Bit map mode is turned OFF by setting bit 5 of the VIC-II control
  register to 0 at location 53265 ($D011), like this:

    POKE 53265,PEEK(53265)AND 223

    Before we get into the details of the bit map mode, there is one more
  issue to tackle, and that is where to locate the bit map area.

  HOW IT WORKS

    If you remember the PROGRAMMABLE CHARACTERS section you will recall
  that you were able to set the bit pattern of a character stored in RAM to
  almost anything you wanted. If at the same time you change the character
  that is displayed on the screen, you would be able to change a single
  dot, and watch it happen. This is the basis of bit-mapping. The entire

  screen is filled with programmable characters, and you make your changes
  directly into the memory that the programmable characters get their
  patterns from.
    Each of the locations in screen memory that were used to control what
  character was displayed, are now used for color information. For example,
  instead of POKEing a I in location 1024 to make an "A" appear in the top
  left hand corner of the screen, location 1024 now controls the colors of
  the bits in that top left space.
    Colors of squares in bit map mode do not come from color memory, as
  they do in the character modes. Instead, colors are taken from screen
  memory. The upper 4 bits of screen memory become the color of any bit
  that is set to 1 in the 8 by 8 area controlled by that screen memory
  location. The lower 4 bits become the color of any bit that is set to
  a 0.

  EXAMPLE: Type the following:

  5 BASE=2*4096:POKE53272,PEEK(53272)OR8:REM PUT BIT MAP AT 8192
  10 POKE53265,PEEK(53265)OR32:REM ENTER BIT MAP MODE

  Now RUN the program.
    Garbage appears on the screen, right? Just like the normal screen mode,
  you have to clear the HIGH-RESOLUTION (HI-RES) screen before you use it.
  Unfortunately, printing a CLR won't work in this case. Instead you have
  to clear out the section of memory that you're using for your
  programmable characters. Hit the <RUN/STOP> and <RESTORE> keys, then add
  the following lines to your program to clear the HI-RES screen:

  20 FORI=BASETOBASE+7999:POKEI,0:NEXT:REM CLEAR BIT
  30 FORI=1024TO2023:POKEI,3:NEXT:REM SET COLOR TO CYAN AND BLACK

    Now RUN the program again. You should see the screen clearing, then the
  greenish blue color, cyan, should cover the whole screen. What we want to
  do now is to turn the dots on and off on the HI-RES screen.

    To SET a dot (turn a dot ON) or UNSET a dot (turn a dot OFF) you must
  know how to find the correct bit in the character memory that you have to
  set to a 1. In other words, you have to find the character you need to
  change, the row of the character, and which bit of the row that you
  have to change. You need a formula to calculate this.
    We will use X and Y to stand for the horizontal and vertical positions
  of a dot, The dot where X=0 and Y=0 is at the upper-left of the display.
  Dots to the right have higher X values, and the dots toward the bottom
  have higher Y values. The best way to use bit mapping is to arrange the
  bit map display something like this:

  0. . . . . . . . . . . . . . . . . .X. . . . . . . . . . . . . . . . .319

  .                                                                      .

  .                                                                      .

  .                                                                      .

  .                                                                      .

  Y                                                                      .

  .                                                                      .

  .                                                                      .

  .                                                                      .

  .                                                                      .

  199. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

    Each dot will have an X and a Y coordinate. With this format it is easy
  to control any dot on the screen.

     However, what you actually have is something like this:

  ----- BYTE 0   BYTE 8   BYTE 16    BYTE 24 ..................... BYTE 312
        BYTE 1   BYTE 9      .          .                          BYTE 313
        BYTE 2   BYTE 10     .          .                          BYTE 314
        BYTE 3   BYTE 11     .          .                          BYTE 315
        BYTE 4   BYTE 12     .          .                          BYTE 316
        BYTE 5   BYTE 13     .          .                          BYTE 317
        BYTE 6   BYTE 14     .          .                          BYTE 318
  ----- BYTE 7   BYTE 15     .          .                          BYTE 319

  ----- BYTE 320 BYTE 328 BYTE 336 BYTE 344....................... BYTE 632
        BYTE 321 BYTE 329    .          .                          BYTE 633
        BYTE 322 BYTE 330    .          .                          BYTE 634
        BYTE 323 BYTE 331    .          .                          BYTE 635
        BYTE 324 BYTE 332    .          .                          BYTE 636
        BYTE 325 BYTE 333    .          .                          BYTE 637
        BYTE 326 BYTE 334    .          .                          BYTE 638
  ----- BYTE 327 BYTE 335    .          .                          BYTE 639

    The programmable characters which make up the bit map are arranged in
  25 rows of 40 columns each. While this is a good method of organization
  for text, it makes bit mapping somewhat difficult. (There is a good
  reason for this method. See the section on MIXED MODES.)
    The following formula will make it easier to control a dot on the bit
  map screen:
    The start of the display memory area is known as the BASE, The row
  number (from 0 to 24) of your dot is:

    ROW = INT(Y/8) (There are 320 bytes per line.)

  The character position on that line (from 0 to 39) is:

    CHAR = INT(X/8) (There are 8 bytes per character.)

  The line of that character position (from 0 to 7) is:

    LINE = Y AND 7

  The bit of that byte is:

    BIT = 7-(X AND 7)

    Now we put these formulas together. The byte in which character memory
  dot (X,Y) is located is calculated by:

    BYTE = BASE + ROW*320+ CHAR*8 + LINE

    To turn on any bit on the grid with coordinates (X,Y), use this line:

  POKE BYTE, PEEK(BYTE) OR 2^BIT

    Let's add these calculations to the program. In the following example,
  the COMMODORE 64 will plot a sine curve:

  50 FORX=0TO319STEP.5:REM WAVE WILL FILL THE SCREEN
  60 Y=INT(90+80*SIN(X/10))
  70 CH=INT(X/8)
  80 RO=INT(Y/8)
  85 LN=YAND7
  90 BY=BASE+RO*320+8*CH+LN
  100 BI=7-(XAND7)
  110 POKEBY,PEEK(BY)OR(2^BI)
  120 NEXTX
  125 POKE1024,16
  130 GOTO130

    The calculation in line 60 will change the values for the sine function
  from a range of +1 to -1 to a range of 10 to 170. Lines 70 to 100
  calculate the character, row, byte, and bit being affected, using the
  formulae as shown above. Line 125 signals the program is finished by
  changing the color of the top left corner of the screen. Line 130 freezes
  the program by putting it into an infinite loop. When you have finished
  looking at the display, just hold down <RUN/STOP> and hit <RESTORE>.

    As a further example, you can modify the sine curve program to display
  a semicircle. Here are the lines to type to make the changes:

  50 FORX=0TO160:REM DO HALF THE SCREEN
  55 Y1=100+SQR(160*X-X*X)
  56 Y2=100-SQR(160*X-X*X)
  60 FORY=Y1TOY2STEPY1-Y2
  70 CH=INT(X/()
  80 RO=INT(Y/X)
  85 LNYAND7
  90 BY=BASE+RO*320+8*CH+LN
  100 BI=7-(XAND7)
  110 POKEBY,PEEK(BY)OR(2^BI)
  114 NEXT

  This will create a semicircle in the HI-RES area of the screen.

  +-----------------------------------------------------------------------+
  | WARNING: BASIC variables can overlay your high-resolution screen. If  |
  | you need more memory space you must move the bottom of BASIC above the|
  | high-resolution screen area. Or, you must move your high-resolution   |
  | screen area. This problem will NOT occur in machine language. It ONLY |
  | happens when you're writing programs in BASIC.                        |
  +-----------------------------------------------------------------------+

  MULTI-COLOR BET MAP MODE

    Like multi-color mode characters, multi-color bit map mode allows you
  to display up to four different colors in each 8 by 8 section of bit map.
  And as in multi-character mode, there is a sacrifice of horizontal
  resolution (from 320 dots to 160 dots).
    Multi-color bit map mode uses an 8K section of memory for the bit map.
  You select your colors for multi-color bit map mode from (1) the
  background color register 0, (the screen background color), (2) the video
  matrix (the upper 4 bits give one possible color, the lower 4 bits an-
  other), and (3) color memory.
    Multi-color bit mapped mode is turned ON by setting bit 5 of 53265
  ($D011) and bit 4 at location 53270 ($D016) to a 1. The following POKE
  does this:

    POKE 53265,PEEK(53625)OR 32: POKE 53270,PEEK(53270)OR 16

    Multi-color bit mapped mode is turned OFF by setting bit 5 of 53265
  ($D011) and bit 4 at location 53270 ($D016) to a 0. The following POKE
  does this:

    POKE 53265,PEEK(53265)AND 223: POKE 53270,PEEK(53270)AND 239

    As in standard (HI-RES) bit mapped mode, there is a one to one cor-
  respondence between the 8K section of memory being used for the display,
  and what is shown on the screen. However, the horizontal dots are two
  bits wide. Each 2 bits in the display memory area form a dot, which can
  have one of 4 colors.

    BITS    COLOR INFORMATION COMES FROM

     00     Background color #0 (screen color)
     01     Upper 4 bits of screen memory
     10     Lower 4 bits of screen memory
     11     Color nybble (nybble = 1/2 byte = 4 bits)

  SMOOTH SCROLLING

    The VIC-II chip supports smooth scrolling in both the horizontal and
  vertical directions. Smooth scrolling is a one pixel movement of the
  entire screen in one direction. It can move either UP, or down, or left,
  or right. It is used to move new information smoothly onto the screen,
  while smoothly removing characters from the other side.
    While the VIC-II chip does much of the task for you, the actual scroll-
  ing must be done by a machine language program. The VIC-II chip features
  the ability to place the video screen in any of 8 horizontal positions,
  and 8 vertical positions. Positioning is controlled by the VIC-II
  scrolling registers. The VIC-II chip also has a 38 column mode, and a 24
  row mode. the smaller screen sizes are used to give you a place for your
  new data to scroll on from.

  The following are the steps for SMOOTH SCROLLING:

  1) Shrink the screen (the border will expand).
  2) Set the scrolling register to maximum (or minimum value depending upon
     the direction of your scroll).
  3) Place the new data on the proper (covered) portion of the screen.
  4) Increment (or decrement) the scrolling register until it reaches the
     maximum (or minimum) value.
  5) At this point, use your machine language routine to shift the entire
     screen one entire character in the direction of the scroll.
  6) Go back to step 2.

    To go into 38 column mode, bit 3 of location 53270 ($D016) must be set
  to a 0. The following POKE does this:

    POKE 53270,PEEK(53270)AND 247

    To return to 40 column mode, set bit 3 of location 53270 ($D016) to a
  1.The following POKE does this:

    POKE 53270,PEEK(53270)OR 8

    To go into 24 row mode, bit 3 of location 53265 ($D011) must be set to
  a 0. The following POKE will do this:

    POKE 53265,PEEK(53265)AND 247

    To return to 25 row mode, set bit 3 of location 53265 ($D011) to a 1.
  The following POKE does this:

    POKE 53265,PEEK(53265)OR 8

    When scrolling in the X direction, it is necessary to place the VIC-II
  chip into 38 column mode. This gives new data a place to scroll from.
  When scrolling LEFT, the new data should be placed on the right. When
  scrolling RIGHT the new data should be placed on the left. Please note
  that there are still 40 columns to screen memory, but only 38 are
  visible.
    When scrolling in the Y direction, it is necessary to place the VIC-II
  chip into 24 row mode. When scrolling UP, place the new data in the LAST
  row. When scrolling DOWN, place the new data on the FIRST row. Unlike X
  scrolling, where there are covered areas on each side of the screen,
  there is only one covered area in Y scrolling. When the Y scrolling

  register is set to 0, the first line is covered, ready for new data. When
  the Y scrolling register is set to 7 the last row is covered.
    For scrolling in the X direction, the scroll register is located in
  bits 2 to 0 of the VIC-II control register at location 53270 ($D016 in
  HEX). As always, it is important to affect only those bits. The following
  POKE does this:

    POKE 53270,(PEEK(53270)AND 248)+X

  where X is the X position of the screen from 0 to 7.
    For scrolling in the Y direction, the scroll register is located in
  bits 2 to 0 of the VIC-II control register at location 53265 ($D011 in
  HEX). As always, it is important to affect only those bits. The following
  POKE does this:

    POKE 53265,(PEEK(53265)AND 248)+Y

  where Y is the Y position of the screen from 0 to 7.
    To scroll text onto the screen from the bottom, you would step the low-
  order 3 bits of location 53265 from 0-7, put more data on the covered
  line at the bottom of the screen, and then repeat the process. To scroll
  characters onto the screen from left to right, you would step the low-
  order 3 bits of location 53270 from 0 to 7, print or POKE another column
  of new data into column 0 of the screen, then repeat the process.
    If you step the scroll bits by -1, your text will move in the opposite
  direction.

  EXAMPLE: Text scrolling onto the bottom of the screen:

  10 poke53265,peek(53265)and247        :rem go into 24 row mode
  20 printchr$(147)                     :rem clear the screen
  30 forx=1to24:printchr$(17);:next     :rem move the cursor to the bottom
  40 poke53265,(peek(53265)and248)+7:print :rem position for 1st scroll
  50 print"     hello";
  60 forp=6to0step-1
  70 poke53265,(peek(53265)and248)+p
  80 forx=1to50:next                    :rem delay loop
  90 next:goto40
