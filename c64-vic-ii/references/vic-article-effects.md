> Source: vic-ii.txt §3.14 + §4 + appendices, "Effects/applications (Hyperscreen, FLD, FLI, Linecrunch, doubled text lines, DMA delay, sprite stretching), the addresses 0/1 and the $de00 area, bibliography". By Christian Bauer (28.Aug.1996). Lightly cleaned (Φ clock-signal mojibake restored).

3.14. Effects/applications
--------------------------

The following sections will describe some graphical effects that can be
achieved by applying the rules and mechanisms of the VIC described in the
previous sections.

3.14.1. Hyperscreen
-------------------

As explained in section 3.9., the VIC generates the screen border by
comparing the beam coordinates with start and stop positions selected by
the CSEL/RSEL bits. So the border is basically not displayed within a
certain range of coordinates, but rather turned on and off at certain
coordinates. If you now make sure by appropriately switching CSEL/RSEL that
the coordinate comparison never matches, the border is e.g. never turned on
and you can see the graphics in the border area that is normally covered by
the border. The technique is called "hyperscreen" or "opening the border".

However, the graphics displayable in the border area is mainly limited to
sprites, as the graphics data sequencer is in idle state in this area as no
Bad Lines can occur outside of Y coordinates $30-$f7 (see section 3.5.).
But you can also do something sensible with the graphics generated in idle
state.

To turn off the upper/lower border, you proceed as follows:

1. Somewhere in the upper part of the screen, you switch to 25-line-border
   by setting the RSEL bit.
2. Now you wait until RASTER has reached a value in the range of 248-250.
   The vertical border flip flop is still cleared as the comparison value
   for RSEL=1 is raster line 251.
3. Then you clear the RSEL bit. The comparator is switched and now sets the
   vertical flip flop at line 247. But this line is already passed and thus
   the VIC "forgets" to turn on the vertical border.
4. After raster line 251 you set the RSEL bit again and repeat from step 2.

If you open the upper/lower border with this method, the left/right border
still remains active in the "opened up" area. If you switch from RSEL=0 to
RSEL=1 in the raster line range 52-54, the border is never turned off and
covers the whole screen (this is the same when the DEN bit is cleared, but
Bad Lines still occur). But this is not very sensible.

The left/right border can be turned of with the CSEL bit in a similar way.
However, the timing is much more critical. Whereas for the vertical border,
you have 4 raster lines time for the switch, for the horizontal border the
change from CSEL=1 to CSEL=0 has to be exactly in cycle 56. Likewise the
horizontal border can be prevented from turning off by switching from
CSEL=0 to CSEL=1 in cycle 17.

If you want to open the left/right border in the upper/lower border area,
you must either start with it before the vertical border flip flop is set
(i.e. outside of the upper/lower border), or also open the upper/lower
border, because the main border flip flop can only be reset if the vertical
flip flop is not set. If you compare both methods, you can verify that the
vertical flip flop controls the graphics data sequencer output: With the
first method, only the background color is visible in the opened up
upper/lower border area, whereas the second method displays the idle state
graphics there.

3.14.2. FLD
-----------

When building the graphics out of text lines, the VIC orientates itself
exclusively by the occurrence of Bad Lines: A Bad Line gives the "start
signal" for the display of one text line. By appropriately changing YSCROLL
(in register $d011) you can suppress and arbitrarily delay the Bad Line
Condition (see 3.5.). So you can exactly control in which raster lines Bad
Lines should occur and thus from which raster lines the VIC should start to
display one text line each. The distance between two text lines can be
arbitrarily increased if only you hold back the next Bad Line long enough.
This effect is called "Flexible Line Distance" (FLD).

E.g. if you only allow three Bad Lines on the screen at raster lines $50,
$78 and $a0, the VIC will also only display three text lines at these
positions. The sequencer is in idle state in the lines between.

If you only delay the occurrence of the first Bad Line, you can scroll down
the complete graphics display by large distances without moving a single
byte in display memory.

3.14.3. FLI
-----------

Instead of delaying the occurrence of Bad Lines as for the FLD effect, you
may also artificially create additional Bad Lines before the VIC has
completed the current text line. This is especially interesting for the
bitmap modes, as these use the data from the video matrix (which is read in
the Bad Lines) for color information, so normally only single 8×8 pixel
blocks can be colored individually in bitmap modes. But if you make every
raster line a Bad Line by appropriately modifying YSCROLL, the VIC will
read from the video matrix in every line and so it will also read new color
information for every line.

