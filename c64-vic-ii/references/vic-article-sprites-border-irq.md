> Source: vic-ii.txt §3.8–3.13, "Sprites, the border units, Display Enable, Lightpen, VIC interrupts, DRAM refresh". By Christian Bauer (28.Aug.1996). Lightly cleaned (Φ clock-signal mojibake restored).

3.8. Sprites
------------

Apart from the text/bitmap graphics, the VIC can display eight independent
24×21 pixels large, freely movable objects, the "sprites" (called "MOBs"
(Movable Object Blocks) in [2]).

The sprites can have an arbitrary position on the screen, you can switch
them on and off one at a time with the bits of register $d015 (MxE), expand
them by the factor 2 in X and/or Y direction with registers $d017/$d01d
(with the resolution still being 24×21 pixels), choose between standard and
multicolor mode with register $d01c (MxMC), set the display priority with
respect to the text/bitmap graphics with register $d01b (MxDP) and assign a
different color to each sprite (registers $d027-$d02e). Besides, the VIC
has the ability to detect collisions between sprites among themselves or
between sprites and text/bitmap graphics and to trigger an interrupt on
such collisions (see 3.11.).

The position of the top left corner of a sprite is specified with the
coordinate registers (MxX, MxY) belonging to it. There are 8 bits for the Y
coordinate and 9 bits for the X coordinate (the most significant bits of
all sprites are collected in register $d010).

3.8.1. Memory access and display
--------------------------------

The 63 bytes of sprite data necessary for displaying 24×21 pixels are
stored in memory in a linear fashion: 3 adjacent bytes form one line of the
sprite.

These 63 bytes can be moved in steps of 64 bytes within the 16KB address
space of the VIC. For this, the VIC reads a sprite data pointer for each
sprite in every raster line from the very last 8 bytes of the video matrix
(p-access) that is used as the upper 8 bits of the address for sprite data
accesses (s-accesses). The lower 6 bits come from a sprite data counter
(MC0-MC7, one for each sprite) that plays a similar role for the sprites as
VC does for the video matrix. As the p-accesses are done in every raster
line and not only when the belonging sprite is just displayed, you can
change the appearance of a sprite in the middle of its display by changing
the sprite data pointer.

When s-accesses are necessary for a sprite, they are done in the three
half-cycles directly after the p-access belonging to the sprite within the
raster line. The VIC also uses the BA and AEC signals (as in the Bad Lines)
to access the bus in the second clock phase. BA will also go low three
cycles before the proper access in this case. The s-accesses are done in
every raster line in which the sprite is visible (for the sprites 0-2, it
is always in the line before, see the timing diagrams in section 3.6.3.),
for every sprite in statically assigned cycles within the line.

Like the text and bitmap graphics, the sprites also have a standard mode
and a multicolor mode. In standard mode, every bit directly corresponds to
one pixel on the screen. A "0" pixel is transparent and the underlying
graphics are visible below it, a "1" pixel is displayed in the sprite color
from registers $d027-$d02e belonging to the sprite in question. In
multicolor mode, two adjacent bits form one pixel, thus reducing the
resolution of the sprite to 12×21 (the pixels are twice as wide).

Moreover, the sprites can be doubled in their size on the screen in X
and/or Y direction (X/Y expansion). For that, every sprite pixel simply
becomes twice as wide/tall, the resolution doesn't change. So a pixel of an
x-expanded multicolor sprite is four times as wide as a pixel of an
unexpanded standard sprite. Although both expansions look similar, they are
implemented completely differently in the VIC. The X expansion simply
instructs the sprite data sequencer to output pixels with half frequency.
But the Y expansion makes the sprite address generator read from the same
addresses in each two lines in sequence so that every sprite line is output
twice.

Every sprite has its own sprite data sequencer whose core is a 24 bit shift
register. Apart from that, there are two internal registers for every
sprite:

 · "MC" (MOB Data Counter) is a 6 bit counter that can be loaded from
   MCBASE.
 · "MCBASE" (MOB Data Counter Base) is a 6 bit counter with reset input.

