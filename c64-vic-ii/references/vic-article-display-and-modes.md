> Source: vic-ii.txt §3.4–3.7, "Display generation, Bad Lines, memory access/raster timing, text/bitmap display and all graphics modes (incl. the invalid ones)". By Christian Bauer (28.Aug.1996). Lightly cleaned (Φ clock-signal mojibake restored).

3.4. Display generation and display window dimensions
-----------------------------------------------------

As usual for controlling CRTs, the VIC builds the video frame line by line.
The line number and the number of clock cycles per line are constant for
every VIC type. The VIC works character-based, every character consists of
a matrix of 8×8 pixels, so a text line is made up of 8 pixel lines. 40×25
text characters are displayed in the text based modes, 320×200 or 160×200
pixels in the bitmap modes.

In this article, the specification of a position on the screen is done with
the raster line number as the Y coordinate (RASTER, register $d011/$d012)
and a X coordinate that corresponds to the sprite coordinate system. When
specifying the time of a VIC memory access or an internal operation in the
VIC, the raster line number is used as Y coordinate and the number of the
clock cycle within the line as X coordinate. As previously mentioned, 8
pixels make a clock cycle, so the specification of a sprite X coordinate is
eight times more precise than that of a cycle number.

The graphics are displayed in an unmovable window in the middle of the
visible screen area, the "display window". The area outside the display
window is covered by the screen border and is displayed in the border color
(EC, register $d020). You can also turn off the border partially or
completely with some little tweaking; then you see that the display window
is part of a "display column" that is made up by the linear extension of
the display window to the top and bottom. With that you can divide the
border in an upper/lower border and a left/right border. The visible screen
area is surrounded by blanking intervals in which the video signal is
turned off and in which the raster beam returns to the start of the next
line or the start of the frame, respectively.

The following figure (not in scale) illustrates the last paragraph:


                Visible pixels/line
     ____________________|___________________
    /                                        \

+------------------------------------------------+  <- Raster line 0 (6569)
|       .                                .       |
|       .   Vertical blanking interval   .       |
|       .                                .       |
+---+---+--------------------------------+---+---+  \
|   |   |                                |   |   |  |
| H |   |          Upper border          |   | H |  |
| o |   |                                |   | o |  |
| r |   +--------------------------------+   | r |  |
| i |   |                                |   | i |  |
| z |   |                                |   | z |  |
| o |   |                                |   | o |  |
| n |   |                                |   | n |  |
| t |   |                                |   | t |  |
| a |   |                                | r | a |  |
| l | l |                                | i | l |  |
|   | e |                                | g |   |  |
| b | f |                                | h | b |  |
| l | t |                                | t | l |  |
| a |   |         Display window         |   | a |  |- Visible lines
| n | b |                                | b | n |  |
| k | o |                                | o | k |  |
| i | r |                                | r | i |  |
| n | d |                                | d | n |  |
| g | e |                                | e | g |  |
|   | r |                                | r |   |  |
| i |   |                                |   | i |  |
| n |   |                                |   | n |  |
| t |   |                                |   | t |  |
| e |   |                                |   | e |  |
| r |   |                                |   | r |  |
| v |   +--------------------------------+   | v |  |
| a |   |                                |   | a |  |
| l |   |          Lower border          |   | l |  | <- Raster line 0 (6567)
|   |   |                                |   |   |  |
+---+---+--------------------------------+---+---+  /
|       .                                .       |
|       .   Vertical blanking interval   .       |
|       .                                .       |
+------------------------------------------------+
 
      ^ \________________________________/
      |                 |
      |           Display column
      |
 X coordinate 0


The height and width of the display window can each be set to two different
values with the bits RSEL and CSEL in the registers $d011 and $d016:

 RSEL|  Display window height   | First line  | Last line
 ----+--------------------------+-------------+----------
   0 | 24 text lines/192 pixels |   55 ($37)  | 246 ($f6)
   1 | 25 text lines/200 pixels |   51 ($33)  | 250 ($fa)

 CSEL|   Display window width   | First X coo. | Last X coo.
 ----+--------------------------+--------------+------------
   0 | 38 characters/304 pixels |   31 ($1f)   |  334 ($14e)
   1 | 40 characters/320 pixels |   24 ($18)   |  343 ($157)

If RSEL=0 the upper and lower border are each extended by 4 pixels into the
display window, if CSEL=0 the left border is extended by 7 pixels and the
right one by 9 pixels. The position of the display window and its
resolution do not change, RSEL/CSEL only switch the starting and ending
position of the border display. The size of the video matrix also stays
constantly at 40×25 characters.

With XSCROLL/YSCROLL (bits 0-2 of registers $d011 (XSCROLL) and $d016
(YSCROLL)), the position of the graphics inside the display window can be
scrolled in single-pixel units up to 7 pixels to the right and to the
bottom. This can be used for soft scrolling. The position of the display
window itself doesn't change. To keep the graphics aligned with the window,
X/YSCROLL have to be 0 and 3 for 25 lines/40 columns and both 7 for 24
lines/38 columns.