This way, each of the 4×8 pixels of a block in multicolor mode can have a
different color. This software-generated new graphics mode is called
"Flexible Line Interpretation" (FLI) and is probably the most outstanding
example of "unconventional" VIC programming.

There is however one problem: If you create a new Bad Line before the
current text line has been finished, VCBASE is not incremented (see
3.7.2.). So the VIC reads from the same addresses in the video matrix as in
the previous line. As you cannot change the video matrix fast enough with
the processor, you have to switch the base address of the video matrix with
the bits VM10-VM13 of register $d018 (unfortunately the Color RAM cannot be
switched, so the color selection of the pixels is not completely free).

Besides, the access to $d011 to create the Bad Line may not happen until
cycle 14 of each raster line, or else the RC would be cleared in every line
and the bitmap display would not be as desired. But this also implies that
the first three c-accesses of the VIC in each line do not read valid data,
because the first c-access in cycle 15 requires that BA should already have
gone low in cycle 12 so that AEC can stay low in cycle 15 (AEC doesn't stay
low until three cycles after the negative edge of BA, there is no way
around that). But as the Bad Line was first created in cycle 14, it's true
that BA is low in cycle 15 on the first c-access, but AEC is high and so
the internal data bus drivers D0-D7 of the VIC are closed and as the chip
is manufactured in NMOS technology, it reads the value $ff and not the
video matrix data (the data bus drivers D8-D11 are indeed open, but this is
explained in section 3.14.6. in more detail) which is visible as 24 pixel
wide stripes on the left side of the screen.

Practically you store eight video matrices in memory that are used in the
following way: In the first raster line the first line of the first matrix,
in the second line the first line of the second matrix, etc..., in the
eighth line the first line of the eighth matrix, in the ninth line the
second line of the first matrix, etc. With these eight matrices you can
line-wise cover a complete bitmap.

There are several flavors of the FLI mode, such as AFLI (Advanced FLI)
which uses the standard bitmap mode and simulates color blends by similarly
colored adjacent pixels, and IFLI (Interlaced FLI) that alternates between
two frames in a sort of interlace mode.

3.14.4. Linecrunch
------------------

By manipulating YSCROLL, you have even more possibilities to control the
Bad Lines. You may also abort a Bad Line before its correct completion by
negating the Bad Line Condition within an already begun Bad Line before
cycle 14. This his several consequences:

 - The graphics data is in display state, so graphics are displayed.
 - The RC is not reset. If you abort the very first line of a frame this
   way, the RC is still at 7 from the last line of the previous frame.
 - In cycle 58 of the line the RC is still 7, so the sequencer goes to idle
   state and VCBASE is loaded from VC. But as the sequencer has been in
   display state within the line, VC has been incremented after every
   g-access, so VCBASE has now been effectively increased by 40. The RC
   doesn't overflow, it stays at 7.

With this procedure you have reduced the display of a text line to its last
raster line, because as VCBASE has been incremented by 40, the VIC
continues with the next line. This effect if therefore called "Linecrunch":
You can "crunch" single text lines with it.

If you now do this in every raster line, the RC will always stay at 7 and
there will be no c-accesses, but VCBASE is incremented by 40 in every line.
This eventually makes VCBASE cross the 1000 byte limit of the video matrix
and the VIC displays the last, normally invisible, 24 bytes of the matrix
(where also the sprite data pointers are stored). VCBASE wraps around to
zero when reaching 1024.

By crunching whole text lines to one raster line each you have the
possibility to quickly scroll the screen contents up by large distances
without moving bytes in the graphics memory, in a similar way as you can
scroll it down with FLD. The only disturbing side effect is that the
crunched lines pile up at the upper screen border, looking awkward. But
here you can use one of the invalid graphics modes to blank out these
lines.

3.14.5. Doubled text lines
--------------------------

The display of a text line is normally finished after 8 raster lines,
because then RC=7 and in cycle 58 of the last line the sequencer goes to
idle state (see section 3.7.2.). But if you now assert a Bad Line Condition
between cycles 54-57 of the last line, the sequencer stays in display state
and the RC is incremented again (and thus overflows to zero). The VIC will
then in the next line start again with the display of the previous text
line. But as no new video matrix data has been read, the previous text line
is simply displayed twice.