Besides, there is one expansion flip flop per sprite that controls the
Y expansion.

The display of a sprite is done after the following rules (the cycle
numbers are only valid for the 6569):

1. The expansion flip flip is set as long as the bit in MxYE in register
   $d017 corresponding to the sprite is cleared.

2. If the MxYE bit is set in the first phase of cycle 55, the expansion
   flip flop is inverted.

3. In the first phases of cycle 55 and 56, the VIC checks for every sprite
   if the corresponding MxE bit in register $d015 is set and the Y
   coordinate of the sprite (odd registers $d001-$d00f) match the lower 8
   bits of RASTER. If this is the case and the DMA for the sprite is still
   off, the DMA is switched on, MCBASE is cleared, and if the MxYE bit is
   set the expansion flip flip is reset.

4. In the first phase of cycle 58, the MC of every sprite is loaded from
   its belonging MCBASE (MCBASE->MC) and it is checked if the DMA for the
   sprite is turned on and the Y coordinate of the sprite matches the lower
   8 bits of RASTER. If this is the case, the display of the sprite is
   turned on.

5. If the DMA for a sprite is turned on, three s-accesses are done in
   sequence in the corresponding cycles assigned to the sprite (see the
   diagrams in section 3.6.3.). The p-accesses are always done, even if the
   sprite is turned off. The read data of the first access is stored in the
   upper 8 bits of the shift register, that of the second one in the middle
   8 bits and that of the third one in the lower 8 bits. MC is incremented
   by one after each s-access.

6. If the sprite display for a sprite is turned on, the shift register is
   shifted left by one bit with every pixel as soon as the current X
   coordinate of the raster beam matches the X coordinate of the sprite
   (even registers $d000-$d00e), and the bits that "fall off" are
   displayed. If the MxXE bit belonging to the sprite in register $d01d is
   set, the shift is done only every second pixel and the sprite appears
   twice as wide. If the sprite is in multicolor mode, every two adjacent
   bits form one pixel.

7. In the first phase of cycle 15, it is checked if the expansion flip flop
   is set. If so, MCBASE is incremented by 2.

8. In the first phase of cycle 16, it is checked if the expansion flip flop
   is set. If so, MCBASE is incremented by 1. After that, the VIC checks if
   MCBASE is equal to 63 and turns of the DMA and the display of the sprite
   if it is.

As the test in rule 3 is done at the end of a raster line, the sprite Y
coordinates stored in the registers must be 1 less than the desired Y
position of the first sprite line, as the sprite display will not start
until the following line, after the first sprite data has been read (as
long as the sprite is not positioned to the right of sprite X coordinate
$164 (cycle 58, see rule 4)).

Sprites can be "reused" vertically: If you change the Y coordinate of a
sprite to a later raster line during or after its display has completed, so
that the comparisons mentioned in rules 1 and 2 will match again, the
sprite is displayed again at that Y coordinate (you may then of course
freely set a new X coordinate and sprite data pointer). It is therefore
possible to display more than 8 sprites on the screen.

This is not possible in the horizontal direction. After 24 displayed
pixels, the shift register has run empty and even if you change the X
coordinate within a line so that the comparison in rule 4 will match again,
no sprite data is displayed any more. So you can only display up to 8
sprites within one raster line at a time.

Once again an overview of the scheme of p- and s-accesses:

p-access

 Addresses

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 |VM13|VM12|VM11|VM10|  1 |  1 |  1 |  1 |  1 |  1 |  1 |Sprite number |
 +----+----+----+----+----+----+----+----+----+----+----+--------------+

 Data

 +----+----+----+----+----+----+----+----+
 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+
 | MP7| MP6| MP5| MP4| MP3| MP2| MP1| MP0|
 +----+----+----+----+----+----+----+----+