The dimensions of the video display for the different VIC types are as
follows:

          | Video  | # of  | Visible | Cycles/ |  Visible
   Type   | system | lines |  lines  |  line   | pixels/line
 ---------+--------+-------+---------+---------+------------
 6567R56A | NTSC-M |  262  |   234   |   64    |    411
  6567R8  | NTSC-M |  263  |   235   |   65    |    418
   6569   |  PAL-B |  312  |   284   |   63    |    403

          | First  |  Last  |              |   First    |   Last
          | vblank | vblank | First X coo. |  visible   |  visible
   Type   |  line  |  line  |  of a line   |   X coo.   |   X coo.
 ---------+--------+--------+--------------+------------+-----------
 6567R56A |   13   |   40   |  412 ($19c)  | 488 ($1e8) | 388 ($184)
  6567R8  |   13   |   40   |  412 ($19c)  | 489 ($1e9) | 396 ($18c)
   6569   |  300   |   15   |  404 ($194)  | 480 ($1e0) | 380 ($17c)

If you are wondering why the first visible X coordinates seem to come after
the last visible ones: This is because for the reference point to mark the
beginning of a raster line, the occurrence of the raster IRQ has been
chosen, which doesn't coincide with X coordinate 0 but with the coordinate
given as "First X coo. of a line". The X coordinates run up to $1ff (only
$1f7 on the 6569) within a line, then comes X coordinate 0. This is
explained in more detail in the explanation of the structure of a raster
line.

3.5. Bad Lines
--------------

As already mentioned, the VIC needs 40 additional bus cycles when fetching
the character pointers (i.e. the character codes of one text line from the
video matrix), because the 63-65 bus cycles available for transparent
(unnoticed by the processor) access for the VIC during the first clock
phases within a line are not sufficient to read both the character pointers
and the pixel data for the characters from memory.

For this reason, the VIC uses the mechanism described in section 2.4.3. to
"stun" the processor for 40-43 cycles during the first pixel line of each
text line to read the character pointers. The raster lines in which this
happens are usually called "Bad Lines" ("bad" because they stop the
processor and thus slow down the computer and lead to problems if the
precise timing of a program is essential, e.g. for the transmission of data
to/from a floppy drive).

The character pointer access is also done in the bitmap modes, because the
video matrix data is then used for color information.

Normally, every eighth line inside the display window, starting with the
very first line of the graphics, is a Bad Line, i.e the first raster lines
of each text line. So the position of the Bad Lines depends on the YSCROLL.
As you will see later, the whole graphics display and memory access scheme
depend completely on the position of the Bad Lines.

It is therefore necessary to introduce a more general definition, namely
that of a "Bad Line Condition":

 A Bad Line Condition is given at any arbitrary clock cycle, if at the
 negative edge of Φ0 at the beginning of the cycle RASTER >= $30 and RASTER
 <= $f7 and the lower three bits of RASTER are equal to YSCROLL and if the
 DEN bit was set during an arbitrary cycle of raster line $30.

This definition has to be taken literally. You can generate and take away a
Bad Line condition multiple times within an arbitrary raster line in the
range of $30-$f7 by modifying YSCROLL, and thus make every raster line
within the display window completely or partially a Bad Line, or trigger or
suppress all the other functions that are connected with a Bad Line
Condition. If YSCROLL=0, a Bad Line Condition occurs in raster line $30 as
soon as the DEN bit (register $d011, bit 4) is set (for more about the DEN
bit, see section 3.10.).

The following three sections describe the function units that are used for
displaying the graphics. Section 3.6. explains the the memory interface
that is used to read the graphics data and the timing of the accesses
within a raster line. Section 3.7. is about the display unit that converts
the text and bitmap graphics data into colors and generates the addresses
for the memory access. Section 3.8. covers the sprites and their address
generation.

3.6. Memory access
------------------

3.6.1. The X coordinates
------------------------

Before explaining the timing of memory accesses within a raster line, we
will quickly explain how to obtain the X coordinates. This is necessary
because the VIC doesn't have a counterpart to the RASTER register (which
gives the current Y coordinate) to hold the X coordinates, so you cannot
simply read them with the processor. But the VIC surely keeps track of the
X coordinates internally as the horizontal sprite positions are based on
them, and a pulse at the lightpen input LP latches the current X position
in the register LPX ($d013).

Determining the absolute X coordinates of events within a raster line is
not trivial as you cannot e.g. simply put a sprite to a well-defined X
coordinate and conclude from the text characters displayed at the same X
position to the X coordinates of the memory accesses belonging to these
characters. The memory access and the display are separate function units
and the read graphics data is not immediately displayed on the screen
(there is a delay of 12 pixels).

So a different approach has been taken: The absolute position of a single X
coordinate within the raster line was measured with the LPX register and
the other X coordinates were determined relative to this. To do that, the
IRQ output of the VIC has been connected to the LP input and the VIC has
been programmed for a raster line interrupt. As the negative edge of IRQ
was defined to be the start of a raster line, the absolute X position of
the line start could be determined. The position of the negative edge of BA
during a Bad Line was also measured with this method and the result was
consistent with the relative distance of IRQ and BA to each other. Based on
these two measurements, the X coordinates of all other events within a
raster line have been determined (see [4]). Not until now the sprite X
coordinates were used to be able to determine the moment of the display
generation of the text characters.