3.14.6. DMA delay
-----------------

The most sophisticated Bad Line manipulation is to create a Bad Line
Condition within cycles 15-53 of a raster line in the display window in
which the graphics data sequencer is in idle state, e.g. by modifying
register $d011 so that YSCROLL is equal to the lower three bits of RASTER.

The VIC will then set BA to low immediately in the next cycle, switch to
display state and start reading from the video matrix (the processor is now
stopped because BA is low and it wants to read the next opcode). However,
AEC still follows Φ2 for three cycles before also staying at low state.
This behavior (AEC not until three cycles after BA) is hardwired in the VIC
and cannot be avoided.

Nevertheless, the VIC accesses the video matrix, or at least it tries,
because as long as AEC is still high in the second clock phase, the address
and data bus drivers D0-D7 of the VIC are in tri-state and the VIC reads
the value $ff from D0-D7 instead of the data from the video matrix in the
first three cycles. The data lines D8-D13 of the VIC however don't have
tri-state drivers and are always set to input. But the VIC doesn't get
valid Color RAM data from there either, because as AEC is high, the 6510 is
still considered the bus master and unless it doesn't by chance want to
read the next opcode from the Color RAM, the chip select input of the Color
RAM is not active. Instead, a 4 bit analog (!) switch, U16, connects the
data bits D0-D3 of the processor with the data bits D8-D13. This connection
is always in place when AEC is high and should allow the processor to
access the Color RAM if desired. To make a long story short: In the first
three cycles after BA went low, the VIC reads $ff as character pointers and
as color information the lower 4 bits of the opcode after the access to
$d011. Not until then, regular video matrix data is read.

These data are stored just as usual at the start of the internal video
matrix/color line and VC is incremented after each following g-access (with
the generation of the Bad Line, the sequencer has also been put into
display state). The c- and g-accesses are continued until cycle 54. But as
the accesses started in the middle of a line, less than 40 accesses took
place so VC has been incremented by a total of less than 40 in this raster
line and no longer is a multiple of 40 as it normally always is at the end
of a raster line. Because of the working of VC (see section 3.7.2.), this
"misalignment" is continued for all following lines. So the whole screen
seems to be scrolled to the right by as much characters as the number of
cycles the $d011 access was done after cycle 14. As the c-accesses within
the line start later than in a normal Bad Line, this procedure is called
"DMA Delay".

With this, it is possible to scroll the complete screen sideways by large
distances (this also works with bitmap graphics as with text screens as the
VC is also used for accessing the bitmap data) without having to move the
graphics memory with the processor. If you now combine DMA Delay with FLD
and Linecrunch, you can scroll complete graphics screens without using much
computing time by almost arbitrarily large distances in all directions.

Experimenting with the DMA Delay (and with Bad Line effects in general) is
also the best method to discover the internal functions of the VIC,
especially of RC and VC, and to determine in which cycles certain things
are done inside the VIC.

It should also be mentioned that DMA Delay can not only be achieved by
manipulating YSCROLL but also with the DEN bit of register $d011. To do
this, you have to set YSCROLL to zero so that raster line $30 becomes a bad
line and switch DEN from reset to set in the middle of the line. This is
because Bad Line can only occur if the DEN bit has been set for at least
one cycle in line $30, and if YSCROLL is zero a Bad Line Condition will
occur in line $30 as soon as DEN is set.

3.14.7 Sprite stretching
------------------------

As the sprite circuitry is simpler than that for the text graphics, there
are not as many special effects possible with sprites, but among them is a
very interesting effect that takes advantage of the way the sprite Y
expansion works: By modifying the MxYE bits in register $d017 it is not
only possible to decide for every single sprite line if it should be
doubled, but you can also have single lines repeated three or more times
and so expand a sprite by arbitrary scaling factors.

This effect can be understood as follows (see section 3.8.1.):

Let's say that we are in cycle 55 of a raster line in which sprite 0 is
turned on and whose Y coordinate matches the Y coordinate of the sprite,
so we are in the line before the sprite is displayed. Suppose that the M0YE
bit is set. The VIC will then turn on the DMA for sprite 0 and clear MCBASE
and the expansion flip flop. BA goes to low state so that the VIC is able
to access in the second clock phases of cycles 58 and 59. In cycle 58, MC
is loaded from MCBASE and so cleared as well, and the p-access for the
sprite is done. Afterwards, the three s-accesses are carried out and MC is
incremented after each access so it now has the value 3.