s-access

 Addresses

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | MP7| MP6| MP5| MP4| MP3| MP2| MP1| MP0| MC5| MC4| MC3| MC2| MC1| MC0|
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+

 Data

 +----+----+----+----+----+----+----+----+
 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+
 |         8 pixels (1 bit/pixel)        |
 |                                       | MxMC = 0
 | "0": Transparent                      |
 | "1": Sprite color ($d027-$d02e)       |
 +---------------------------------------+
 |         4 pixels (2 bits/pixel)       |
 |                                       |
 | "00": Transparent                     | MxMC = 1
 | "01": Sprite multicolor 0 ($d025)     |
 | "10": Sprite color ($d027-$d02e)      |
 | "11": Sprite multicolor 1 ($d026)     |
 +---------------------------------------+

3.8.2. Priority and collision detection
---------------------------------------

As soon as several graphics elements (sprites and text/bitmap graphics)
overlap on the screen, it has to be decided which element is displayed in
the foreground. To do this, every element has a priority assigned and only
the element with highest priority is displayed.

The sprites have a rigid hierarchy among themselves: Sprite 0 has the
highest and sprite 7 the lowest priority. If two sprites overlap, the
sprite with the higher number is displayed only where the other sprite has
a transparent pixel.

The priority of the sprites to the text/bitmap graphics can be controlled
within some limits. First of all, you have to distinguish the text/bitmap
graphics between foreground and background pixels. Which bit combinations
belong to the foreground or background is decided by the MCM bit in
register $d016 independently of the state of the graphics data sequencer
and of the BMM and ECM bits in register $d011:

             | MCM=0 |   MCM=1
 ------------+-------+-----------
 Bits/pixel  |   1   |     2
 Pixels/byte |   8   |     4
 Background  |  "0"  | "00", "01"
 Foreground  |  "1"  | "10", "11"

In multicolor mode (MCM=1), the bit combinations "00" and "01" belong to
the background and "10" and "11" to the foreground whereas in standard mode
(MCM=0), cleared pixels belong to the background and set pixels to the
foreground. It should be noted that this is also valid for the graphics
generated in idle state.

With the MxDP bits from register $d01b, you can separately specify for each
sprite if it should be displayed in front of or behind the foreground
pixels (the table in [2] is wrong):

 MxDP=0:

       +-----------------------+
       |  Background graphics  |  low priority
     +-----------------------+ |
     |  Foreground graphics  |-+
   +-----------------------+ |
   |       Sprite x        |-+
 +-----------------------+ |
 |     Screen border     |-+
 |                       |   high priority
 +-----------------------+

 MxDP=1:

       +-----------------------+
       |  Background graphics  |  low priority
     +-----------------------+ |
     |       Sprite x        |-+
   +-----------------------+ |
   |  Foreground graphics  |-+
 +-----------------------+ |
 |     Screen border     |-+
 |                       |   high priority
 +-----------------------+

Of course, the graphics elements with lower priority than an overlayed
sprite are visible where the sprite has a transparent pixel.

If you choose one of the invalid video modes only the sprites will be
visible (fore- and background graphics will all become black, see sections
3.7.3.6.-3.7.3.8.), but by setting the sprites to appear behind the
foreground graphics, the foreground graphics will actually become visible
as black pixels overlaying the sprite pixels.

Together with the priority management, the VIC has the ability to detect
collisions of sprites among themselves and of sprites and foreground pixels
of the text/bitmap graphics.

A collision of sprites among themselves is detected as soon as two or more
sprite data sequencers output a non-transparent pixel in the course of
display generation (this can also happen somewhere outside of the visible
screen area). In this case, the MxM bits of all affected sprites are set in
register $d01e and (if allowed, see section 3.12.), an interrupt is
generated. The bits remain set until the register is read by the processor
and are cleared automatically by the read access.

A collision of sprites and other graphics data is detected as soon as one
or more sprite data sequencers output a non-transparent pixel and the
graphics data sequencer outputs a foreground pixel in the course of display
generation. In this case, the MxD bits of the affected sprites are set in
register $d01f and (if allowed, see section 3.12.), an interrupt is
generated. As with the sprite-sprite collision, the bits remain set until
the register is read by the processor.