This of course implicitly assumes that the LPX coordinates are the same as
the sprite X coordinates. There is, however, no indication and thus no
reason to suppose that they don't (a direct correlation would also be the
most simple solution in terms of circuit design).

3.6.2. Access types
-------------------

The VIC generates two kinds of graphics that require access to memory: The
text/bitmap graphics (also often called "background graphics" or simply
"graphics") and the sprite graphics. Both require accesses to two separated
memory areas:

For the text/bitmap graphics:

 · The video matrix; an area of 1000 video addresses (40×25, 12 bits each)
   that can be moved in 1KB steps within the 16KB address space of the VIC
   with the bits VM10-VM13 of register $d018. It stores the character codes
   and their color for the text modes and some of the color information of
   8×8 pixel blocks for the bitmap modes. The Color RAM is part of the
   video matrix, it delivers the upper 4 bits of the 12 bit matrix. The
   data read from the video matrix is stored in an internal buffer in the
   VIC, the 40×12 bit video matrix/color line.

 · The character generator resp. the bitmap; an area of 2048 bytes (bitmap:
   8192 bytes) that can be moved in 2KB steps (bitmap: 8KB steps) within
   the VIC address space with the bits CB11-CB13 (bitmap: only CB13) of
   register $d018. It stores the pixel data of the characters for the text
   modes and the bitmap for the bitmap modes. The character generator has
   basically nothing to do with the Char ROM. The Char ROM only contains
   prepared bit patterns that can be used as character generator, but you
   can also store the character generator in normal RAM to define your own
   character images.

For the sprites:

 · The sprite data pointers; 8 bytes after the end of the video matrix,
   that select one out of 256 blocks of 64 bytes within the VIC address
   space for each sprite.

 · The sprite data; an area of 63 bytes containing the pixel data of the
   sprites which can be moved in steps of 64 bytes with the sprite data
   pointers independently for each sprite.

Corresponding to that, the VIC does 4 different kinds of graphics accesses:

1. To the video matrix ("c-access", 12 bits wide).
2. To the pixel data, i.e. character generator or bitmap ("g-access", 8
   bits wide).
3. To the sprite data pointers ("p-access", 8 bits wide).
4. To the sprite data ("s-access", 8 bits wide).

Moreover, the VIC does two additional types of accesses:

5. Accesses for refreshing the dynamic RAM, 5 read accesses per raster
   line.

6. Idle accesses. As described, the VIC accesses in every first clock phase
   although there are some cycles in which no other of the above mentioned
   accesses is pending. In this case, the VIC does an idle access; a read
   access to video address $3fff (i.e. to $3fff, $7fff, $bfff or $ffff
   depending on the VIC bank) of which the result is discarded.

3.6.3. Timing of a raster line
------------------------------

The sequence of VIC memory accesses within a raster line is hard-wired,
independent of the graphics mode and the same for every raster line. The
negative edge of IRQ on a raster interrupt has been used to define the
beginning of a line (this is also the moment in which the RASTER register
is incremented). Raster line 0 is, however, an exception: In this line, IRQ
and incrementing (resp. resetting) of RASTER are performed one cycle later
than in the other lines. But for simplicity we assume equal line lengths
and define the beginning of raster line 0 to be one cycle before the
occurrence of the IRQ.

First the timing diagrams, the explanation follows:


6569, Bad Line, no sprites:

Cycl-# 6                   1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3 3 3 4 4 4 4 4 4 4 4 4 4 5 5 5 5 5 5 5 5 5 5 6 6 6 6
       3 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 1
        _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
    Φ0 _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
       __
   IRQ   ________________________________________________________________________________________________________________________________
       ________________________                                                                                      ____________________
    BA                         ______________________________________________________________________________________
        _ _ _ _ _ _ _ _ _ _ _ _ _ _ _                                                                                 _ _ _ _ _ _ _ _ _ _
   AEC _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _________________________________________________________________________________ _ _ _ _ _ _ _ _ _

   VIC i 3 i 4 i 5 i 6 i 7 i r r r r rcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcgcg i i 0 i 1 i 2 i 3
  6510  x x x x x x x x x x x x X X X                                                                                 x x x x x x x x x x

Graph.                      |===========01020304050607080910111213141516171819202122232425262728293031323334353637383940=========

X coo. \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
       1111111111111111111111111110000000000000000000000000000000000000000000000000000000000000000111111111111111111111111111111111111111
       89999aaaabbbbccccddddeeeeff0000111122223333444455556666777788889999aaaabbbbccccddddeeeeffff000011112222333344445555666677778888999
       c048c048c048c048c048c048c04048c048c048c048c048c048c048c048c048c048c048c048c048c048c048c048c048c048c048c048c048c048c048c048c048c048


6569, no Bad Line, no sprites (abbreviated):