Now you wait for cycle 16 of the following line. As the expansion flip flop
is reset, MCBASE still stays at zero. Then you first clear the M0YE bit and
thereby set the flip flop, but immediately set the M0YE again. The flip
flop is now inverted in cycle 55, because M0YE is set, and is thus reset
again (if the M0YE hadn't been cleared, the flip flop would now be set).
But this is exactly the same state in which the VIC was also in cycle 55 of
the previous line. So the VIC "thinks" that it is still in the first raster
line of an expanded sprite line and (as MC is still zero) and it will read
the first sprite line twice more from memory, three times in total: The
first sprite line has been tripled.

Another interesting effect can be achieved by proceeding exactly as
outlines above and not clearing the M0YE bit after cycle 16 but in the
second phase of cycle 15. MCBASE will then only be incremented by 1 and the
next sprite line is read from memory with MC=1..3, that is one byte higher
than normal. This "misalignment" is continued in the complete display of
the sprite. Therefore, the condition MC=63 for turning off the sprite DMA
in cycle 16 is also not met and the sprite is effectively displayed twice
in sequence. Not until the end of the second display, the DMA is turned off
when MC is 63.


4. The addresses 0 and 1 and the $de00 area
-------------------------------------------

The address range $de00-$dfff of the 6510 (see 2.4.1.) is reserved for
external expansions of the C64 and normally not connected with any other
unit (RAM, I/O). A read access will fetch data that looks random at first
sight. The same is true for the upper nybbles of the addresses $d800-$dbff
(the Color RAM).

But on some C64, this data is not "random" at all but rather identical to
the data that the VIC has read from memory in the first phase of the clock
cycle. This effect is however not reproducible on all machines and not
always precisely.

Apart from the fact that this gives the possibility to measure the VIC
timing completely by software (the timing diagrams in [4] on which the
diagrams in this article are based, have e.g. been created with this
method), you can also make the 6510 execute programs in the $de00-area or
in the Color RAM if the VIC displays a graphics in such a way that the 6510
gets valid opcodes from the graphics data read by the VIC.

With a similar effect you can also write to RAM addresses 0 and 1 from the
processor. They are normally not available as the internal data direction
register and data register of the 6510 I/O port are mapped to these
addresses, and the data bus drivers stay in tri-state on a write access.
But the R/W line is set to low state (this can be explained as the I/O port
has been integrated afterwards into the existing design of the 6502) and so
the byte read by the VIC in the first clock phase is written to RAM. If you
want to write a certain value to addresses 0 or 1 you only have to write an
arbitrary value to these addresses and take care that the VIC read the
desired value from RAM in the clock phase before.

The addresses 0 and 1 can of course also be read by the processor. Either
with via the $de00-area of with the aid of sprite collisions. For this, you
make the VIC display a bitmap starting at address 0 and move a sprite
consisting only of one pixel over the single bits of the first two bytes of
the bitmap. Depending on whether a collision has been detected or not, you
can find out the state of the single bits and put them together to one
byte.


Appendix A: Bibliography
------------------------

[1] Commodore Business Machines, "C64 Programmers Reference Guide",
    Appendix L: "6510 microprocessor data sheet", 1984

[2] dto., Appendix N: "6566/6567 Video Interface Controller (VIC-II) Chip
    Specifications"

[3] dto., Chapter 5, Section "Memory management on the Commodore 64"

[4] Marko Mäkelä, "The memory accesses of the MOS 6569 VIC-II and MOS 8566
    VIC-IIe Video Interface Controller" (AKA: Pal timing), 15.07.1994

[5] John West, Marko Mäkelä, "Documentation for the NMOS 65xx/85xx
    Instruction Set" (AKA: 64doc), 03.06.1994


Appendix B: Acknowledgments
---------------------------

I want to thank

 - Marko Mäkelä, Andreas Boose, Pasi Ojala and Wolfgang Lorenz for the
   amount of work they put into the examination of the VIC
 - Kaspar Jensen for proof-reading the English version of this document and
   for his suggestions
 - Adam Vardy <abe0084@InfoNET.st-johns.nf.ca> for pointing out that my
   description of idle state graphics display was wrong