If the vertical border flip flop is set (normally within the upper/lower
border, see next section), the output of the graphics data sequencer is
turned off and there are no collisions.

3.9. The border unit
--------------------

The VIC uses two flip flops to generate the border around the display
window: A main border flip flop and a vertical border flip flop.

The main border flip flop controls the border display. If it is set, the
VIC displays the color stored in register $d020, otherwise it displays the
color that the priority multiplexer switches through from the graphics or
sprite data sequencer. So the border overlays the text/bitmap graphics as
well as the sprites. It has the highest display priority.

The vertical border flip flop is for auxiliary control of the upper/lower
border. If it is set, the main border flip flop cannot be reset. Apart from
that, the vertical border flip flop controls the output of the graphics
data sequencer. The sequencer only outputs data if the flip flop is
not set, otherwise it displays the background color. This was probably done
to prevent sprite-graphics collisions in the border area.

There are 2×2 comparators belonging to each of the two flip flops. There
comparators compare the X/Y position of the raster beam with one of two
hardwired values (depending on the state of the CSEL/RSEL bits) to control
the flip flops. The comparisons only match if the values are reached
precisely. There is no comparison with an interval.

The horizontal comparison values:

       |   CSEL=0   |   CSEL=1
 ------+------------+-----------
 Left  |  31 ($1f)  |  24 ($18)
 Right | 335 ($14f) | 344 ($158)

And the vertical ones:

        |   RSEL=0  |  RSEL=1
 -------+-----------+----------
 Top    |  55 ($37) |  51 ($33)
 Bottom | 247 ($f7) | 251 ($fb)

The flip flops are switched according to the following rules:

1. If the X coordinate reaches the right comparison value, the main border
   flip flop is set.
2. If the Y coordinate reaches the bottom comparison value in cycle 63, the
   vertical border flip flop is set.
3. If the Y coordinate reaches the top comparison value in cycle 63 and the
   DEN bit in register $d011 is set, the vertical border flip flop is
   reset.
4. If the X coordinate reaches the left comparison value and the Y
   coordinate reaches the bottom one, the vertical border flip flop is set.
5. If the X coordinate reaches the left comparison value and the Y
   coordinate reaches the top one and the DEN bit in register $d011 is set,
   the vertical border flip flop is reset.
6. If the X coordinate reaches the left comparison value and the vertical
   border flip flop is not set, the main flip flop is reset.

So the Y coordinate is checked once or twice within each raster line: In
cycle 63 and if the X coordinate reaches the left comparison value.

By appropriate switching of the CSEL/RSEL bits you can prevent the
comparison values from being reached and thus turn off the border partly or
completely (see 3.14.1.).

3.10. Display Enable
--------------------

The DEN bit (Display Enable, register $d011, bit 4) serves for switching on
and off the text/bitmap graphics. It is normally set. The bit affects two
functions of the VIC: The Bad Lines and the vertical border unit.

 - A Bad Line Condition can only occur if the DEN bit has been set for at
   least one cycle somewhere in raster line $30 (see section 3.5.).
 - If the DEN bit is cleared, the reset input of the vertical border flip
   flop is deactivated (see section 3.9.). Then the upper/lower border is
   not turned off.

So clearing the DEN bit will normally prevent Bad Lines (and thus c- and
g-accesses) from occuring and make the whole screen display the border
color.

3.11. Lightpen
--------------

On a negative edge on the LP input, the current position of the raster beam
is latched in the registers LPX ($d013) and LPY ($d014). LPX contains the
upper 8 bits (of 9) of the X position and LPY the lower 8 bits (likewise of
9) of the Y position. So the horizontal resolution of the light pen is
limited to 2 pixels.

Only one negative edge on LP is recognized per frame. If multiple edges
occur on LP, all following ones are ignored. The trigger is not released
until the next vertical blanking interval.