Cycl-# 6                   1 1 1 1 1 1 1 1 1 1 |5 5 5 5 5 5 5 6 6 6 6
       3 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 |3 4 5 6 7 8 9 0 1 2 3 1
        _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _| _ _ _ _ _ _ _ _ _ _ _ _
    Φ0 _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ |_ _ _ _ _ _ _ _ _ _ _ _
       __                                      |
   IRQ   ______________________________________|________________________
       ________________________________________|________________________
    BA                                         |
        _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _| _ _ _ _ _ _ _ _ _ _ _ _
   AEC _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ |_ _ _ _ _ _ _ _ _ _ _ _ 
                                               |
   VIC i 3 i 4 i 5 i 6 i 7 i r r r r r g g g g |g g g i i 0 i 1 i 2 i 3
  6510  x x x x x x x x x x x x x x x x x x x x| x x x x x x x x x x x x
                                               |
Graph.                      |===========0102030|7383940=========
                                               |
X coo. \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|\\\\\\\\\\\\\\\\\\\\\\\\
       1111111111111111111111111110000000000000|111111111111111111111111
       89999aaaabbbbccccddddeeeeff0000111122223|344445555666677778888999
       c048c048c048c048c048c048c04048c048c048c0|c048c048c048c048c048c048


6567R56A, Bad Line, sprites 5-7 active in this line, sprite 0 in the next
line (abbreviated):

Cycl-# 6                   1 1 1 1 1 1 1 1 1 1 |5 5 5 5 5 5 5 6 6 6 6 6
       4 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 |3 4 5 6 7 8 9 0 1 2 3 4 1
        _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _| _ _ _ _ _ _ _ _ _ _ _ _ _
    Φ0 _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ |_ _ _ _ _ _ _ _ _ _ _ _ _ 
       __                                      |
   IRQ   ______________________________________|__________________________
       ____                  __                |    __          __________
    BA     __________________  ________________|____  __________
        _ _ _ _ _             _ _ _ _          |     _ _ _ _     _ _ _ _ _
   AEC _ _ _ _ _ _____________ _ _ _ __________|_____ _ _ _ _____ _ _ _ _ 
                                               |
   VIC i 3 i 4 i 5sss6sss7sssr r r r rcgcgcgcgc|gcgcg i i i 0sss1 i 2 i 3 
  6510  x x X X X             x X X X          |     x X X X     x x x x x
                                               |
Graph.                      |===========0102030|7383940===========
                                               |
X coo. \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|\\\\\\\\\\\\\\\\\\\\\\\\\\
       1111111111111111111111111110000000000000|11111111111111111111111111
       999aaaabbbbccccddddeeeeffff0000111122223|3444455556666777788889999a
       48c048c048c048c048c048c048c048c048c048c0|c048c048c048c048c048c048c0


6567R8, no Bad Line, sprites 2-7 active in this line, sprites 0-4 in the
next line (abbreviated):

Cycl-# 6                   1 1 1 1 1 1 1 1 1 1 |5 5 5 5 5 5 5 6 6 6 6 6 6
       5 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 |3 4 5 6 7 8 9 0 1 2 3 4 5 1
        _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _| _ _ _ _ _ _ _ _ _ _ _ _ _ _
    Φ0 _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ |_ _ _ _ _ _ _ _ _ _ _ _ _ _
       __                                      |
   IRQ   ______________________________________|____________________________
                             __________________|________
    BA ______________________                  |        ____________________
                              _ _ _ _ _ _ _ _ _| _ _ _ _ _ _ _
   AEC _______________________ _ _ _ _ _ _ _ _ |_ _ _ _ _ _ _ ______________
                                               |
   VIC ss3sss4sss5sss6sss7sssr r r r r g g g g |g g g i i i i 0sss1sss2sss3s
  6510                        x x x x x x x x x| x x x x X X X
                                               |
Graph.                      |===========0102030|7383940============
                                               |
X coo. \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\|\\\\\\\\\\\\\\\\\\\\\\\\\\\\
       1111111111111111111111111110000000000000|1111111111111111111111111111
       999aaaabbbbccccddddeeeeffff0000111122223|344445555666677778888889999a
       48c048c048c048c048c048c048c048c048c048c0|c048c048c048c048c04cccc04c80


The line "Cycl-#" show the number of the clock cycle within the raster
line. The line starts with cycle 1 and consists of 63 cycles on the 6569,
of 64 cycles on the 6567R56A and of 65 cycles on the 6567R8. The last cycle
of the previous line and the first cycle of the next line have also been
included in the diagrams to make things clearer.

The lines "Φ0", "IRQ", "BA" and "AEC" reflect the state of the bus signals
with the same names. Φ0 is low in the first phase and high in the second
phase.

The symbols in the lines "VIC" and "6510" show what kind of access VIC and
6510 do in the corresponding clock phase (for an explanation of the
different access types of the VIC see section 3.6.2.):

  c  Access to video matrix and Color RAM (c-access)
  g  Access to character generator or bitmap (g-access)
 0-7 Reading the sprite data pointer for sprite 0-7 (p-access)
  s  Reading the sprite data (s-access)
  r  DRAM refresh
  i  Idle access

  x  Read or write access of the processor
  X  Processor may do write accesses, stops on first read (BA is low and so
     is RDY)

