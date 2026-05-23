> Source: c64prg.txt §Chapter 3 "Programming Graphics on the Commodore 64", sprites portion (Sprites through "Programming Sprites - Another Look", to end of chapter). Lightly cleaned from the Project 64 etext.

  SPRITES

    A SPRITE is a special type of user definable character which can be
  displayed anywhere on the screen. Sprites are maintained directly by the
  VIC-II chip. And all you have to do is tell a sprite "what to look like,"
  "what color to be," and "where to appear." The VIC-II chip will do the
  rest! Sprites can be any of the 16 colors available.
    Sprites can be used with ANY of the other graphics modes, bit mapped,
  character, multi-color, etc., and they'll keep their shape in all of
  them. The sprite carries its own color definition, its own mode (HI-RES
  or multi-colored), and its own shape.
    Up to 8 sprites at a time can be maintained by the VIC-II chip auto-
  matically. More sprites can be displayed using RASTER INTERRUPT
  techniques.

    The features of SPRITES include:

    1) 24 horizontal dot by 21 vertical dot size.
    2) Individual color control for each sprite.
    3) Sprite multi-color mode.
    4) Magnification (2x) in horizontal, vertical, or both directions.
    5) Selectable sprite to background priority.
    6) Fixed sprite to sprite priorities.
    7) Sprite to sprite collision detection.
    8) Sprite to background collision detection.

    These special sprite abilities make it simple to program many arcade
  style games. Because the sprites are maintained by hardware, it is even
  possible to write a good quality game in BASIC!
    There are 8 sprites supported directly by the VIC-II chip. They are
  numbered from 0 to 7. Each of the sprites has it own definition location,
  position registers and color register, and has its own bits for enable
  and collision detection.

  DEFINING A SPRITE

    Sprites are defined like programmable characters are defined. However,
  since the size of the sprite is larger, more bytes are needed. A sprite
  is 24 by 21 dots, or 504 dots. This works out to 63 bytes (504/8 bits)

                          [THE PICTURE IS MISSING!]

                    Figure 3-2. Sprite Definition Block.

  needed to define a sprite. The 63 bytes are arranged in 21 rows of 3
  bytes each. A sprite definition looks like this.

                          BYTE 0  BYTE 1  BYTE 2
                          BYTE 3  BYTE 4  BYTE 5
                          BYTE 6  BYTE 7  BYTE 8
                            ..      ..      ..
                            ..      ..      ..
                            ..      ..      ..
                          BYTE 60 BYTE 61 BYTE 62

    Another way to view how a sprite is created is to take a look at the
  sprite definition block on the bit level. It would look something like
  Figure 3-2.
    In a standard (HI-RES) sprite, each bit set to I is displayed in that
  sprite's foreground color. Each bit set to 0 is transparent and will
  display whatever data is behind it. This is similar to a standard
  character.
    Multi-color sprites are similar to multi-color characters. Horizontal
  resolution is traded for extra color resolution. The resolution of the
  sprite becomes 12 horizontal dots by 21 vertical dots. Each dot in the
  sprite becomes twice as wide, but the number of colors displayable in the
  sprite is increased to 4.

  SPRITE POINTERS

    Even though each sprite takes only 63 bytes to define, one more byte
  is needed as a place holder at the end of each sprite. Each sprite, then,
  takes up 64 bytes. This makes it easy to calculate where in memory your
  sprite definition is, since 64 bytes is an even number and in binary it's
  an even power.
    Each of the 8 sprites has a byte associated with it called the SPRITE
  POINTER. The sprite pointers control where each sprite definition is lo-
  cated in memory. These 8 bytes are always located as the lost 8 bytes
  of the 1K chunk of screen memory. Normally, on the Commodore 64, this
  means they begin at location 2040 ($07F8 in HEX). However, if you move
  the screen, the location of your sprite pointers will also move.
    Each sprite pointer can hold a number from 0 to 255. This number points
  to the definition for that sprite. Since each sprite definition takes
  64 bytes, that means that the pointer can "see" anywhere in the 16K
  block of memory that the VIC-II chip can access (since 256*64=16K).

    If sprite pointer #0, at location 2040, contains the number 14, for
  example, this means that sprite 0 will be displayed using the 64 bytes
  beginning at location 14*64 = 896 which is in the cassette buffer. The
  following formula makes this clear:

    LOCATION = (BANK * 16384) + (SPRITE POINTER VALUE * 64)

  Where BANK is the 16K segment of memory that the VIC-II chip is looking
  at and is from 0 to 3.
    The above formula gives the start of the 64 bytes of the sprite
  definition block.
    When the VIC-II chip is looking at BANK 0 or BANK 2, there is a ROM
  IMAGE of the character set present in certain locations, as mentioned
  before. Sprite definitions can NOT be placed there. If for some reason
  you need more than 128 different sprite definitions, you should use one
  of the banks without the ROM IMAGE, 1 or 3.

  TURNING SPRITES ON

    The VIC-II control register at location 53269 ($D015 in HEX) is known
  as the SPRITE ENABLE register. Each of the sprites has a bit in this
  register which controls whether that sprite is ON or OFF. The register
  looks like this:

                     $D015  7 6 5 4 3 2 1 0

    To turn on sprite 1, for example, it is necessary to turn that bit to
  a 1. The following POKE does this:

    POKE 53269.PEEK(53269)OR 2

  A more general statement would be the following:

    POKE 53269,PEEK(53269)OR (2^SN)

  where SN is the sprite number, from 0 to 7.

  +-----------------------------------------------------------------------+
  | NOTE: A sprite must be turned ON before it can be seen.               |
  +-----------------------------------------------------------------------+

  TURNING SPRITES OFF

    A sprite is turned off by setting its bit in the VIC-II control
  register at 53269 ($D015 in HEX) to a 0. The following POKE will do this:

    POKE 53269,PEEK(53269)AND(255-2^SN)

  where SN is the sprite number from 0 to 7.

  COLORS

    A sprite can be any of the 16 colors generated by the VIC-II chip. Each
  of the sprites has its own sprite color register. These are the memory
  locations of the color registers:

            ADDRESS         |          DESCRIPTION
  --------------------------+----------------------------------------------
        53287   ($D027)     |    SPRITE 0 COLOR REGISTER
        53288   ($D028)     |    SPRITE 1 COLOR REGISTER
        53289   ($D029)     |    SPRITE 2 COLOR REGISTER
        53290   ($D02A)     |    SPRITE 3 COLOR REGISTER
        53291   ($D02B)     |    SPRITE 4 COLOR REGISTER
        53292   ($D02C)     |    SPRITE 5 COLOR REGISTER
        53293   ($D02D)     |    SPRITE 6 COLOR REGISTER
        53294   ($D02E)     |    SPRITE 7 COLOR REGISTER

    All dots in the sprite will be displayed in the color contained in the
  sprite color register. The rest of the sprite will be transparent, and
  will show whatever is behind the sprite.

  MULTI-COLOR MODE

    Multi-color mode allows you to have up to 4 different colors in each
  sprite. However, just like other multi-color modes, horizontal resolution
  is cut in half. In other words, when you're working with sprite multi-
  color mode (like in multi-color character mode), instead of 24 dots
  across the sprite, there are 12 pairs of dots. Each pair of dots is
  called a BIT PAIR. Think of each bit pair (pair of dots) as a single dot
  in your overall sprite when it comes to choosing colors for the dots in
  your sprites. The table below gives you the bit pair values needed to

  turn ON each of the four colors you've chosen for your sprite:

    BIT PAIR                           DESCRIPTION
  -------------------------------------------------------------------------
      00        TRANSPARENT, SCREEN COLOR
      01        SPRITE MULTI-COLOR REGISTER #0 (53285) ($D025)
      10        SPRITE COLOR REGISTER
      11        SPRITE MULTI-COLOR REGISTER #I (53286) ($D026)
  +-----------------------------------------------------------------------+
  | NOTE: The sprite foreground color is a 10. The character foreground   |
  | is a 11.                                                              |
  +-----------------------------------------------------------------------+

  SETTING A SPRITE TO MULTI-COLOR MODE

    To switch a sprite into multi-color mode you must turn ON the VIC-II
  control register at location 53276 ($D01C). The following POKE does this:

    POKE 53276,PEEK(53276)OR(2^SN)

  where SN is the sprite number (0 to 7).
    To switch a sprite out of multi-color mode you must turn OFF the VIC-II
  control register at location 53276 ($D01C). The following POKE does this:

    POKE 53276,PEEK(53276)AND(255-2^SN)

  where SN is the sprite number (0 to 7).

  EXPANDED SPRITES

    The VIC-II chip has the ability to expand a sprite in the vertical
  direction, the horizontal direction, or both at once. When expanded, each
  dot in the sprite is twice as wide or twice as tall. Resolution doesn't
  actually increase... the sprite just gets bigger.
    To expand a sprite in the horizontal direction, the corresponding bit
  in the VIC-II control register at location 53277 ($D01D in HEX) must be
  turned ON (set to a 1). The following POKE expands a sprite in the X
  direction:

    POKE 53277,PEEK(53277)OR(2^SN)

  where SN is the sprite number from 0 to 7.

    To unexpand a sprite in the horizontal direction, the corresponding bit
  in the VIC-II control register at location 53277 ($D01D in HEX) must be
  turned OFF (set to a 0). The following POKE "unexpands" a sprite in the
  X direction:

    POKE 53277,PEEK(53277)AND (255-2^SN)

  where SN is the sprite number from 0 to 7.
    To expand a sprite in the vertical direction, the corresponding bit in
  the VIC-II control register at location 53271 ($D017 in HEX) must be
  turned ON (set to a 1). The following POKE expands a sprite in the Y
  direction:

    POKE 53271,PEEK(53271)OR(2^SN)

  where SN is the sprite number from 0 to 7.

    To unexpand a sprite in the vertical direction, the corresponding bit
  in the VIC-II control register at location 53271 ($D017 in HEX) must be
  turned OFF (set to a 0). The following POKE "unexpands" a sprite in the
  Y direction:

    POKE 53271,PEEK(53271)AND (255-2^SN)

  where SN is the sprite number from 0 to 7.

  SPRITE POSITIONING

    Once you've made a sprite you want to be able to move it around the
  screen. To do this, your Commodore 64 uses three positioning registers:

    1) SPRITE X POSITION REGISTER
    2) SPRITE Y POSITION REGISTER
    3) MOST SIGNIFICANT BIT X POSITION REGISTER

    Each sprite has an X position register, a Y position register, and a
  bit in the X most significant bit register. This lets you position your
  sprites very accurately. You can place your sprite in 512 possible X
  positions and 256 possible Y positions.
    The X and Y position registers work together, in pairs, as a team. The
  locations of the X and Y registers appear in the memory map as follows:
  First is the X register for sprite 0, then the Y register for sprite 0.

  Next comes the X register for sprite 1, the Y register for sprite 1, and
  so on. After all 16 X and Y registers comes the most significant bit in
  the X position (X MSB) located in its own register.
    The chart below lists the locations of each sprite position register.
  You use the locations at their appropriate time through POKE statements:

  +-------------------+---------------------------------------------------+
  |     LOCATION      |                                                   |
  +---------+---------+                   DESCRIPTION                     |
  | DECIMAL |   HEX   |                                                   |
  +---------+---------+---------------------------------------------------+
  |  53248  | ($D000) |     SPRITE 0 X POSITION REGISTER                  |
  |  53249  | ($D001) |     SPRITE 0 Y POSITION REGISTER                  |
  |  53250  | ($D002) |     SPRITE 1 X POSITION REGISTER                  |
  |  53251  | ($D003) |     SPRITE 1 Y POSITION REGISTER                  |
  |  53252  | ($D004) |     SPRITE 2 X POSITION REGISTER                  |
  |  53253  | ($D005) |     SPRITE 2 Y POSITION REGISTER                  |
  |  53254  | ($D006) |     SPRITE 3 X POSITION REGISTER                  |
  |  53255  | ($D007) |     SPRITE 3 Y POSITION REGISTER                  |
  |  53256  | ($D008) |     SPRITE 4 X POSITION REGISTER                  |
  |  53257  | ($D009) |     SPRITE 4 Y POSITION REGISTER                  |
  |  53258  | ($D00A) |     SPRITE 5 X POSITION REGISTER                  |
  |  53259  | ($D00B) |     SPRITE 5 Y POSITION REGISTER                  |
  |  53260  | ($D00C) |     SPRITE 6 X POSITION REGISTER                  |
  |  53261  | ($D00D) |     SPRITE 6 Y POSITION REGISTER                  |
  |  53262  | ($D00E) |     SPRITE 7 X POSITION REGISTER                  |
  |  53263  | ($D00F) |     SPRITE 7 Y POSITION REGISTER                  |
  |  53264  | ($D010) |     SPRITE X MSB REGISTER                         |
  +---------+---------+---------------------------------------------------+

    The position of a sprite is calculated from the TOP LEFT corner of the
  24 dot by 21 dot area that your sprite can be designed in. It does NOT
  matter how many or how few dots you use to make up a sprite. Even if only
  one dot is used as a sprite, and you happen to want it in the middle of
  the screen, you must still calculate the exact positioning by starting at
  the top left corner location.

  VERTICAL POSITIONING

    Setting up positions in the horizontal direction is a little more
  difficult than vertical positioning, so we'll discuss vertical (Y)
  positioning first.

    There are 200 different dot positions that can be individually pro-
  grammed onto your TV screen in the Y direction. The sprite Y position
  registers can handle numbers up to 255. This means that you have more
  than enough register locations to handle moving a sprite up and down. You
  also want to be able to smoothly move a sprite on and off the screen.
  More than 200 values are needed for this.
    The first on-screen value from the top of the screen, and in the Y
  direction for an unexpanded sprite is 30. For a sprite expanded in the Y
  direction it would be 9. (Since each dot is twice as tall, this makes a
  certain amount of sense, as the initial position is STILL calculated from
  the top left corner of the sprite.)
    The first Y value in which a sprite (expanded or not) is fully on the
  screen (all 21 possible lines displayed) is 50.
    The last Y value in which an unexpanded sprite is fully on the screen
  is 229. The last Y value in which an expanded sprite is fully on the
  screen is 208.
    The first Y value in which a sprite is fully off the screen is 250.

  EXAMPLE:

  10 print"{clear}"                :rem clear screen
  20 poke 2040,13                  :rem get sprite 0 data from block 13
  30 fori=0to62:poke832+i,129:next :rem poke sprite data into block 13
  40 v=53248                       :rem set beginning of video chip
  50 pokev+21,1                    :rem enable sprite 0
  60 pokev+39,1                    :rem set sprite 0 color
  70 pokev+1,100                   :rem set sprite 0 y position
  80 pokev+16,0:pokev,100          :rem set sprite 0 x position

  HORIZONTAL POSITIONING

    Positioning in the horizontal direction is more complicated because
  there are more than, 256 positions. This means that an extra bit, or 9th
  bit is used to control the X position. By adding the extra bit when
  necessary a sprite now has 512 possible positions in the left/right, X,
  direction. This makes more possible combinations than can be seen on the
  visible part of the screen. Each sprite can have a position from 0 to
  511. However, only those values between 24 and 343 are visible on the
  screen. If the X position of a sprite is greater than 255 (on the right
  side of the screen), the bit in the X MOST SIGNIFICANT BIT POSITION

        0 ($00)  24 ($18)                     296 ($128)    344 ($158)
                                                       |    |
              |  |
              |  |                                     +----+ 8 ($08)
              |                                        |    |
     29 ($1D) |  +--+                                  |    |
              |  |  |                                  |    |
                 |  |                                  |    |
     50 ($32) +--+-------------------------------------+----+----+ 50 ($32)
              |  |  |                                  |    |    |
              |  |  |                                  |    |    |
              +--+--+                                  |    |    |
                 |                                     |    |    |
                 |                                     +----+----+
                 |                                          |
                 |           VISIBLE VIEWING AREA           |
                 |                                          |
                 |                                          |
                 |                                          |
                 |                                          |
                 |                                          |
                 |                                          |
                 |                                          |
                 |               NTSC*                      |
                 |               40 COLUMNS                 |
                 |               25 ROWS                    |
  208 ($D0) +----+----+                                     |
            |    |    |                                     |
            |    |    |                                  +--+--+ 299 ($E5)
            |    |    |                                  |  |  |
            |    |    |                                  |  |  |
  250 ($FA) +----+----+----------------------------------+--+--+ 250 ($FA)
                 |    |                                  |  |
            |    |    |                                  |  |
            |    |    |                                  +--+
            |    |    |
                 +----+                                  |  |
    488 ($1E8)
                 |                              320 ($140)  344 ($158)
                 24 ($18)

    *North American television transmission standards for your home TV.

        7 ($07)  31 ($1F)                     287 ($11F)    335 ($14F)
                                                       |    |
              |  |
              |  |                                     +----+ 12 ($0C)
              |                                        |    |
     33 ($21) |  +--+                                  |    |
              |  |  |                                  |    |
                 |  |                                  |    |
     54 ($36) +--+-------------------------------------+----+----+ 54 ($36)
              |  |  |                                  |    |    |
              |  |  |                                  |    |    |
              +--+--+                                  |    |    |
                 |                                     |    |    |
                 |                                     +----+----+
                 |                                          |
                 |           VISIBLE VIEWING AREA           |
                 |                                          |
                 |                                          |
                 |                                          |
                 |                                          |
                 |                                          |
                 |                                          |
                 |                                          |
                 |               NTSC*                      |
                 |               38 COLUMNS                 |
                 |               24 ROWS                    |
  204 ($CC) +----+----+                                     |
            |    |    |                                     |
            |    |    |                                  +--+--+ 225 ($E1)
            |    |    |                                  |  |  |
            |    |    |                                  |  |  |
  246 ($F6) +----+----+----------------------------------+--+--+ 246 ($F6)
                 |    |                                  |  |
            |    |    |                                  |  |
            |    |    |                                  +--+
            |    |    |
                 +----+                                  |  |
    480 ($1E0)
                 |                              311 ($137)  335 ($14F)
                 31 ($1F)

    *North American television transmission standards for your home TV.

  register must be set to a 1 (turned ON). If the X position of a sprite is
  less than 256 (on the left side of the screen), then the X MSB of that
  sprite must be 0 (turned OFF). Bits 0 to 7 of the X MSB register
  correspond to sprites 0 to 7, respectively.
    The following program moves a sprite across the screen:

  EXAMPLE:

  10 print"{clear}"
  20 poke2040,13
  30 fori=0to62:poke832+i,129:next
  40 v=53248
  50 pokev+21,1
  60 pokev+39,1
  70 pokev+1,100
  80 forj=0to347
  90 hx=int(j/256):lx=j-256*hx
  100 pokev,lx:pokev+16,hx:next

    When moving expanded sprites onto the left side of the screen in the
  X direction, you have to start the sprite OFF SCREEN on the RIGHT SIDE.
  This is because an expanded sprite is larger than the amount of space
  available on the left side of the screen.

  EXAMPLE:

  10 print"{clear}"
  20 poke2040,13
  30 fori=0to62:poke832+i,129:next
  40 v=53248
  50 pokev+21,1
  60 pokev+39,1:pokev+23,1:pokev+29,1
  70 pokev+1,100
  80 j=488
  90 hx=int(j/256):lx=j-256*hx
  100 pokev,lx:pokev+16,hx
  110 j=j+1:ifj>511thenj=0
  120 ifj>488orj<348goto90

  The charts in Figure 3-3 explain sprite positioning.
    By using these values, you can position each sprite anywhere. By moving
  the sprite a single dot position at a time, very smooth movement is easy
  to achieve.

  SPRITE POSITIONING SUMMARY

    Unexpanded sprites are at least partially visible in the 40 column, by
  25 row mode within the following parameters:

                            1 < X < 343

                           30 < Y < 249

  In the 38 column mode, the X parameters change to she following:

                           8 <= X <= 334

  In the 24 row mode, the Y parameters change to the following:

                          34 <= Y <= 245

    Expanded sprites are at least partially visible in the 40 column, by 25
  row mode within the following parameters:

                         489 >= X <= 343
                           9 >= Y <= 249

  In the 38 column mode, the X parameters change to the following:

                         496 >= X <= 334

  In the 24 row mode, the Y parameters change to the following:

                          13 <= Y <= 245

  SPRITE DISPLAY PRIORITIES

    Sprites have the ability to cross each other's paths, as well as cross
  in front of, or behind other objects on the screen. This can give you a
  truly three dimensional effect for games.
    Sprite to sprite priority is fixed. That means that sprite 0 has the
  highest priority, sprite 1 has the next priority, and so on, until we get
  to sprite 7, which has the lowest priority. In other words, if sprite 1
  and sprite 6 are positioned so that they cross each other, sprite 1 will
  be in front of sprite 6.
    So when you're planning which sprites will appear to be in the fore-
  ground of the picture, they must be assigned lower sprite numbers than
  those sprites you want to put towards the back of the scene. Those
  sprites will be given higher sprite numbers,

  +-----------------------------------------------------------------------+
  | NOTE: A "window" effect is possible. If a sprite with higher priority |
  | has "holes" in it (areas where the dots are not set to 1 and thus     |
  | turned ON), the sprite with the lower priority will show through. This|
  | also happens with sprite and background data.                         |
  +-----------------------------------------------------------------------+

    Sprite to background priority is controllable by the SPRITE-BACK-
  GROUND priority register located at 53275 ($D01B). Each sprite has a bit
  in this register. If that bit is 0, that sprite has a higher priority
  than the background on the screen. In other words, the sprite appears in
  front of background data. If that bit is a 1, that sprite has a lower
  priority than the background. Then the sprite appears behind the back-
  ground data.

  COLLISION DETECTS

    One of the more interesting aspects of the VIC-II chip is its collision
  detection abilities. Collisions can be detected between sprites, or be-
  tween sprites and background data. A collision occurs when a non-zero
  part of a sprite overlaps a non-zero portion of another sprite or char-
  acters on the screen.

  SPRITE TO SPRITE COLLISIONS

    Sprite to sprite collisions are recognized by the computer, or flagged,
  in the sprite to sprite collision register at location 53278 ($D01E in
  HEX) in the VIC-II chip control register. Each sprite has a bit in this
  register. If that bit is a 1, then that sprite is involved in a
  collision. The bits in this register will remain set until read (PEEKed).
  Once read, the register is automatically cleared, so it is a good idea to
  save the value in a variable until you are finished with it.

  +-----------------------------------------------------------------------+
  | NOTE: Collisions can take place even when the sprites are off screen. |
  +-----------------------------------------------------------------------+

  SPRITE TO DATA COLLISIONS

    Sprite to data collisions are detected in the sprite to data collision
  register at location 53279 ($D01F in HEX) of the VIC-II chip control
  register.
    Each sprite has a bit in this register. If that bit is a 1 , then that
  sprite is involved in a collision. The bits in this register remain set
  until read (PEEKed). Once read, the register is automatically cleared, so
  it is a good idea to save the value in a variable until you are finished
  with it.

  +-----------------------------------------------------------------------+
  | NOTE: MULTI-COLOR data 01 is considered transparent for collisions,   |
  | even though it shows up on the screen. When setting up a background   |
  | screen, it is a good idea to make everything that should not cause a  |
  | collision 01 in multi-color mode.                                     |
  +-----------------------------------------------------------------------+

  10 rem sprite example 1... the hot air balloon
  30 vic=13*4096:rem this is where the vic registers begin
  35 pokevic+21,1:rem enable sprite 0
  36 pokevic+33,14:rem set background color to light blue
  37 pokevic+23,1:rem expand sprite 0 in y
  38 pokevic+29,1:rem expand sprite 0 in x
  40 poke2040,192:rem set sprite 0's pointer
  180 pokevic+0,100:rem set sprite 0's x position
  190 pokevic+1,100:rem set sprite 0's y position
  220 pokevic+39,1:rem set sprite 0's color
  250 fory=0to63:rem byte counter with sprite loop
  300 reada:rem read in a byte
  310 poke192*64+y,a:rem store the data in sprite area
  320 nexty:rem close loop
  330 dx=1:dy=1
  340 x=peek(vic):rem look at sprite 0's x position
  350 y=peek(vic+1):rem look at sprite 0's y position
  360 ify=50ory=208thendy=-dy:rem if y is on the edge of the...
  370 rem screen, then reverse delta y
  380 ifx=24and(peek(vic+16)and1)=0thendx=-dx:rem if sprite is touching...
  390 rem the left edge(x=24 and the msb for sprite 0 is 0), reverse it
  400 ifx=40and(peek(vic+16)and1)=1thendx=-dx:rem if sprite is touching...
  410 rem the right edge (x=40 and the msb for sprite 0 is 1), reverse it
  420 ifx=255anddx=1thenx=-1:side=1
  430 rem switch to other side of the screen
  440 ifx=0anddx=-1thenx=256:side=0
  450 rem switch to other side of the screen
  460 x=x+dx:rem add delta x to x
  470 x=xand255:rem make sure x is in allowed range
  480 y=y+dy:rem add delta y to y
  485 pokevic+16,side
  490 pokevic,x:rem put new x value into sprite 0's x position
  510 pokevic+1,y:rem put new y value into sprite 0's y position
  530 goto340
  600 rem ***** sprite data *****
  610 data0,127,0,1,255,192,3,255,224,3,231,224
  620 data7,217,240,7,223,240,7,217,240,3,231,224
  630 data3,255,224,3,255,224,2,255,160,1,127,64
  640 data1,62,64,0,156,128,0,156,128,0,73,0,0,73,0
  650 data0,62,0,0,62,0,0,62,0,0,28,0,0

  10 rem sprite example 2...
  20 rem the hot air balloon again
  30 vic=13*4096:rem this is where the vic registers begin
  35 pokevic+21,63:rem enable sprites 0 thru 5
  36 pokevic+33,14:rem set background color to light blue
  37 pokevic+23,3:rem expand sprites 0 and 1 in y
  38 pokevic+29,3:rem expand sprites 0 and 1 in x
  40 poke2040,192:rem set sprite 0's pointer
  50 poke2041,193:rem set sprite 1's pointer
  60 poke2042,192:rem set sprite 2's pointer
  70 poke2043,193:rem set sprite 3's pointer
  80 poke2044,192:rem set sprite 4's pointer
  90 poke2045,193:rem set sprite 5's pointer
  100 pokevic+4,30:rem set sprite 2's x position
  110 pokevic+5,58:rem set sprite 2's y position
  120 pokevic+6,65:rem set sprite 3's x position
  130 pokevic+7,58:rem set sprite 3's y position
  140 pokevic+8,100:rem set sprite 4's x position
  150 pokevic+9,58:rem set sprite 4's y position
  160 pokevic+10,100:rem set sprite 5's x position
  170 pokevic+11,58:rem set sprite 5's y position
  175 print"{white}{clear}"tab(15)"this is two hires sprites";
  176 printtab(55)"on top of each other"
  180 pokevic+0,100:rem set sprite 0's x position
  190 pokevic+1,100:rem set sprite 0's y position
  200 pokevic+2,100:rem set sprite 1's x position
  210 pokevic+3,100:rem set sprite 1's y position
  220 pokevic+39,1:rem set sprite 0's color
  230 pokevic+41,1:rem set sprite 2's color
  240 pokevic+43,1:rem set sprite 4's color
  250 pokevic+40,6:rem set sprite 1's color
  260 pokevic+42,6:rem set sprite 3's color
  270 pokevic+44,6:rem set sprite 5's color
  280 forx=192to193:rem the start of the loop that defines the sprites
  290 fory=0to63:rem byte counter with sprite loop
  300 reada:rem read in a byte
  310 pokex*64+y,a:rem store the data in sprite area
  320 nexty,x:rem close loops
  330 dx=1:dy=1
  340 x=peek(vic):rem look at sprite 0's x position
  350 ify=50ory=208thendy=-dy:rem if y is on the edge of the...

  370 rem screen, then reverse delta y
  380 ifx=24and(peek(vic+16)and1)=0thendx=-dx:rem if sprite is...
  390 rem touching the left edge, then reverse it
  400 ifx=40and(peek(vic+16)and1)=1thendx=-dx:rem if sprite is...
  410 rem touching the right edge, then reverse it
  420 ifx=255anddx=1thenx=-1:side=3
  430 rem switch to other side of the screen
  440 ifx=0anddx=-1thenx=256:side=0
  450 rem switch to other side of the screen
  460 x=x+dx:rem add delta x to x
  470 x=xand255:rem make sure x is in allowed range
  480 y=y+dy:rem add delta y to y
  485 pokevic+16,side
  490 pokevic,x:rem put new x value into sprite 0's x position
  500 pokevic+2,x:rem put new x value into sprite 1's x position
  510 pokevic+1,y:rem put new y value into sprite 0's y position
  520 pokevic+3,y:rem put new y value into sprite 1's y position
  530 goto340
  600 rem ***** sprite data *****
  610 data0,255,0,3,153,192,7,24,224,7,56,224,14,126,112,14,126,112,14,126
  620 data112,6,126,96,7,56,224,7,56,224,1,56,128,0,153,0,0,90,0,0,56,0
  630 data0,56,0,0,0,0,0,0,0,0,126,0,0,42,0,0,84,0,0,40,0,0
  640 data0,0,0,0,102,0,0,231,0,0,195,0,1,129,128,1,129,128,1,129,128
  650 data1,129,128,0,195,0,0,195,0,4,195,32,2,102,64,2,36,64,1,0,128
  660 data1,0,128,0,153,0,0,153,0,0,0,0,0,84,0,0,42,0,0,20,0,0

  10 rem sprite example 3...
  20 rem the hot air gorf
  30 vic=53248:rem this is where the vic registers begin
  35 pokevic+21,1:rem enable sprite 0
  36 pokevic+33,14:rem set background color to light blue
  37 pokevic+23,1:rem expand sprite 0 in y
  38 pokevic+29,1:rem expand sprite 0 in x

  40 poke2040,192:rem set sprite 0's pointer
  50 pokevic+28,1:rem turn on multicolor
  60 pokevic+37,7:rem set multicolor 0
  70 pokevic+38,4:rem set multicolor 1
  180 pokevic+0,100:rem set sprite 0's x position
  190 pokevic+1,100:rem set sprite 0's y position
  220 pokevic+39,2:rem set sprite 0's color
  290 fory=0to63:rem byte counter with sprite loop
  300 reada:rem read in a byte
  310 poke12288+y,a:rem store the data in sprite area
  320 next y:rem close loop
  330 dx=1:dy=1
  340 x=peek(vic):rem look at sprite 0's x position
  350 y=peek(vic+1):rem look at sprite 0's y position
  360 ify=50ory=208then dy=-dy:rem if y is on the edge of the...
  370 rem screen, then reverse delta y
  380 ifx=24and(peek(vic+16)and1)=0thendx=-dx:rem if sprite is...
  390 rem touching the left edge, then reverse it
  400 ifx=40and(peek(vic+16)and1)=1thendx=-dx:rem if sprite is...
  410 rem touching the right edge, then reverse it
  420 ifx=255anddx=1thenx=-1:side=1
  430 rem switch to other side of the screen
  440 ifx=0anddx=-1thenx=256:side=0
  450 rem switch to other side of the screen
  460 x=x+dx:rem add delta x to x
  470 x=xand255:rem make sure that x is in allowed range
  480 y=y+dy:rem add delta y to y
  485 pokevic+16,side
  490 pokevic,x:rem put new x value into sprite 0's x position
  510 pokevic+1,y:rem put new y value into sprite 0's y position
  520 geta$:rem get a key from the keyboard
  521 ifa$="m"thenpokevic+28,1:rem user selected multicolor
  522 ifa$="h"thenpokevic+28,0:rem user selected high resolution
  530 goto340
  600 rem ***** sprite data *****
  610 data64,0,1,16,170,4,6,170,144,10,170,160,42,170,168,41,105,104,169
  620 data235,106,169,235,106,169,235,106,170,170,170,170,170,170,170,170
  630 data170,170,170,170,166,170,154,169,85,106,170,85,170,42,170,168,10
  640 data170,160,1,0,64,1,0,64,5,0,80,0

  OTHER GRAPHICS FEATURES

  SCREEN BLANKING

    Bit 4 of the VIC-II control register controls the screen blanking func-
  tion. It is found in the control register at location 53265 ($D011). When
  it is turned ON (in other words, set to a 1) the screen is normal. When
  bit 4 is set to 0 (turned OFF), the entire screen changes to border
  color.
    The following POKE blanks the screen. No data is lost, it just isn't
  displayed.

    POKE 53265,PEEK(53265)AND 239

  To bring back the screen. use the POKE shown below:

    POKE 53265,PEEK(53265)OR 16
  +-----------------------------------------------------------------------+
  | NOTE: Turning off the screen will speed up the processor slightly.    |
  | This means that program RUNning is also sped up.                     |
  +-----------------------------------------------------------------------+

  RASTER REGISTER

    The raster register is found in the VIC-II chip at location 53266
  ($D012). The raster register is a dual purpose register. When you read
  this register it returns the lower 8 bits of the current raster position.
  The raster position of the most significant bit is in register location
  53265 ($D011). You use the raster register to set up timing changes in
  your display so that you can get rid of screen flicker. The changes on
  your screen should be mode when the raster is not in the visible display
  area, which is when your dot positions fall between 51 and 251.
    When the raster register is written to (including the MSB) the number
  written to is saved for use with the raster compare function. When the
  actual raster value becomes the same as the number written to the raster
  register, a bit in the VIC-II chip interrupt register 53273 ($D019) is
  turned ON by setting it to 1.

  +-----------------------------------------------------------------------+
  | NOTE: If the proper interrupt bit is enabled (turned on), an interrupt|
  | (IRQ) will occur.                                                     |
  +-----------------------------------------------------------------------+

  INTERRUPT STATUS REGISTER

    The interrupt status register shows the current status of any interrupt
  source. The current status of bit 2 of the interrupt register will be a 1
  when two sprites hit each other. The same is true, in a corresponding 1
  to 1 relationship, for bits 0-3 listed in the chart below. Bit 7 is also
  set with a 1, whenever an interrupt occurs.
    The interrupt status register is located at 53273 ($D019) and is as
  follows:

    LATCH  BIT#             DESCRIPTION
  -------------------------------------------------------------------------
    IRST    0   Set when current raster count = stored raster count
    IMDC    1   Set by SPRITE-DATA collision (1st one only, until reset)
    IMMC    2   Set by SPRITE-SPRITE collision (1st one only, until reset)
     ILP    3   Set by negative transition of light pen (1 per frame)
     IRQ    7   Set by latch set and enabled
  -------------------------------------------------------------------------
    Once an interrupt bit has been set, it's "latched" in and must be
  cleared by writing a 1 to that bit in the interrupt register when you're
  ready to handle it. This allows selective interrupt handling, without
  having to store the other interrupt bits.
    The INTERRUPT ENABLE REGISTER is located at 53274 ($D01A). It has the
  same format as the interrupt status register. Unless the corresponding
  bit in the interrupt enable register is set to a 1, no interrupt from
  that source will take place. The interrupt status register can still be
  polled for information, but no interrupts will be generated.
    To enable an interrupt request the corresponding interrupt enable bit
  (as shown in the chart above) must be set to a 1.
    This powerful interrupt structure lets you use split screen modes. For
  instance you can have half of the screen bit mapped, half text, more than
  8 sprites at a time, etc. The secret is to use interrupts properly. For
  example, if you want the top half of the screen to be bit mapped and the
  bottom to be text, just set the raster compare register (as explained
  previously) for halfway down the screen. When the interrupt occurs, tell
  the VIC-II chip to get characters from ROM, then set the raster compare
  register to interrupt at the top of the screen. When the interrupt occurs
  at the top of the screen, tell the VIC-II chip to get characters from RAM
  (bit map mode).
    You can also display more than 8 sprites in the same way. Unfortunately
  BASIC isn't fast enough to do this very well. So if you want to start
  using display interrupts, you should work in machine language.

  SUGGESTED SCREEN AND CHARACTER COLOR COMBINATIONS

    Color TV sets are limited in their ability to place certain colors next
  to each other on the same line. Certain combinations of screen and char-
  acter colors produce blurred images. This chart shows which color com-
  binations to avoid, and which work especially well together.

                          CHARACTER COLOR
            0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
          +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
         0| x| o| x| o| o| /| x| o| o| x| o| o| o| o| o| o|
          +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
         1| o| x| o| x| o| o| o| x| /| o| /| o| o| x| o| o|
          +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
         2| x| o| x| x| /| x| x| o| o| x| o| x| x| x| x| /|
          +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
         3| o| x| x| x| x| /| o| x| x| x| x| /| x| x| /| x|
          +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
         4| o| /| x| x| x| x| x| x| x| x| x| x| x| x| x| /|
          +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
         5| o| /| x| /| x| x| x| x| x| x| x| /| x| o| x| /|
          +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
  SCREEN 6| /| o| x| o| x| x| x| x| x| x| x| x| x| /| o| o|
  COLOR   +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
         7| o| x| o| x| x| x| /| x| /| o| /| o| o| x| x| x|
          +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
         8| /| o| o| x| x| x| x| o| x| o| x| x| x| x| x| /|
          +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
         9| x| o| x| x| x| x| x| o| o| x| o| x| x| x| x| o|
          +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        10| /| /| o| x| x| x| x| /| x| o| x| x| x| x| x| /|   o = EXCELLENT
          +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        11| o| o| x| /| x| x| x| o| x| x| x| x| o| o| /| o|   / = FAIR
          +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        12| o| o| /| x| x| x| /| x| x| /| x| o| x| x| x| o|   x = POOR
          +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        13| o| x| x| x| x| o| /| x| x| x| x| o| x| x| x| x|
          +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        14| o| o| x| o| x| x| o| x| x| x| x| /| x| x| x| /|
          +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        15| o| o| o| x| /| /| o| x| x| /| /| o| o| x| /| x|
          +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

  PROGRAMMING SPRITES - ANOTHER LOOK

    For those of you having trouble with graphics, this section has been
  designed as a more elementary tutorial approach to sprites.

  MAKING SPRITES IN BASIC - A SHORT PROGRAM

    There are at least three different BASIC programming techniques which
  let you create graphic images and cartoon animations on the Commodore 64.
  You can use the computer's built-in graphics character set (see Page
  376). You can program your own characters (see Page 108) or... best of
  all... you can use the computer's built-in "sprite graphics. To
  illustrate how easy it is, here's one of the shortest spritemaking
  programs you can write in BASIC:

  10 print"{clear}"
  20 poke2040,13
  30 fors=832to832+62:pokes,255:next
  40 v=53248
  50 pokev+21,1
  60 pokev+39,1
  70 pokev,24
  80 pokev+1,100

    This program includes the key "ingredients" you need to create any
  sprite. The POKE numbers come from the SPRITEMAKING CHART on Page 176.
  This program defines the first sprite... sprite 0... as a solid white
  square on the screen. Here's a line-by-line explanation of the program:

    LINE 10 clears the screen.

    LINE 20 sets the "sprite pointer" to where the Commodore 64 will read
  its sprite data from. Sprite 0 is set at 2040, sprite 1 at 2041, sprite
  2 at 2042, and so on up to sprite 7 at 2047. You can set all 8 sprite
  pointers to 13 by using this line in place of line 20:

    20 FOR SP=2040TO2047:POKE SP,13:NEXT SP

    LINE 30 puts the first sprite (sprite 0) into 63 bytes of the Commodore
  64's RAM memory starting at location 832 (each sprite requires 63 bytes

  of memory). The first sprite (sprite 0) is "addressed" at memory
  locations 832 to 894.

    LINE 40 sets the variable "V" equal to 53248, the starting address of
  the VIDEO CHIP. This entry lets us use the form (V+number) for sprite
  settings. 're using the form (V+number) when POKEing sprite settings
  because this format conserves memory and lets us work with smaller
  numbers. For example, in line 50 we typed POKE V+21. This is the same as
  typing POKE 53248+21 or POKE 53269... but V+21 requires less space than
  53269, and is easier to remember.

    LINE 50 enables or "turns on" sprite 0. There are 8 sprites, numbered
  from 0 to 7. To turn on an individual sprite, or a combination of
  sprites, all you have to do is POKE V+21 followed by a number from 0
  (turn all sprites off) to 255 (turn all 8 sprites on). You can turn on
  one or more sprites by POKEing the following numbers:
  +------+------+------+------+------+------+------+------+------+-------+
  |ALL ON|SPRT 0|SPRT 1|SPRT 2|SPRT 3|SPRT 4|SPRT 5|SPRT 6|SPRT 7|ALL OFF|
  |  255 |   1  |   2  |   4  |   8  |  16  |  32  |  64  |  128 |   0   |
  +------+------+------+------+------+------+------+------+------+-------+

    POKE V+21,1 turns on sprite 0. POKE V+21,128 turns on sprite 7. You
  can also turn on combinations of sprites. For example, POKE V+21,129
  turns on both sprite 0 and sprite 7 by adding the two "turn on" numbers
  (1+128) together. (See SPRITEMAKING CHART, Page 176.)

    LINE 60 sets the COLOR of sprite 0. There are 16 possible sprite
  colors, numbered from 0 (black) to 15 (grey). Each sprite requires a
  different POKE to set its color, from V+39 to V+46. POKE V+39,1 colors
  sprite 0 white. POKE V+46,15 colors sprite 7 grey. (See the SPRITEMAKING
  CHART for more information.)
    When you create a sprite, as you just did, the sprite will STAY IN
  MEMORY until you POKE it off, redefine it, or turn off your computer.
  This lets you change the color, position and even shape of the sprite in
  DIRECT or IMMEDIATE mode, which is useful for editing purposes. As an
  example, RUN the program above, then type this line in DIRECT mode
  (without a line number) and hit the <RETURN> key:

    POKE V+39,8

    The sprite on the screen is now ORANGE. Try POKEing some other numbers
  from 0 to 15 to see the other sprite colors. Because you did this in

  DIRECT mode, if you RUN your program the sprite will return to its origi-
  nal color (white).

    LINE 70, determines the HORIZONTAL or "X" POSITION of the sprite on the
  screen. This number represents the location of the UPPER LEFT CORNER of
  the sprite. The farthest left horizontal (X) position which you can see
  on your television screen is position number 24, although you can move
  the sprite OFF THE SCREEN to position number 0.

    LINE 80 determines the VERTICAL or "Y" POSITION of the sprite. In this
  program, we placed the sprite at X (horizontal) position 24, and Y
  (vertical) position 100. To try another location, type this POKE in
  DIRECT mode and hit <RETURN>:

    POKE V,24:POKE V+1,50

    This places the sprite at the upper left corner of the screen. To move
  the sprite to the lower left corner, type this:

    POKE V,24:POKE V+1,229

    Each number from 832 to 895 in our sprite 0 address represents one
  block of 8 pixels, with three 8-pixel blocks in each horizontal row of
  the sprite. The loop in line 80 tells the computer to POKE 832,255 which
  makes the first 8 pixels solid . . . then POKE 833,255 to make the second
  8 pixels solid, and so on to location 894 which is the last group of 8
  pixels in the bottom right corner of the sprite. To better see how this
  works, try typing the following in DIRECT r-node, and notice that the
  second group of 8 pixels is erased:

    POKE 833,0 (to put it back type POKE 833,255 or RUN your program)

    The following line, which you can add to your program. erases the
  blocks in the MIDDLE of the sprite you created:

    90 FOR A=836 TO 891 STEP 3:POKE A,O:NEXT A

    Remember, the pixels that make up the sprite are grouped in blocks of
  eight. This line erases the 5th group of eight pixels (block 836) and
  every third block up to block 890. Try POKEing any of the other numbers
  from 832 to 894 with either a 255 to make them solid or 0 to make them
  blank.

  +-----------------------------------------------------------------------+
  | CRUNCHING YOUR SPRITE PROGRAMS                                        |
  |                                                                       |
  | Here's a helpful "crunching" tip: The program described above is      |
  | already short, but it can be made even shorter by "crunching" it      |
  | smaller. In our example we list the key sprite settings on separate   |
  | program lines so you can see what's happening in the program. In      |
  | actual practice, a good programmer would probably write this program  |
  | as a TWO LINE PROGRAM... by "crunching" it as follows:                |
  |                                                                       |
  | 10 PRINTCHR$(147):V=53248:POKEV+21,1:POKE2040.13:POKEV+39,1           |
  | 20 FORS=832TO894:POKES,255:NEXT:POKEV,24:POKEV+1,100                  |
  |                                                                       |
  | For more tips on how to crunch your programs so they fit in less      |
  | memory and run more efficiently, see the "crunching guide" on Page 24.|
  +-----------------------------------------------------------------------+

                                  TV SCREEN
            +---------------------------------------------------+
            |        ^                                          |
            |        |                                          |
            |<-------+---- X POSITION = HORIZONTAL ------------>|
            |        |                                          |
            |        |                                          |
            |        |                                          |
            |        |                                          |
            |        |                                          |
            |        |                          +-+             |
            |        |                          | |             |
            |        |                          +-+             |
            |        |                          /               |
            |        |                         /                |
            |        |                        /                 |
            |        |                       /                  |
            +-------------------------------/-------------------+
                                           /
    A sprite located here must have both its X-position (horizontal) and
    Y-position (vertical) set so it can be displayed on the screen.

  Figure 3-4. The display screen is divided into a grid of X and Y coor-
  dinates.

  POSITIONING SPRITES ON THE SCREEN

    The entire display screen is divided into a grid of X and Y coordi-
  nates, like a graph. The X COORDINATE is the HORIZONTAL position across
  the screen and the Y COORDINATE is the VERTICAL position up and down (see
  Figure 3-4).
    To position any sprite on the screen, you must POKE TWO SETTINGS...
  the X position and the Y position... these tell the computer where to
  display the UPPER LEFT HAND CORNER of the sprite. Remember that a sprite
  consists of 504 individual pixels, 24 across by 21 down... so if you POKE
  a sprite onto the upper left corner of your screen, the sprite will be
  displayed as a graphic image 24 pixels ACROSS and 21 pixels DOWN starting
  at the X-Y position you defined. The sprite will be displayed based on
  the upper left corner of the entire sprite, even if you define the sprite
  using only a small part of the 24X21-pixel sprite area.
    To understand how X-Y positioning works, study the following diagram
  (Figure 3-5), which shows the X and Y numbers in relation to your display
  screen. Note that the GREY AREA in the diagram shows your television
  viewing area... the white area represents positions which are OFF your
  viewing screen...

                         [THE PICTURE IS MISSING!]

    To display a sprite in a given location, You must POKE the X and Y
  settings for each SPRITE... remembering that every sprite has its own
  unique X POKE and Y POKE. The X and Y settings for ail 8 sprites are
  shown here:

  POKE THESE VALUES TO SET X-Y SPRITE POSITIONS

  +------+-------+-------+-------+-------+-------+-------+-------+--------+
  |      |SPRT 0 |SPRT 1 |SPRT 2 |SPRT 3 |SPRT 4 |SPRT 5 |SPRT 6 |SPRT 7  |
  +------+-------+-------+-------+-------+-------+-------+-------+--------+
  |SET X |V,X    |V+2,X  |V+4,X  |V+6,X  |V+8,X  |V+10,X |V+12,X |V+14,X  |
  |SET Y |V+1,Y  |V+3,Y  |V+5,Y  |V+7,Y  |V+9,Y  |V+11,Y |V+13,Y |V+15,Y  |
  |RIGHTX|V+16,1 |V+16,2 |V+16,4 |V+16,8 |V+16,16|V+16,32|V+16,64|V+16,128|
  +------+-------+-------+-------+-------+-------+-------+-------+--------+

    POKEING AN X POSITION: The possible values of X are 0 to 255, counting
  from left to right. Values 0 to 23 place all or part of the sprite OUT OF
  THE VIEWING AREA off the left side of the screen... values 24 to 255
  place the sprite IN THE VIEWING AREA up to the 255th position (see next
  paragraph for settings beyond the 255th X position). To place the sprite
  at one of these positions, just type the X-POSITION POKE for the sprite
  you're using. For example, to POKE sprite I at the farthest left X
  position IN THE VIEWING AREA, type: POKE V+2,24.

    X VALUES BEYOND THE 255TH POSITION: To get beyond the 255th position
  across the screen, you need to make a SECOND POKE using the numbers in
  the "RIGHT X" row of the chart (Figure 3-5). Normally, the horizontal (X)
  numbering would continue past the 255th position to 256, 257, etc., but
  because registers only contain 8 bits we must use a "second register" to
  access the RIGHT SIDE of the screen and start our X numbering over again
  at 0. So to get beyond X position 255, you must POKE V+16 and a number
  (depending on the sprite). This gives you 65 additional X positions
  (renumbered from 0 to 65) in the viewing area on the RIGHT side of the
  viewing screen. (You can actually POKE the right side X value as high as
  255, which takes you off the right edge of the viewing screen.)

    POKEING A Y POSITION: The possible values of Y are 0 to 255, counting
  from top to bottom. Values 0 to 49 place all or part of the sprite OUT
  OF THE VIEWING AREA off the TOP of the screen. Values 50 to 229 place the
  sprite IN THE VIEWING AREA. Values 230 to 255 place all or part of the
  sprite OUT OF THE VIEWING AREA off the BOTTOM of the screen.

    Let's see how this X-Y positioning works, using sprite 1. Type this
  program:
  10 print"{clear}":v=53248:pokev+21,2:poke2041,13
  20 fors=832to895:pokes,255:next:pokev+40,7
  30 pokev+2,24
  40 pokev+3,50

  This simple program establishes sprite 1 as a solid box and positions it
  at the upper left corner of the screen. Now change line 40 to read:

    40 POKE V+3,229

  This moves the sprite to the bottom left corner of the screen. Now let's
  test the RIGHT X LIMIT of the sprite. Change line 30 as shown:

    30 POKE V+2,255

  This moves the sprite to the RIGHT but reaches the RIGHT X LIMIT, which
  is 255. At this point, the "most significant bit" in register 16 must be
  SET. In other words, you must type POKE V+ 16 and the number shown in the
  "RIGHT X" column in the X-Y POKE CHART above to RESTART the X position
  counter at the 256th pixel/position on the screen. Change line 30 as
  follows:

    30 POKE V+16,PEEK(V+16)OR 2:POKE V+2,0

  POKE V+16,2 sets the most significant bit of the X position for sprite 1
  and restarts it at the 256th pixel/position on the screen. POKE V+2,0
  displays the sprite at the NEW POSITION ZERO, which is now reset to the
  256th pixel.
    To get back to the left side of the screen, you must reset the most
  significant bit of the X position counter to 0 by typing (for sprite 1):

    POKE V+16, PEEK(V+16)AND 253

    TO SUMMARIZE how the X positioning works... POKE the X POSITION for any
  sprite with a number from 0 to 255. To access a position beyond the 255th
  position/pixel across the screen, you must use an additional POKE (V+16)
  which sets the most significant bit of the X position and start counting
  from 0 again at the 256th pixel across the screen.

  This POKE starts the X numbering over again from 0 at the 256th position
  (Example: POKE V+16,PEEK(V+16)OR 1 and POKE V,1 must be included to place
  sprite 0 at the 257th pixel across the screen.) To get back to the left
  side X positions you have to TURN OFF the control setting by typing
  POKE V+16,PEEK(V+16)AND 254.

  POSITIONING MULTIPLE SPRITES ON THE SCREEN

    Here's a program which defines THREE DIFFERENT SPRITES (0, 1 and 2) in
  different colors and places them in different positions on the screen:

  10 print"{clear}":v=53248:fors=832to895:pokes,255:next
  20 form=2040to2042:pokem,13:next
  30 pokev+21,7
  40 pokev+39,1:pokev+40,7:pokev+41,8
  50 pokev,24:pokev+1,50
  60 pokev+2,12:pokev+3,229
  70 pokev+4,255:pokev+5,50

    For convenience, all 3 sprites have been defined as solid squares,
  getting their data from the same place. The important lesson here is how
  the 3 sprites are positioned. The white sprite 0 is at the top lefthand
  corner. The yellow sprite 1 is at the bottom lefthand corner but HALF the
  sprite is OFF THE SCREEN (remember, 24 is the leftmost X position in the
  viewing area... an X position less than 24 puts all or part of the sprite
  off the screen and we used an X position 12 here which put the sprite
  halfway off the screen). Finally, the orange sprite 2 is at the RIGHT X
  LIMIT (position 255)... but what if you want to display a sprite in the
  area to the RIGHT of X position 255?

  DISPLAYING A SPRITE BEYOND THE 255TH X-POSITION

    Displaying a sprite beyond the 255th X position requires a special POKE
  which SETS the most significant bit of the X position and starts over at
  the 256th pixel position across the screen. Here's how it works...
    First, you POKE V+16 with the number for the sprite you're using (check
  the "RIGHT X" row in the X-Y chart... we'll use sprite 0). Now we assign
  an X position, keeping in mind that the X counter starts over from 0 at
  the 256th position on the screen. Change line 50 to read as follows:
    50 POKE V+16,1:POKE V,24:POKE V+1,75

  This line POKEs V+ 16 with the number required to "open up" the right
  side of the screen... the new X position 24 for sprite 0 now begins 24
  pixels to the RIGHT of position 255. To check the right edge of the
  screen, change line 60 to:

    60 POKE V+16,1:POKE V,65:POKE V+1,75

    Some experimentation with the settings in the sprite chart will give
  you the settings you need to position and move sprites on the left and
  right sides of the screen. The section on "moving sprites" will also
  increase your understanding of how sprite positioning works.

  SPRITE PRIORITIES

    You can actually make different sprites seem to move IN FRONT OF or
  BEHIND each other on the screen. This incredible three dimensional illu-
  sion is achieved by the built-in SPRITE PRIORITIES which determine which
  sprites have priority over the others when 2 or more sprites OVERLAP on
  the screen.
    The rule is "first come, first served" which means lower-numbered
  sprites AUTOMATICALLY have priority over higher-numbered sprites. For
  example, if you display sprite 0 and sprite 1 so they overlap on the
  screen, sprite 0 will appear to be IN FRONT OF sprite 1. Actually, sprite
  0 always supersedes all the other sprites because it's the lowest num-
  bered sprite. In comparison, sprite 1 has priority over sprites 2-7;
  sprite 2 has priority over sprites 3-7, etc. Sprite 7 (the last sprite)
  has LESS PRIORITY than any of the other sprites, and will always appear
  to be displayed "BEHIND" any other sprites which overlap its position.
    To illustrate how priorities work, change lines 50, 60, and 70 in the
  program above to the following:

  50 POKEV,24:POKEV+1,50:POKEV+16,0
  60 POKEV+2,34:POKEV+3,60
  70 POKEV+4,44:POKEV+5,70

  You should see a white sprite on top of a yellow sprite on top of an
  orange sprite. Of course, now that you see how priorities work, you can
  also MOVE SPRITES and take advantage of these priorities in your ani-
  mation.

  DRAWING A SPRITE

    Drawing a Commodore sprite is like coloring the empty spaces in a
  coloring book. Every sprite consists of tiny dots called pixels. To draw
  a sprite, all you have to do is "color in" some of the pixels.
    Look at the spritemaking grid in Figure 3-6. This is what a blank
  sprite looks like:

                        [THE PICTURE IS MISSING!]

                      Figure 3-6. Spritemaking grid.

  Each little "square" represents one pixel in the sprite. There are 24
  pixels across and 21 pixels up and down, or 504 pixels in the entire
  sprite. To make the sprite look like something, you have to color in
  these pixels using a special PROGRAM... but how can you control over 500
  individual pixels? That's where computer programming can help you. In-
  stead of typing 504 separate numbers, you only have to type 63 numbers
  for each sprite. Here's how it works...

  CREATING A SPRITE... STEP BY STEP

    To make this as easy as possible for you, we've put together this
  simple step by step guide to help you draw your own sprites.

  STEP 1:

  Write the spritemaking program shown here ON A PIECE OF PAPER... note
  that line 100 starts a special DATA section of your program which will
  contain the 63 numbers you need to create your sprite.

                        [THE PICTURE IS MISSING!]

  STEP 2:

  Color in the pixels on the spritemaking grid on Page 162 (or use a piece
  of graph paper... remember, a sprite has 24 squares across and 21 squares
  down). We suggest you use a pencil and draw lightly so you can reuse this
  grid. You can create any image you like, but for our example we'll draw
  a simple box.

  STEP 3:

  Look at the first EIGHT pixels. Each column of pixels has a number (128,
  64, 32, 16, 8, 4, 2, 1). The special type of addition we are going to
  show you is a type of BINARY ARITHMETIC which is used by most computers

  as a special way of counting. Here's a close-up view of the first eight
  pixels in the top left hand corner of the sprite:

       |128| 64| 32| 16|  8|  4|  2|  1|
       +---+---+---+---+---+---+---+---+
       |@@@|@@@|@@@|@@@|@@@|@@@|@@@|@@@|
       |@@@|@@@|@@@|@@@|@@@|@@@|@@@|@@@|
       +---+---+---+---+---+---+---+---+
  STEP 4:

  Add up the numbers of the SOLID pixels. This first group of eight pixels
  is completely solid, so the total number is 255.

  STEP 5:

  Enter that number as the FIRST DATA STATEMENT in line 100 of the
  Spritemaking Program below. Enter 255 for the second and third groups
  of eight.

  STEP 6:

  Look at the FIRST EIGHT PIXELS IN THE SECOND ROW of the sprite. Add up
  the values of the solid pixels. Since only one of these pixels is solid,
  the total value is 128. Enter this as the first DATA number in line 101.

       |128| 64| 32| 16|  8|  4|  2|  1|
       +---+---+---+---+---+---+---+---+
       |@@@|   |   |   |   |   |   |   |
       |@@@|   |   |   |   |   |   |   |
       +---+---+---+---+---+---+---+---+
  STEP 7:

  Add up the values of the next group of eight pixels (which is 0 because
  they're all BLANK) and enter in line 101. Now move to the next group of
  pixels and repeat the process for each GROUP OF EIGHT PIXELS (there are
  3 groups across each row, and 21 rows). This will give you a total of 63
  numbers. Each number represents ONE group of 8 pixels, and 63 groups of
  eight equals 504 total individual pixels. Perhaps a better way of looking
  at the program is like this... each line in the program represents ONE
  ROW in the sprite. Each of the 3 numbers in each row represents ONE GROUP
  OF EIGHT PIXELS. And each number tells the computer which pixels to make
  SOLID and which pixels to leave blank.

  STEP 8:

  CRUNCH YOUR PROGRAM INTO A SMALLER SPACE BY RUNNING TOGETHER ALL THE DATA
  STATEMENTS, AS SHOWN IN THE SAMPLE PROGRAM BELOW. Note that we asked you
  to write your sprite program on a piece of paper. We did this for a good
  reason. The DATA STATEMENT LINES 100-120 in the program in STEP 1 are
  only there to help you see which numbers relate to which groups of pixels
  in your sprite. Your final program should be "crunched" like this:

  10 print"{clear}":poke53280,5:poke53281,6
  20 v=53248:pokev+34,3
  30 poke 53269,4:poke2042,13
  40 forn=0to62:readq:poke832+n,q:next
  100 data255,255,255,128,0,1,128,0,1,128,0,1,144,0,1,144,0,1,144,0,1,144,0
  101 data1,144,0,1,144,0,1,144,0,1,144,0,1,144,0,1,144,0,1,128,0,1,128,0,1
  102 data128,0,1,128,0,1,128,0,1,128,0,1,255,255,255
  200 x=200:y=100:poke53252,x:poke53253,y

  MOVING YOUR SPRITE ON THE SCREEN

    Now that you've created your sprite, let's do some interesting things
  with it. To move your sprite smoothly across the screen, add these two
  lines to your program:

    50 POKE V+5,100:FOR X=24TO255:POKE V+4,X:NEXT:POKE V+16,4
    55 FOR X=0TO65:POKE V+4,X:NEXT X:POKE V+16,0:GOTO 50

    LINE 50 POKEs the Y POSITION at 100 (try 50 or 229 instead for
  variety). Then it sets up a FOR... NEXT loop which POKEs the sprite into
  X position 0 to X position 255, in order. When it reaches the 255th
  position, it POKEs the RIGHT X POSITION (POKE V+16,4) which is required
  to cross to the right side of the screen.

    LINE 55 has a FOR... NEXT loop which continues to POKE the sprite in
  the last 65 positions on the screen. Note that the X value was reset to
  zero but because you used the RIGHT X setting (POKE V+16,2) X starts over
  on the right side of the screen.
    This line keeps going back to itself (GOTO 50). If you just want the
  sprite to move ONCE across the screen and disappear, then take out
  GOTO50.

    Here's a line which moves the sprite BACK AND FORTH:

    50 POKE V+5,100:FOR X=24TO255:POKE V+4,X:NEXT:POKE V+16,4:
       FOR X=0TO65: POKE V+4,X: NEXT X
    55 FOR X=65TO0 STEP-1:POKE V+4,X:NEXT:POKE V+16,0: FOR
       X=255TO24 STEP-1: POKE V+4,X:NEXT
    60 GOTO 50

  Do you see how these programs work? This program is the same as the
  previous one, except when it reaches the end of the right side of the
  screen, it REVERSES ITSELF and goes back in the other direction. That is
  what the STEP-1 accomplishes... it tells the program to POKE the sprite
  into X values from 65 to 0 on the right side of the screen, then from 255
  to 0 on the left side of the screen, STEPping backwards minus-1 position
  at a time.

  VERTICAL SCROLLING

    This type of sprite movement is called "scrolling." To scroll your
  sprite up or down in the Y position, you only have to use ONE LINE. ERASE
  LINES 50 and 55 by typing the line numbers by themselves and hitting
  <RETURN> like this:

    50 <RETURN>
    60 <RETURN>

  Now enter LINE 50 again as follows:

    50 POKE V+4,24:FOR Y=0TO255:POKE V+5,Y:NEXT

  THE DANCING MOUSE-A SPRITE PROGRAM EXAMPLE

    Sometimes the techniques described in a programmer's reference manual
  are difficult to understand, so we've put together a fun sprite program
  called "Michael's Dancing Mouse." This program uses three different
  sprites in a cute animation with sound effects-and to help you understand
  how it works we've included an explanation of EACH COMMAND so you can see
  exactly how the program is constructed:

  5 s=54272:pokes+24,15:pokes,220:pokes+1,68:pokes+5,15:pokes+6,215
  10 pokes+7,120:pokes+8,100:pokes+12,15:pokes+13,215
  15 print"{clear}":v=53248:pokev+21,1
  20 fors1=12288to12350:readq1:pokes1,q1:next
  25 fors2=12352to12414:readq2:pokes2,q2:next
  30 fors3=12416to12478:readq3:pokes3,q3:next
  35 pokev+39,15:pokev+1,68
  40 printtab(160)"{white}i am the dancing mouse!{light blue}"
  45 p=192
  50 forx=0to347step3
  55 rx=int(x/256):lx=x-rx*256
  60 pokev,lx:pokev+16,rx
  70 ifp=192thengosub200
  75 ifp=193thengosub300
  80 poke2040,p:fort=1to60:next
  85 p=p+1:ifp>194thenp=192
  90 next
  95 end
  100 data30,0,120,63,0,252,127,129,254,127,129,254,127,189,254,127,255,254
  101 data63,255,252,31,187,248,3,187,192,1,255,128,3,189,192,1,231,128,1,
  102 data255,0,31,255,0,0,124,0,0,254,0,1,199,32,3,131,224,7,1,192,1,192,0
  103 data3,192,0,30,0,120,63,0,252,127,129,254,127,129,254,127,189,254,127
  104 data255,254,63,255,252,31,221,248,3,221,192,1,255,128,3,255,192,1,195
  105 data128,1,231,3,31,255,255,0,124,0,0,254,0,1,199,0,7,1,128,7,0,204,1
  106 data128,124,7,128,5630,0,120,63,0,252,127,129,254,127,129,254,127,189
  107 data254,127,255,25463,255,252,31,221,248,3,221,192,1,255,134,3,189
  108 data204,1,199,152,1,255,48,1,255,224,1,252,0,3,254,0
  109 data7,14,0,204,14,0,248,56,0,112,112,0,0,60,0,-1
  200 pokes+4,129:pokes+4,128:return
  300 pokes+11,129:pokes+11,128:return

  LINE 5:

    S=54272             Sets the variable 5 equal to 54272, which is the
                        beginning memory location of the SOUND CHIP.
                        From now on, instead of poking a direct memory
                        location, we will POKE S plus a value.
    POKES+24,15         Same as POKE 54296,15 which sets VOLUME to
                        highest level.
    POKES,220           Same as POKE 54272,220 which sets Low Fre-
                        quency in Voice 1 for a note which approximates
                        high C in Octave 6.
    POKES+1,68          Same as POKE 54273,68 which sets High Fre-
                        quency in Voice I for a note which approximates
                        high C in Octave 6.
    POKES+5,15          Same as POKE 54277,15 which sets Attack/Decay
                        for Voice 1 and in this case consists of the
                        maximum DECAY level with no attack, which pro-
                        duces the "echo" effect.
    POKES+6,215         Same as POKE 54278,215 which sets Sustain/Re-
                        lease for Voice 1 (215 represents a combination
                        of sustain and release values).
  LINE 10:

    POKES+7,120         Same as POKE 54279,120 which sets the Low Fre-
                        quency for Voice 2.
    POKES+8,100         Same as POKE 54280,100 which sets the High
                        Frequency for Voice 2.
    POKES+12,15         Same as POKE 54284,15 which sets Attack/Decay
                        for Voice 2 to same level as Voice 1 above.
    POKES+13,215        Same as POKE 54285,215 which sets Sustain/Re-
                        lease for Voice 2 to same level as Voice 1 above.

  LINE 15:

    PRINT"<SHIFT+CLR/HOME>" Clears the screen when the program begins.

    V=53248             Defines the variable "V" as the starting location
                        of the VIC chip which controls sprites. From now
                        on we will define sprite locations as V plus a
                        value.

    POKEV+21,1          Turns on (enables) sprite number 1.

  LINE 20:

    FORS1=12288         We are going to use ONE SPRITE (sprite 0) in this
    TO 12350            animation, but we are going to use THREE sets of
                        sprite data to define three separate shapes. To
                        get our animation, we will switch the POINTERS
                        for sprite 0 to the three places in memory where
                        we have stored the data which defines our three
                        different shapes. The same sprite will be rede-
                        fined rapidly over and over again as 3 different
                        shapes to produce the dancing mouse animation.
                        You can define dozens of sprite shapes in DATA
                        STATEMENTS, and rotate those shapes through
                        one or more sprites. So you see, you don't have to
                        limit one sprite to one shape or vice-versa. One
                        sprite can have many different shapes, simply by
                        changing the POINTER SETTING FOR THAT SPRITE to
                        different places in memory where the sprite data
                        for different shapes is stored. This line means we
                        have put the DATA for "sprite shape 1" at memory
                        locations 12288 to 12350.

    READ Q1             Reads 63 numbers in order from the DATA state-
                        ments which begin at line 100. Q1 is an arbitrary
                        variable name. It could just as easily be A, Z1 or
                        another numeric variable.

    POKES1,Q1           Pokes the first number from the DATA statements
                        (the first "Q1" is 30) into the first memory
                        location (the first memory location is 12288). This
                        is the same as POKE12288,30.

    NEXT                This tells the computer to look BETWEEN the FOR and
                        NEXT parts of the loop and perform those in-between
                        commands (READQ1 and POKES1,Q1 using the NEXT
                        numbers in order). In other words, the NEXT
                        statement makes the computer READ the NEXT Q1 from
                        the DATA STATEMENTS, which is 0, and also
                        increments S1 by 1 to the next value, which is
                        12289. The result is POKE12289,0... the NEXT
                        command makes the loop keep going back until the
                        last values in the series, which are POKE 12350,0.

  LINE 25:

    FORS2=12352         The second shape of sprite zero is defined by the
    TO 12414            DATA which is located at locations 12352 to 12414.
                        NOTE that location 12351 is SKIPPED... this is the
                        64th location which is used in the definition of
                        the first sprite group but does not contain any of
                        the sprite data numbers. Just remember when
                        defining sprites in consecutive locations that you
                        will use 64 locations, but only POKE sprite data
                        into the first 63 locations.

    READQ2              Reads the 63 numbers which follow the numbers we
                        used for the first sprite shape. This READ simply
                        looks for the very next number in the DATA area and
                        starts reading 63 numbers, one at a time.

    POKES2,Q2           Pokes the data (Q2) into the memory locations (S2)
                        for our second sprite shape, which begins at
                        location 12352.

    NEXT                Same use as line 20 above.

  LINE 30:

    FORS3=12416         The third shape of sprite zero is defined by the
    TO 12478            DATA to be located at locations 12416 to 12478.
    READQ3              Reads last 63 numbers in order as Q3.
    POKES3,Q3           Pokes those numbers into locations 12416 to 12478.
    NEXT                Same as lines 20 and 25.

  LINE 35:

    POKEV+39,15         Sets color for sprite 0 to light grey.

    POKEV+1,68          Sets the upper right hand corner of the sprite
                        square to vertical (Y) position 68. For the sake of
                        comparison, position 50 is the top lefthand corner
                        Y position on the viewing screen.

  LINE 40:

    PRINTTAB(160)       Tabs 160 spaces from the top lefthand CHARACTER
                        SPACE on the screen, which is the same as 4 rows
                        beneath the clear command... this starts your PRINT
                        message on the 6th line down on the screen.
    "{white}            Hold down the <CTRL> key and press the key marked
                        <WHT> at the same time. If you do this inside
                        quotation marks, a "reversed E" will appear. This
                        sets the color to everything PRINTed from then on
                        to WHITE.
    I AM THE            This is a simple PRINT statement.
    DANCING
    MOUSE!

    {light blue}        This sets the color back to light blue when the
                        PRINT statement ends. Holding down <C=> and <7>
                        a at the same time inside quotation marks
                        causes a "reversed diamond symbol" to appear.

  LINE 45:

    P=192               Sets the variable P equal to 192. This number 192
                        is the pointer you must use, in this case to
                        "point" sprite 0 to the memory locations that begin
                        at location 12288. Changing this pointer to the
                        locations of the other two sprite shapes is the
                        secret of using one sprite to create an animation
                        that is actually three different shapes.

  LINE 50:

    FORX=0TO347         Steps the movement of your sprite 3 X positions at
    STEP3               a time (to provide fast movement) from position 0
                        to position 347.

  LINE 55:

    RX=INT(X/256)       RX is the integer of X/256 which means that RX is
                        rounded off to 0 when X is less than 256, and RX
                        becomes 1 when X reaches position 256. We will
                        use RX in a moment to POKE V+16 with a 0 or 1
                        to turn on the "RIGHT SIDE" of the screen.

    LX=X-RX*256         When the sprite is at X position 0, the formula
                        looks like this: LX = 0 - (0 times 256) or 0. When
                        the sprite is at X position 1 the formula looks
                        like this: LX = 1 - (0 times 256) or 1. When the
                        sprite is at X position 256 the formula looks like
                        this: LX = 256 - (1 times 256) or 0 which resets X
                        back to 0 which must be done when you start over on
                        the RIGHT SIDE of the screen (POKEV+16,1).

  LINE 60:

    POKEV,LX            You POKE V by itself with a value to set the Hori-
                        zontal (X) Position of sprite 0 on the screen. (See
                        SPRITEMAKING CHART on Page 176). As shown above,
                        the value of LX, which is the horizontal position
                        of the sprite, changes from 0 to 255 and when it
                        reaches 255 it automatically resets back to zero
                        because of the LX equation set up in line 55.

    POKEV+16,RX         POKEV+16 always turns on the "right side" of the
                        screen beyond position 256, and resets the
                        horizontal positioning coordinates to zero. RX is
                        either a 0 or a 1 based on the position of the
                        sprite as determined by the RX formula in line 55.

  LINE 70:

    IFP=192THEN         If the sprite pointer is set to 192 (the first
    GOSUB200            sprite shape) the waveform control for the first
                        sound effect is set to 129 and 128 per line 200.

  LINE 75:

    IFP=193THEN         If the sprite pointer is set to 193 (the second
    GOSUB300            sprite shape) the waveform control for the second
                        sound effect (Voice 2) is set to 129 and 128 per
                        line 300.

  LINE 80:

    POKE2040,P          Sets the SPRITE POINTER to location 192 (remember
                        P=192 in line 45? Here's where we use the P).

    FORT=1TO60:         A simple time delay loop which sets the speed at
    NEXT                which the mouse dances. (Try a faster or slower
                        speed by increasing/decreasing the number 60.)

  LINE 85:

    P=P+1               Now we increase the value of the pointer by adding
                        1 to the original value of P.

    IFP>194THEN         We only want to point the sprite to 3 memory lo-
    P=192               cations. 192 points to locations 12288 to 12350,
                        193 points to locations 12352 to 12414, and 194
                        points to locations 12416 to 12478. This line tells
                        the computer to reset P back to 192 as soon as P
                        becomes 195 so P never really becomes 195. P is
                        192, 193, 194 and then resets back to 192 and the
                        pointer winds up pointing consecutively to the
                        three sprite shapes in the three 64-byte groups of
                        memory locations containing the DATA.

  LINE 90:

    NEXTX               After the sprite has become one of the 3 different
                        shapes defined by the DATA, only then is it allowed
                        to move across the screen. It will jump 3 X
                        positions at a time (instead of scrolling smoothly
                        one position at a time, which is also possible).
                        STEPping 3 positions at a time makes the mouse
                        "dance" faster across the screen. NEXT X matches
                        the FOR... X position loop in line 50.

  LINE 95

    END                 ENDs the program, which occurs when the sprite
                        moves off the screen.

  LINES 100-109

    DATA                The sprite shapes are read from the data numbers,
                        in order. First the 63 numbers which comprise
                        sprite shape 1 are read, then the 63 numbers for
                        sprite shape 2, and then sprite shape 3. This data
                        is permanently read into the 3 memory locations and
                        after it is read into these locations, all the
                        program has to do is point sprite 0 at the 3 memory
                        locations and the sprite automatically takes the
                        shape of the data in those locations. We are
                        pointing the sprite at 3 locations one at a time
                        which produces the "animation" effect. If you want
                        to see how these numbers affect each sprite, try
                        changing the first 3 numbers in LINE 100 to 255,
                        255, 255. See the section on defining sprite shapes
                        for more information.

  LINE 200:

    POKES+4,129         Waveform control set to 129 turns on the sound
                        effect.
    POKES+4,128         Waveform control set to 128 turns off the sound
                        effect.
    RETURN              Sends program back to end of line 70 after
                        waveform control settings are changed, to resume
                        program.

  LINE 300:

    POKES+11,129        Waveform control set to 129 turns on the sound
                        effect.
    POKES+11,128        Waveform control set to 128 turns off the sound
                        effect.
    RETURN              Sends program back to end of line 75 to resume.

  EASY SPRITEMAKING CHART
  +----------+------+------+------+------+-------+-------+-------+--------+
  |          |SPRT 0|SPRT 1|SPRT 2|SPRT 3|SPRT 4 |SPRT 5 |SPRT 6 | SPRT 7 |
  +----------+------+------+------+------+-------+-------+-------+--------+
  |Turn on   |V+21,1|V+21,2|V+21,4|V+21,8|V+21,16|V+21,32|V+21,64|V+21,128|
  +----------+------+------+------+------+-------+-------+-------+--------+
  |Put in mem| 2040,| 2041,| 2042,| 2043,| 2044, | 2045, | 2046, | 2047,  |
  |set point.|  192 |  193 |  194 |  195 |  196  |  197  |  198  |  199   |
  +----------+------+------+------+------+-------+-------+-------+--------+
  |Locations | 12288| 12352| 12416| 12480| 12544 | 12608 | 12672 | 12736  |
  |for Sprite|  to  |  to  |  to  |  to  |  to   |  to   |  to   |  to    |
  |Pixel     | 12350| 12414| 12478| 12542| 12606 | 12670 | 12734 | 12798  |
  +----------+------+------+------+------+-------+-------+-------+--------+
  |Color     |V+39,C|V+40,C|V+41,C|V+42,C|V+43,C |V+44,C |V+45,C |V+46,C  |
  +----------+------+------+------+------+-------+-------+-------+--------+
  |Set LEFT X| V+0,X| V+2,X| V+4,X| V+6,X| V+8,X |V+10,X |V+12,X |V+14,X  |
  +----------+------+------+------+------+-------+-------+-------+--------+
  |Set RIGHT |V+16,1|V+16,2|V+16,4|V+16,8|V+16,16|V+16,32|V+16,64|V+16,128|
  |X position| V+0,X| V+2,X| V+4,X| V+6,X| V+8,X |V+10,X |V+12,X |V+14,X  |
  +----------+------+------+------+------+-------+-------+-------+--------+
  |Set Y pos.| V+1,Y| V+3,Y| V+5,Y| V+7,Y| V+9,Y |V+11,Y |V+13,Y |V+15,Y  |
  +----------+------+------+------+------+-------+-------+-------+--------+
  |Exp. Horiz|V+29,1|V+29,2|V+29,4|V+29,8|V+29,16|V+29,32|V+29,64|V+29,128|
  +----------+------+------+------+------+-------+-------+-------+--------+
  |Exp. Vert.|V+23,1|V+23,2|V+23,4|V+23,8|V+23,16|V+23,32|V+23,64|V+23,128|
  +----------+------+------+------+------+-------+-------+-------+--------+
  |Multi-Col.|V+28,1|V+28,2|V+28,4|V+28,8|V+28,16|V+28,32|V+28,64|V+28,128|
  +----------+------+------+------+------+-------+-------+-------+--------+
  |M-Color 1 |V+37,C|V+37,C|V+37,C|V+37,C|V+37,C |V+37,C |V+37,C |V+37,C  |
  +----------+------+------+------+------+-------+-------+-------+--------+
  |M-Color 2 |V+38,C|V+38,C|V+38,C|V+38,C|V+38,C |V+38,C |V+38,C |V+38,C  |
  +----------+------+------+------+------+-------+-------+-------+--------+
  |Priority  | The rule is that lower numbered sprites always have display|
  |of sprites| priority over higher numbered sprites. For example, sprite |
  |          | 0 has priority over ALL other sprites, sprite 7 has last   |
  |          | priority. This means lower numbered sprites always appear  |
  |          | to move IN FRONT OF or ON TOP OF higher numbered sprites.  |
  +----------+------------------------------------------------------------+
  |S-S Collis| V+30   IF PEEK(V+30)ANDX=X THEN [action]                   |
  +----------+------------------------------------------------------------+
  |S-B Collis| V+31   IF PEEK(V+31)ANDX=X THEN [action]                   |
  +----------+------------------------------------------------------------+

  SPRITEMAKING NOTES

            Alternative Sprite Memory Pointers and Memory Locations
                            Using Cassette Buffer
  +---------------+-------+-------+-------+-------------------------------+
  | Put in Memory |SPRT 0 |SPRT 1 |SPRT 2 | If you're using 1 to 3 sprites|
  | (Set pointers)|2040,13|2041,14|2042,15| you can use these memory      |
  +---------------+-------+-------+-------+ locations in the cassette     |
  | Sprite Pixel  | 832   | 896   | 960   | buffer (832 to 1023) but for  |
  | Locations for | to 894| to 958|to 1022| more than 3 sprites we suggest|
  | Blocks 13-15  |       |       |       | using locations from 12288 to |
  +---------------+-------+-------+-------+ 12798 (see chart).            |
  TURNING ON SPRITES:                     +-------------------------------+

    You can turn on any individual sprite by using POKE V+21 and the number
  from the chart... BUT... turning on just ONE sprite will turn OFF any
  others. To turn on TWO OR MORE sprites, ADD TOGETHER the numbers of the
  sprites you want to turn on (Example: POKE V+21, 6 turns on sprites 1 and
  2). Here is a method you can use to turn one sprite off and on without
  affecting any of the others (useful for animation).

  EXAMPLE:

    To turn off just sprite 0 type: POKE V+21,PEEK V+21AND(255-1). Change
  the number 1 in (255-1) to 1,2,4,8,16,32,64, or 128 (for sprites 0-7). To
  re-enable the sprite and not affect the other sprites currently turned
  on, POKE V+21, PEEK(V+21)OR 1 and change the OR 1 to OR 2 (sprite 2), OR
  4 (sprite 3), etc.

  X POSITION VALUES BEYOND 255:

    X positions run from 0 to 255... and then START OVER from 0 to 255. To
  put a sprite beyond X position 255 on the far right side of the screen,
  you must first POKE V+ 16 as shown, THEN POKE a new X valve from 0 to 63,
  which will place the sprite in one of the X positions at the right side
  of the screen. To get back to positions 0-255, POKE V+16,0 and POKE in an
  X value from 0 to 255.

  Y POSITION VALUES:

    Y positions run from 0 to 255, including 0 to 49 off the TOP of the
  viewing area, 50 to 229 IN the,viewing area, and 230 to 255 off the
  BOTTOM of the viewing area.

  SPRITE COLORS:

    To make sprite 0 WHITE, type: POKE V+39,1 (use COLOR POKE SETTING shown
  in chart, and INDIVIDUAL COLOR CODES shown below):

    0-BLACK     4-PURPLE        8-ORANGE        12-MED. GREY
    1-WHITE     5-GREEN         9-BROWN         13-LT. GREEN
    2-RED       6-BLUE          10-LT. RED      14-LT. BLUE
    3-CYAN      7-YELLOW        11-DARK GREY    15-LT. GREY

  MEMORY LOCATION:

    You must "reserve" a separate 64-BYTE BLOCK of numbers in the
  computer's memory for each sprite of which 63 BYTES will be used for
  sprite data. The memory settings shown below are recommended for the
  "sprite pointer" settings in the chart above. Each sprite will be unique
  and you'll have to define it as you wish. To make all sprites exactly the
  same, point the sprites you want to look the same to the same register
  for sprites.

  DIFFERENT SPRITE POINTER SETTINGS:

    These sprite pointer settings are RECOMMENDATIONS ONLY.
    Caution: you can set your sprite pointers anywhere in RAM memory but if
  you set them too "low" in memory a long BASIC program may overwrite your
  sprite data, or vice versa. To protect an especially LONG BASIC PROGRAM
  from overwriting sprite data, you may want to set the sprites at a higher
  area of memory (for example, 2040,192 for sprite 0 at locations 12288 to
  12350... 2041,193 at locations 12352 to 12414 for sprite 1 and so on...
  by adjusting the memory locations from which sprites get their "data,"
  you can define as many as 64 different sprites plus a sizable BASIC
  program. To do this, define several sprite "shapes" in your DATA
  statements and then redefine a particular sprite by changing the
  "pointer" so the sprite you are using is "pointed" at different areas of
  memory containing different sprite picture data. See the "Dancing Mouse"
  to see how this works. If you want two or more sprites to have THE SAME
  SHAPE (you can still change position and color of each sprite), use the
  same sprite pointer and memory location for the sprites you want to match
  (for example, you can point sprites 0 and 1 to the same location by using
  POKE 2040,192 and POKE 2041, 192).

  PRIORITY:

    Priority means one sprite will appear to move "in front of" or "behind"
  another sprite on the display screen. Sprites with more priority always
  appear to move "in front of" or "on top of" sprites with less priority.
  The rule is that lower numbered sprites have priority over higher
  numbered sprites. Sprite 0 has priority over all other sprites. Sprite 7
  has no priority in relation to the other sprites. Sprite 1 has priority
  over sprites 2-7, etc. If you put two sprites in the some position, the
  sprite with the higher priority will appear IN FRONT OF the sprite with
  the lower priority. The sprite with lower priority will either be
  obscured, or will "show through" (from "behind") the sprite with higher
  priority.

  USING MULTI-COLOR:

    You can create multi-colored sprites although using multi-color mode
  requires that you use PAIRS of pixels instead of individual pixels in
  your sprite picture (in other words each colored "dot" or "block" in the
  sprite will consist of two pixels side by side). You have 4 colors to
  choose from: Sprite Color (chart,above), Multi-Color 1, Multi-Color 2 and
  "Background Color" (background is achieved by using zero settings which
  let the background color "show through"). Consider one horizontal 8-pixel
  block in a sprite picture. The color of each PAIR of pixels is determined
  according to whether the left, right, or both pixels are solid, like
  this:

  +-+-+
  | | | BACKGROUND      (Making BOTH PIXELS BLANK (zero) lets the
  +-+-+                  INNER SCREEN COLOR (background)show through.)

  +-+-+
  | |@| MULTI-COLOR 1   (Making the RIGHT PIXEL SOLID in a pair of pixels
  +-+-+                  sets BOTH PIXELS to Multi-Color 1.)

  +-+-+
  |@| | SPRITE COLOR    (Making the LEFT PIXEL SOLID in a pair of pixels
  +-+-+                  sets BOTH PIXELS to Sprite Color.)

  +-+-+
  |@|@| MULTI-COLOR 2   (Making BOTH PIXELS SOLID in a pair of pixels
  +-+-+                  sets BOTH PIXELS to Multi-Color 2.)

  Look at the horizontal 8-pixel row shown below. This block sets the first
  two pixels to background color, the second two pixels to Multi-Color 1,
  the third two pixels to Sprite Color and the fourth two pixels to Multi-
  Color 2. The color of each PAIR of pixels depends on which bits in each
  pair are solid and which are blank, according to the illustration above.
  After you determine which colors you want in each pair of pixels, the
  next step is to add the values of the solid pixels in the 8-pixel block,
  and POKE that number into the proper memory location. For example, if the
  8-pixel row shown below is the first block in a sprite which begins at
  memory location 832, the value of the solid pixels is 16+8+2+1 27, so you
  would POKE 832,27.

                     |128| 64| 32| 16|  8|  4|  2|  1|   16+8+2+1 = 27
                     +---+---+---+---+---+---+---+---+
                     |   |   |   |@@@|@@@|   |@@@|@@@|
                     |   |   |   |@@@|@@@|   |@@@|@@@|
                     +---+---+---+---+---+---+---+---+

                         LOOKS LIKE THIS IN SPRITE

                     +-------+-------+-------+-------+
                     |BACKGR.|MULTI- |SPRITE |MULTI- |
                     | COLOR |COLOR 1| COLOR |COLOR 2|
                     +-------+-------+-------+-------+

  COLLISION:

    You can detect whether a sprite has collided with another sprite by
  using this line: IF PEEK(V+30)ANDX=XTHEN [insert action here]. This line
  checks to see if a particular sprite has collided with ANY OTHER SPRITE,
  where X equals 1 for sprite 0, 2 for sprite 1, 4 for sprite 2, 8 for
  sprite 3, 16 for sprite 4, 32 for sprite 5, 64 for sprite 6, and 128 for
  sprite 7. To check to see if the sprite has collided with a "BACKGROUND
  CHARACTER" use this line: IF PEEK(V+31)ANDX=XTHEN [insert action here].

  USING GRAPHIC CHARACTERS IN DATA STATEMENTS

    The following program allows you to create a sprite using blanks and
  solid circles <SHIFT+Q> in DATA statements. The sprite and the numbers
  POKED into the sprite data registers are displayed.

  10 print"{clear}":fori=0to63:poke832+i,0:next
  20 gosub60000
  999 end
  60000 data"         QQQQQQQ        "
  60001 data"       QQQQQQQQQQQ      "
  60002 data"      QQQQQQQQQQQQQ     "
  60003 data"      QQQQQ   QQQQQ     "
  60004 data"     QQQQQ QQQ  QQQQ    "
  60005 data"     QQQQQ QQQ QQQQQ    "
  60006 data"     QQQQQ QQQ  QQQQ    "
  60007 data"      QQQQQ   QQQQQ     "
  60008 data"      QQQQQQQQQQQQQ     "
  60009 data"      QQQQQQQQQQQQQ     "
  60010 data"      Q QQQQQQQQQ Q     "
  60011 data"       Q QQQQQQQ Q      "
  60012 data"       Q  QQQQQ  Q      "
  60013 data"        Q  QQQ  Q       "
  60014 data"        Q  QQQ  Q       "
  60015 data"         Q  Q  Q        "
  60016 data"         Q  Q  Q        "
  60017 data"          QQQQQ         "
  60018 data"          QQQQQ         "
  60019 data"          QQQQQ         "
  60020 data"           QQQ          "
  60100 v=53248:pokev,200:pokev+1,100:pokev+21,1:pokev+39,14:poke2040,13
  60105 pokev+23,1:pokev+29,1
  60110 fori=0to20:reada$:fork=0to2:t=0:forj=0to7:b=0
  60140 ifmid$(a$,j+k*8+1,1)="Q"thenb=1
  60150 t=t+b*2^(7-j):next:printt;:poke832+i*3+k,t:next:print:next
  60200 return