As the LP input of the VIC is connected to the keyboard matrix as are all
lines of the joystick ports, it can also be controlled by software. This is
done with bit 4 of port B of CIA A ($dc01/$dc03). This allows to determine
the current X position of the raster beam by triggering an LP edge and
reading from LPX afterwards (the VIC has no register that would allow
reading the X position directly). This can e.g. be used to synchronize
raster interrupt routines on exact cycles.

The values you get from the LPX register can be calculated from the sprite
coordinates of the timing diagrams in section 3.6.3. The reference point is
the end of the cycle in which the LP line is triggered. E.g. if you trigger
LP in cycle 20, you get the value $1e in LPX, corresponding to the sprite
coordinate $03c (LPX contains the upper 8 bits of the 9 bit X coordinate).

The VIC can also additionally trigger an interrupt on a negative edge on
the LP pin (see next section), likewise only once per frame.

3.12. VIC interrupts
--------------------

The VIC has the possibility to generate interrupts for the processor when
certain events occur. This is done with the IRQ output that is directly
connected to the IRQ input of the 6510. The VIC interrupts are therefore
maskable with the I flag in the processor status register.

There are four interrupt sources in the VIC. Every source has a
corresponding bit in the interrupt latch (register $d019) and a bit in the
interrupt enable register ($d01a). When an interrupts occurs, the
corresponding bit in the latch is set. To clear it, the processor has to
write a "1" there "by hand". The VIC doesn't clear the latch on its own.

If at least one latch bit and the belonging bit in the enable register is
set, the IRQ line is held low and so the interrupt is triggered in the
processor. So the four interrupt sources can be independently enabled and
disabled with the enable bits. As the VIC - as described - doesn't clear
the interrupt latch by itself, the processor has to do it before the I
flag is cleared resp. before the processor returns from the interrupt
routine. Otherwise the interrupt will be triggered again immediately (the
IRQ input of the 6510 is state-sensitive).

The following table describes the four interrupt sources and their bits in
the latch and enable registers:

 Bit|Name| Trigger condition
 ---+----+-----------------------------------------------------------------
  0 | RST| Reaching a certain raster line. The line is specified by writing
    |    | to register $d012 and bit 7 of $d011 and internally stored by
    |    | the VIC for the raster compare. The test for reaching the
    |    | interrupt raster line is done in cycle 0 of every line (for line
    |    | 0, in cycle 1).
  1 | MBC| Collision of at least one sprite with the text/bitmap graphics
    |    | (one sprite data sequencer outputs non-transparent pixel at the
    |    | same time at which the graphics data sequencer outputs a
    |    | foreground pixel)
  2 | MMC| Collision of two or more sprites (two sprite data sequencers
    |    | output a non-transparent pixel at the same time)
  3 | LP | Negative edge on the LP input (lightpen)

For the MBC and MMC interrupts, only the first collision will trigger an
interrupt (i.e. if the collision registers $d01e resp. $d01f contained the
value zero before the collision). To trigger further interrupts after a
collision, the concerning register has to be cleared first by reading from
it.

The bit 7 in the latch $d019 reflects the inverted state of the IRQ output
of the VIC.

3.13. DRAM refresh
------------------

The VIC does five read accesses in every raster line for the refresh of the
dynamic RAM. An 8 bit refresh counter (REF) is used to generate 256 DRAM
row addresses. The counter is reset to $ff in raster line 0 and decremented
by 1 after each refresh access.

So the VIC will access addresses $3fff, $3ffe, $3ffd, $3ffc and $3ffb in
line 0, addresses $3ffa, $3ff9, $3ff8, $3ff7 and $3ff6 in line 1 etc.

 Refresh addresses

 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
 |  1 |  1 |  1 |  1 |  1 |  1 |REF7|REF6|REF5|REF4|REF3|REF2|REF1|REF0|
 +----+----+----+----+----+----+----+----+----+----+----+----+----+----+