The line "X coo." contains the X coordinates of the beginning of each clock
phase (thus the "\\\" as a reminder) and the line "Graph." is a projection
of the 40 column display window and the border to these coordinates, for
positioning sprites. However, this doesn't correspond to the signal on the
VIC video output. Also you cannot see from the "Graph." line when the
border unit generates the border. This happens approx. 8 pixels later than
shown in the "Graph." line.

To time the accesses of the processor within a raster line when
programming, it's best to use the VIC g-accesses for orientation by
changing a byte in graphics memory with the 6510 and watching on the screen
on which character the change is first visible. The write access of the
processor must then have occurred in the clock phase immediately before.
Then you can use the diagrams to determine the clock cycle in which the
access took place and count the other accesses relative to it.

3.7. Text/bitmap display
------------------------

3.7.1. Idle state/display state
-------------------------------

The text/bitmap display logic in the VIC is in one of two states at any
time: The idle state and the display state.

 - In display state, c- and g-accesses take place, the addresses and
   interpretation of the data depend on the selected display mode.

 - In idle state, only g-accesses occur. The access is always to address
   $3fff ($39ff when the ECM bit in register $d016 is set). The graphics
   are displayed by the sequencer exactly as in display state, but with
   the video matrix data treated as "0" bits.

The transition from idle to display state occurs as soon as there is a Bad
Line Condition (see section 3.5.). The transition from display to idle
state occurs in cycle 58 of a line if the RC (see next section) contains
the value 7 and there is no Bad Line Condition.

As long as register $d011 is not modified in the middle of a frame, the
display logic is in display state within the display window and in idle
state outside of it. If you set a YSCROLL other than 3 in a 25 line display
window and store a value not equal to zero in $3fff you can see the stripes
generated by the sequencer in idle state on the upper or lower side of the
window.

In [4], idle accesses as well as g-accesses in idle state are called "idle
bus cycle". But the two phenomena are not the same. The accesses marked
with "+" in the diagrams of [4] are normal g-accesses. In this article, the
term "idle access" is only used for the accesses marked with "i" in the
diagrams in section 3.6.3., and not for the g-accesses during idle state.

3.7.2. VC and RC
----------------

Probably the most important result of the VIC examinations is the discovery
of the function of the internal registers "VC" and "RC" of the VIC. They
are used to generate the addresses for accessing the video matrix and the
character generator/bitmap.

Strictly speaking there are three registers:

 · "VC" (video counter) is a 10 bit counter that can be loaded with the
   value from VCBASE.
 · "VCBASE" (video counter base) is a 10 bit data register with reset input
   that can be loaded with the value from VC.
 · "RC" (row counter) is a 3 bit counter with reset input.

Besides this, there is a 6 bit counter with reset input that keeps track of
the position within the internal 40×12 bit video matrix/color line where
read character pointers are stored resp. read again. I will call this
"VMLI" (video matrix line index) here.

There four registers behave according to the following rules:

1. Once somewhere outside of the range of raster lines $30-$f7 (i.e.
   outside of the Bad Line range), VCBASE is reset to zero. This is
   presumably done in raster line 0, the exact moment cannot be determined
   and is irrelevant.

2. In the first phase of cycle 14 of each line, VC is loaded from VCBASE
   (VCBASE->VC) and VMLI is cleared. If there is a Bad Line Condition in
   this phase, RC is also reset to zero.

3. If there is a Bad Line Condition in cycles 12-54, BA is set low and the
   c-accesses are started. Once started, one c-access is done in the second
   phase of every clock cycle in the range 15-54. The read data is stored
   in the video matrix/color line at the position specified by VMLI. These
   data is internally read from the position specified by VMLI as well on
   each g-access in display state.

4. VC and VMLI are incremented after each g-access in display state.

5. In the first phase of cycle 58, the VIC checks if RC=7. If so, the video
   logic goes to idle state and VCBASE is loaded from VC (VC->VCBASE). If
   the video logic is in display state afterwards (this is always the case
   if there is a Bad Line Condition), RC is incremented.

These rules normally see that VC counts all 1000 addresses of the video
matrix within the display frame and that RC counts the 8 pixel lines of
each text line. The behavior of VC and RC is largely determined by Bad Line
Conditions which you can control with the processor via YSCROLL, giving you
control of the VC and RC within certain limits.

3.7.3 Graphics modes
--------------------

The graphics data sequencer is capable of 8 different graphics modes that
are selected by the bits ECM, BMM and MCM (Extended Color Mode, Bit Map
Mode and Multi Color Mode) in the registers $d011 and $d016 (of the 8
possible bit combinations, 3 are "invalid" and generate the same output,
the color black). The idle state is a bit special in that no c-accesses
occur in it and the sequencer uses "0" bits for the video matrix data.

The sequencer outputs the graphics data in every raster line in the area of
the display column as long as the vertical border flip-flop is reset (see
section 3.9.). Outside of the display column and if the flip-flop is set,
the last current background color is displayed (this area is normally
covered by the border). The heart of the sequencer is an 8 bit shift
register that is shifted by 1 bit every pixel and reloaded with new
graphics data after every g-access. With XSCROLL from register $d016 the
reloading can be delayed by 0-7 pixels, thus shifting the display up to 7
pixels to the right.

The address generator for the text/bitmap accesses (c- and g-accesses) has
basically 3 modes for the g-accesses (the c-accesses always follow the same
address scheme). In display state, the BMM bit selects either character
generator accesses (BMM=0) or bitmap accesses (BMM=1). In idle state, the
g-accesses are always done at video address $3fff. If the ECM bit is set,
the address generator always holds the address lines 9 and 10 low without
any other changes to the addressing scheme (e.g. the g-accesses in idle
state then occur at address $39ff).

The 8 graphics modes are now covered separately and the generated addresses
and the interpretation of the read data on c- and g-accesses is described.
This is followed by a description of the pecularities of the idle state.
For easy reference, the addresses are always given explicitly for every
mode although e.g. the c-accesses are always the same.

3.7.3.1. Standard text mode (ECM/BMM/MCM=0/0/0)
-----------------------------------------------

In this mode (as in all text modes), the VIC reads 8 bit character pointers
from the video matrix that specify the address of the dot matrix of the
character in the character generator. A character set of 256 characters is
available, each consisting of 8×8 pixels which are stored in 8 successive
bytes in the character generator. Video matrix and character generator can
be moved in memory with the bits VM10-VM13 and CB11-CB13 of register $d018.

In standard text mode, every bit in the character generator directly
corresponds to one pixel on the screen. The foreground color is given by
the color nybble from the video matrix for each character, the background
color is set globally with register $d021.

c-access

 Addresses

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 |VM13|VM12|VM11|VM10| VC9| VC8| VC7| VC6| VC5| VC4| VC3| VC2| VC1| VC0|
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+

 Data

 +----+----+----+----+----+----+----+----+----+----+----+----+
 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+
 |      Color of     | D7 | D6 | D5 | D4 | D3 | D2 | D1 | D0 |
 |     "1" pixels    |    |    |    |    |    |    |    |    |
 +-------------------+----+----+----+----+----+----+----+----+

g-access

 Addresses

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 |CB13|CB12|CB11| D7 | D6 | D5 | D4 | D3 | D2 | D1 | D0 | RC2| RC1| RC0|
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+

 Data

 +----+----+----+----+----+----+----+----+
 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+
 |         8 pixels (1 bit/pixel)        |
 |                                       |
 | "0": Background color 0 ($d021)       |
 | "1": Color from bits 8-11 of c-data   |
 +---------------------------------------+

3.7.3.2. Multicolor text mode (ECM/BMM/MCM=0/0/1)
-------------------------------------------------

This mode allows for displaying four-colored characters at the cost of
horizontal resolution. If bit 11 of the c-data is zero, the character is
displayed as in standard text mode with only the colors 0-7 available for
the foreground. If bit 11 is set, each two adjacent bits of the dot matrix
form one pixel. By this means, the resolution of a character of reduced to
4×8 (the pixels are twice as wide, so the total width of the characters
doesn't change).

It is interesting that not only the bit combination "00" but also "01" is
regarded as "background" for the sprite priority and collision detection.

c-access

 Addresses

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 |VM13|VM12|VM11|VM10| VC9| VC8| VC7| VC6| VC5| VC4| VC3| VC2| VC1| VC0|
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+

 Data

 +----+----+----+----+----+----+----+----+----+----+----+----+
 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+
 | MC |   Color of   | D7 | D6 | D5 | D4 | D3 | D2 | D1 | D0 |
 |flag|  "11" pixels |    |    |    |    |    |    |    |    |
 +----+--------------+----+----+----+----+----+----+----+----+

g-access

 Addresses

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 |CB13|CB12|CB11| D7 | D6 | D5 | D4 | D3 | D2 | D1 | D0 | RC2| RC1| RC0|
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+

 Data

 +----+----+----+----+----+----+----+----+
 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+
 |         8 pixels (1 bit/pixel)        |
 |                                       | MC flag = 0
 | "0": Background color 0 ($d021)       |
 | "1": Color from bits 8-10 of c-data   |
 +---------------------------------------+
 |         4 pixels (2 bits/pixel)       |
 |                                       |
 | "00": Background color 0 ($d021)      | MC flag = 1
 | "01": Background color 1 ($d022)      |
 | "10": Background color 2 ($d023)      |
 | "11": Color from bits 8-10 of c-data  |
 +---------------------------------------+

3.7.3.3. Standard bitmap mode (ECM/BMM/MCM=0/1/0)
-------------------------------------------------

In this mode (as in all bitmap modes), the VIC reads the graphics data from
a 320×200 bitmap in which every bit corresponds to one pixel on the screen.
The data from the video matrix is used for color information. As the video
matrix is still only a 40×25 matrix, you can only specify the colors for
blocks of 8×8 pixels individually (sort of a YC 8:1 format). As the
designers of the VIC wanted to realize the bitmap mode with as little
additional circuitry as possible (the VIC-I didn't have a bitmap mode), the
arrangement of the bitmap in memory is somewhat weird: In contrast to
modern video chips that read the bitmap in a linear fashion from memory,
the VIC forms an 8×8 pixel block on the screen from 8 successive bytes of
the bitmap. The video matrix and the bitmap can be moved in memory with the
bits VM10-VM13 and CB13 of register $d018.

In standard bitmap mode, every bit in the bitmap directly corresponds to
one pixel on the screen. Foreground and background color can be arbitrarily
set for every 8×8 block.

c-access

 Addresses

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 |VM13|VM12|VM11|VM10| VC9| VC8| VC7| VC6| VC5| VC4| VC3| VC2| VC1| VC0|
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+

 Data

 +----+----+----+----+----+----+----+----+----+----+----+----+
 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+
 |       unused      |     Color of      |     Color of      |
 |                   |    "1" pixels     |    "0" pixels     |
 +-------------------+-------------------+-------------------+

g-access

 Addresses

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 |CB13| VC9| VC8| VC7| VC6| VC5| VC4| VC3| VC2| VC1| VC0| RC2| RC1| RC0|
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+

 Data

 +----+----+----+----+----+----+----+----+
 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+
 |         8 pixels (1 bit/pixel)        |
 |                                       |
 | "0": Color from bits 0-3 of c-data    |
 | "1": Color from bits 4-7 of c-data    |
 +---------------------------------------+

3.7.3.4. Multicolor bitmap mode (ECM/BMM/MCM=0/1/1)
---------------------------------------------------

Similar to the multicolor text mode, this mode also forms (twice as wide)
pixels by combining two adjacent bits. So the resolution is reduced to
160×200 pixels.

The bit combination "01" is also treated as "background" for the sprite
priority and collision detection, as in multicolor text mode.

c-access

 Addresses

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 |VM13|VM12|VM11|VM10| VC9| VC8| VC7| VC6| VC5| VC4| VC3| VC2| VC1| VC0|
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+

 Data

 +----+----+----+----+----+----+----+----+----+----+----+----+
 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+
 |     Color of      |     Color of      |     Color of      |
 |    "11 pixels"    |    "01" pixels    |    "10" pixels    |
 +-------------------+-------------------+-------------------+

g-access

 Addresses

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 |CB13| VC9| VC8| VC7| VC6| VC5| VC4| VC3| VC2| VC1| VC0| RC2| RC1| RC0|
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+

 Data

 +----+----+----+----+----+----+----+----+
 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+
 |         4 pixels (2 bits/pixel)       |
 |                                       |
 | "00": Background color 0 ($d021)      |
 | "01": Color from bits 4-7 of c-data   |
 | "10": Color from bits 0-3 of c-data   |
 | "11": Color from bits 8-11 of c-data  |
 +---------------------------------------+

3.7.3.5. ECM text mode (ECM/BMM/MCM=1/0/0)
------------------------------------------

This text mode is the same as the standard text mode, but it allows the
selection of one of four background colors for every single character. The
selection is done with the upper two bits of the character pointer. This,
however, reduces the character set from 256 to 64 characters.

c-access

 Addresses

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 |VM13|VM12|VM11|VM10| VC9| VC8| VC7| VC6| VC5| VC4| VC3| VC2| VC1| VC0|
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+

 Data

 +----+----+----+----+----+----+----+----+----+----+----+----+
 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+
 |     Color of      |Back.col.| D5 | D4 | D3 | D2 | D1 | D0 |
 |    "1" pixels     |selection|    |    |    |    |    |    |
 +-------------------+---------+----+----+----+----+----+----+

g-access

 Addresses

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 |CB13|CB12|CB11|  0 |  0 | D5 | D4 | D3 | D2 | D1 | D0 | RC2| RC1| RC0|
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+

 Data

 +----+----+----+----+----+----+----+----+
 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+
 |         8 pixels (1 bit/pixel)        |
 |                                       |
 | "0": Depending on bits 6/7 of c-data  |
 |      00: Background color 0 ($d021)   |
 |      01: Background color 1 ($d022)   |
 |      10: Background color 2 ($d023)   |
 |      11: Background color 3 ($d024)   |
 | "1": Color from bits 8-11 of c-data   |
 +---------------------------------------+

3.7.3.6. Invalid text mode (ECM/BMM/MCM=1/0/1)
----------------------------------------------

Setting the ECM and MCM bits simultaneously doesn't select one of the
"official" graphics modes of the VIC but creates only black pixels.
Nevertheless, the graphics data sequencer internally generates valid
graphics data that can trigger sprite collisions even in this mode. By
using sprite collisions, you can also read out the generated data (but you
cannot see anything, the screen is black). You can, however, only
distinguish foreground and background pixels as you cannot get color
information from sprite collisions.

The generated graphics is similar to that of the multicolor text mode, but
the character set is limited to 64 characters as in ECM mode.

c-access

 Addresses

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 |VM13|VM12|VM11|VM10| VC9| VC8| VC7| VC6| VC5| VC4| VC3| VC2| VC1| VC0|
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+

 Data

 +----+----+----+----+----+----+----+----+----+----+----+----+
 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+
 | MC |         unused         | D5 | D4 | D3 | D2 | D1 | D0 |
 |flag|                        |    |    |    |    |    |    |
 +----+------------------------+----+----+----+----+----+----+

g-access

 Addresses

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 |CB13|CB12|CB11|  0 |  0 | D5 | D4 | D3 | D2 | D1 | D0 | RC2| RC1| RC0|
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+

 Data

 +----+----+----+----+----+----+----+----+
 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+
 |         8 pixels (1 bit/pixel)        |
 |                                       | MC flag = 0
 | "0": Black (background)               |
 | "1": Black (foreground)               |
 +---------------------------------------+
 |         4 pixels (2 bits/pixel)       |
 |                                       |
 | "00": Black (background)              | MC flag = 1
 | "01": Black (background)              |
 | "10": Black (foreground)              |
 | "11": Black (foreground)              |
 +---------------------------------------+

3.7.3.7. Invalid bitmap mode 1 (ECM/BMM/MCM=1/1/0)
--------------------------------------------------

This mode also only displays a black screen, but the pixels can also be
read out with the sprite collision trick.

The structure of the graphics is basically as in standard bitmap mode, but
the bits 9 and 10 of the g-addresses are always zero due to the set ECM bit
and so the graphics is - roughly said - made up of four "sections" that are
each repeated four times.

c-access

 Addresses

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 |VM13|VM12|VM11|VM10| VC9| VC8| VC7| VC6| VC5| VC4| VC3| VC2| VC1| VC0|
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+

 Data

 +----+----+----+----+----+----+----+----+----+----+----+----+
 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+
 |                           unused                          |
 +-----------------------------------------------------------+

g-access

 Addresses

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 |CB13| VC9| VC8|  0 |  0 | VC5| VC4| VC3| VC2| VC1| VC0| RC2| RC1| RC0|
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+

 Data

 +----+----+----+----+----+----+----+----+
 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+
 |         8 pixels (1 bit/pixel)        |
 |                                       |
 | "0": Black (background)               |
 | "1": Black (foreground)               |
 +---------------------------------------+

3.7.3.8. Invalid bitmap mode 2 (ECM/BMM/MCM=1/1/1)
--------------------------------------------------

The last invalid mode also creates a black screen but it can also be
"scanned" with sprite-graphics collisions.

The structure of the graphics is basically as in multicolor bitmap mode,
but the bits 9 and 10 of the g-addresses are always zero due to the set ECM
bit, with the same results as in the first invalid bitmap mode. As usual,
the bit combination "01" is part of the background.

c-access

 Addresses

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 |VM13|VM12|VM11|VM10| VC9| VC8| VC7| VC6| VC5| VC4| VC3| VC2| VC1| VC0|
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+

 Data

 +----+----+----+----+----+----+----+----+----+----+----+----+
 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+
 |                           unused                          |
 +-----------------------------------------------------------+

g-access

 Addresses

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 |CB13| VC9| VC8|  0 |  0 | VC5| VC4| VC3| VC2| VC1| VC0| RC2| RC1| RC0|
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+

 Data

 +----+----+----+----+----+----+----+----+
 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+
 |         4 pixels (2 bits/pixel)       |
 |                                       |
 | "00": Black (background)              |
 | "01": Black (background)              |
 | "10": Black (foreground)              |
 | "11": Black (foreground)              |
 +---------------------------------------+

3.7.3.9. Idle state
-------------------

In idle state, the VIC reads the graphics data from address $3fff (resp.
$39ff if the ECM bit is set) and displays it in the selected graphics mode,
but with the video matrix data (normally read in the c-accesses) being all
"0" bits. So the byte at address $3fff/$39ff is output repeatedly.

c-access

 No c-accesses occur.

 Data

 +----+----+----+----+----+----+----+----+----+----+----+----+
 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+
 |  0 |  0 |  0 |  0 |  0 |  0 |  0 |  0 |  0 |  0 |  0 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+

g-access

 Addresses (ECM=0)

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 |  1 |  1 |  1 |  1 |  1 |  1 |  1 |  1 |  1 |  1 |  1 |  1 |  1 |  1 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+

 Addresses (ECM=1)

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 |  1 |  1 |  1 |  0 |  0 |  1 |  1 |  1 |  1 |  1 |  1 |  1 |  1 |  1 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+

 Data

 +----+----+----+----+----+----+----+----+
 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+
 |         8 pixels (1 bit/pixel)        | Standard text mode/
 |                                       | Multicolor text mode/
 | "0": Background color 0 ($d021)       | ECM text mode
 | "1": Black                            |
 +---------------------------------------+
 |         8 pixels (1 bit/pixel)        | Standard bitmap mode/
 |                                       | Invalid text mode/
 | "0": Black (background)               | Invalid bitmap mode 1
 | "1": Black (foreground)               |
 +---------------------------------------+
 |         4 pixels (2 bits/pixel)       | Multicolor bitmap mode
 |                                       |
 | "00": Background color 0 ($d021)      |
 | "01": Black (background)              |
 | "10": Black (foreground)              |
 | "11": Black (foreground)              |
 +---------------------------------------+
 |         4 pixels (2 bits/pixel)       | Invalid bitmap mode 2
 |                                       |
 | "00": Black (background)              |
 | "01": Black (background)              |
 | "10": Black (foreground)              |
 | "11": Black (foreground)              |
 +---------------------------------------+
