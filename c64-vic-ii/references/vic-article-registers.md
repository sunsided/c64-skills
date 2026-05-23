> Source: vic-ii.txt §3.1–3.3, "Block diagram / Registers / Color palette". By Christian Bauer (28.Aug.1996). Lightly cleaned (Φ clock-signal mojibake restored).

3.1. Block diagram
------------------

The following block diagram gives an overview over the internal structure
of the VIC and the independently working function units:


 IRQ <---------------------------------+
                                       |
            +---------------+ +-----------------+
            |Refresh counter| | Interrupt logic |<----------------------+
            +---------------+ +-----------------+                       |
        +-+    |               ^                                        |
  A     |M|    v               |                                        |
  d     |e|   +-+    +--------------+  +-------+                        |
  d     |m|   |A|    |Raster counter|->| VC/RC |                        |
  r     |o|   |d| +->|      X/Y     |  +-------+                        |
  . <==>|r|   |d| |  +--------------+      |                            |
  +     |y|   |r| |     | | |              |                            |
  d     | |   |.|<--------+----------------+ +------------------------+ |
  a     |i|   |g|===========================>|40×12 bit video matrix-/| |
  t     |n|<=>|e| |     |   |                |       color line       | |
  a     |t|   |n| |     |   |                +------------------------+ |
        |e|   |e| |     |   |                            ||             |
        |r|   |r| |     |   | +----------------+         ||             |
 BA  <--|f|   |a|============>|8×24 bit sprite |         ||             |
        |a|   |t|<----+ |   | |  data buffers  |         ||             |
 AEC <--|c|   |o| |   | v   | +----------------+         ||             |
        |e|   |r| | +-----+ |         ||                 ||             |
        +-+   +-+ | |MC0-7| |         \/                 \/             |
                  | +-----+ |  +--------------+   +--------------+      |
                  |         |  | Sprite data  |   |Graphics data |      |
        +---------------+   |  |  sequencer   |   |  sequencer   |      |
 RAS <--|               |   |  +--------------+   +--------------+      |
 CAS <--|Clock generator|   |              |         |                  |
 Φ0  <--|               |   |              v         v                  |
        +---------------+   |       +-----------------------+           |
                ^           |       |          MUX          |           |
                |           |       | Sprite priorities and |-----------+
 ΦIN -----------+           |       |  collision detection  |
                            |       +-----------------------+
   VC: Video Matrix Counter |                   |
                            |                   v
   RC: Row Counter          |            +-------------+
                            +----------->| Border unit |
   MC: MOB Data Counter     |            +-------------+
                            |                   |
                            v                   v
                    +----------------+  +----------------+
                    |Sync generation |  |Color generation|<-------- ΦCOLOR
                    +----------------+  +----------------+
                                   |      |
                                   v      v
                                 Video output
                               (S/LUM and COLOR)


The lightpen unit is not shown.

As you can see, the "Raster counter X/Y" plays a central role. This is no
surprise as the complete screen display and all bus accesses are
synchronized by it.

It is important to note that the units for display and for the needed
memory accesses are separate from each other for the sprites as well as for
the graphics. There is a data buffer between the two units that holds the
read graphics data and buffers it for the display circuits. In the normal
operation of the VIC, the functions of the two units are so closely tied to
each other that they appear like a single function block. By appropriate
programming, however, you can decouple the circuits and e.g. display
graphics without previously having read data (in this case, the data which
are still in the buffer are displayed).

3.2. Registers
--------------

The VIC has 47 read/write registers for the processor to control its
functions:

 #| Adr.  |Bit7|Bit6|Bit5|Bit4|Bit3|Bit2|Bit1|Bit0| Function
--+-------+----+----+----+----+----+----+----+----+------------------------
 0| $d000 |                  M0X                  | X coordinate sprite 0
--+-------+---------------------------------------+------------------------
 1| $d001 |                  M0Y                  | Y coordinate sprite 0
--+-------+---------------------------------------+------------------------
 2| $d002 |                  M1X                  | X coordinate sprite 1
--+-------+---------------------------------------+------------------------
 3| $d003 |                  M1Y                  | Y coordinate sprite 1
--+-------+---------------------------------------+------------------------
 4| $d004 |                  M2X                  | X coordinate sprite 2
--+-------+---------------------------------------+------------------------
 5| $d005 |                  M2Y                  | Y coordinate sprite 2
--+-------+---------------------------------------+------------------------
 6| $d006 |                  M3X                  | X coordinate sprite 3
--+-------+---------------------------------------+------------------------
 7| $d007 |                  M3Y                  | Y coordinate sprite 3
--+-------+---------------------------------------+------------------------
 8| $d008 |                  M4X                  | X coordinate sprite 4
--+-------+---------------------------------------+------------------------
 9| $d009 |                  M4Y                  | Y coordinate sprite 4
--+-------+---------------------------------------+------------------------
10| $d00a |                  M5X                  | X coordinate sprite 5
--+-------+---------------------------------------+------------------------
11| $d00b |                  M5Y                  | Y coordinate sprite 5
--+-------+---------------------------------------+------------------------
12| $d00c |                  M6X                  | X coordinate sprite 6
--+-------+---------------------------------------+------------------------
13| $d00d |                  M6Y                  | Y coordinate sprite 6
--+-------+---------------------------------------+------------------------
14| $d00e |                  M7X                  | X coordinate sprite 7
--+-------+---------------------------------------+------------------------
15| $d00f |                  M7Y                  | Y coordinate sprite 7
--+-------+----+----+----+----+----+----+----+----+------------------------
16| $d010 |M7X8|M6X8|M5X8|M4X8|M3X8|M2X8|M1X8|M0X8| MSBs of X coordinates
--+-------+----+----+----+----+----+----+----+----+------------------------
17| $d011 |RST8| ECM| BMM| DEN|RSEL|    YSCROLL   | Control register 1
--+-------+----+----+----+----+----+--------------+------------------------
18| $d012 |                 RASTER                | Raster counter
--+-------+---------------------------------------+------------------------
19| $d013 |                  LPX                  | Light pen X
--+-------+---------------------------------------+------------------------
20| $d014 |                  LPY                  | Light pen Y
--+-------+----+----+----+----+----+----+----+----+------------------------
21| $d015 | M7E| M6E| M5E| M4E| M3E| M2E| M1E| M0E| Sprite enabled
--+-------+----+----+----+----+----+----+----+----+------------------------
22| $d016 |  - |  - | RES| MCM|CSEL|    XSCROLL   | Control register 2
--+-------+----+----+----+----+----+----+----+----+------------------------
23| $d017 |M7YE|M6YE|M5YE|M4YE|M3YE|M2YE|M1YE|M0YE| Sprite Y expansion
--+-------+----+----+----+----+----+----+----+----+------------------------
24| $d018 |VM13|VM12|VM11|VM10|CB13|CB12|CB11|  - | Memory pointers
--+-------+----+----+----+----+----+----+----+----+------------------------
25| $d019 | IRQ|  - |  - |  - | ILP|IMMC|IMBC|IRST| Interrupt register
--+-------+----+----+----+----+----+----+----+----+------------------------
26| $d01a |  - |  - |  - |  - | ELP|EMMC|EMBC|ERST| Interrupt enabled
--+-------+----+----+----+----+----+----+----+----+------------------------
27| $d01b |M7DP|M6DP|M5DP|M4DP|M3DP|M2DP|M1DP|M0DP| Sprite data priority
--+-------+----+----+----+----+----+----+----+----+------------------------
28| $d01c |M7MC|M6MC|M5MC|M4MC|M3MC|M2MC|M1MC|M0MC| Sprite multicolor
--+-------+----+----+----+----+----+----+----+----+------------------------
29| $d01d |M7XE|M6XE|M5XE|M4XE|M3XE|M2XE|M1XE|M0XE| Sprite X expansion
--+-------+----+----+----+----+----+----+----+----+------------------------
30| $d01e | M7M| M6M| M5M| M4M| M3M| M2M| M1M| M0M| Sprite-sprite collision
--+-------+----+----+----+----+----+----+----+----+------------------------
31| $d01f | M7D| M6D| M5D| M4D| M3D| M2D| M1D| M0D| Sprite-data collision
--+-------+----+----+----+----+----+----+----+----+------------------------
32| $d020 |  - |  - |  - |  - |         EC        | Border color
--+-------+----+----+----+----+-------------------+------------------------
33| $d021 |  - |  - |  - |  - |        B0C        | Background color 0
--+-------+----+----+----+----+-------------------+------------------------
34| $d022 |  - |  - |  - |  - |        B1C        | Background color 1
--+-------+----+----+----+----+-------------------+------------------------
35| $d023 |  - |  - |  - |  - |        B2C        | Background color 2
--+-------+----+----+----+----+-------------------+------------------------
36| $d024 |  - |  - |  - |  - |        B3C        | Background color 3
--+-------+----+----+----+----+-------------------+------------------------
37| $d025 |  - |  - |  - |  - |        MM0        | Sprite multicolor 0
--+-------+----+----+----+----+-------------------+------------------------
38| $d026 |  - |  - |  - |  - |        MM1        | Sprite multicolor 1
--+-------+----+----+----+----+-------------------+------------------------
39| $d027 |  - |  - |  - |  - |        M0C        | Color sprite 0
--+-------+----+----+----+----+-------------------+------------------------
40| $d028 |  - |  - |  - |  - |        M1C        | Color sprite 1
--+-------+----+----+----+----+-------------------+------------------------
41| $d029 |  - |  - |  - |  - |        M2C        | Color sprite 2
--+-------+----+----+----+----+-------------------+------------------------
42| $d02a |  - |  - |  - |  - |        M3C        | Color sprite 3
--+-------+----+----+----+----+-------------------+------------------------
43| $d02b |  - |  - |  - |  - |        M4C        | Color sprite 4
--+-------+----+----+----+----+-------------------+------------------------
44| $d02c |  - |  - |  - |  - |        M5C        | Color sprite 5
--+-------+----+----+----+----+-------------------+------------------------
45| $d02d |  - |  - |  - |  - |        M6C        | Color sprite 6
--+-------+----+----+----+----+-------------------+------------------------
46| $d02e |  - |  - |  - |  - |        M7C        | Color sprite 7
--+-------+----+----+----+----+-------------------+------------------------

Notes:

 · The bits marked with '-' are not connected and give "1" on reading
 · The VIC registers are repeated each 64 bytes in the area $d000-$d3ff,
   i.e. register 0 appears on addresses $d000, $d040, $d080 etc.
 · The unused addresses $d02f-$d03f give $ff on reading, a write access is
   ignored
 · The registers $d01e and $d01f cannot be written and are automatically
   cleared on reading
 · The RES bit (bit 5) of register $d016 has no function on the VIC
   6567/6569 examined as yet. On the 6566, this bit is used to stop the
   VIC.
 · Bit 7 in register $d011 (RST8) is bit 8 of register $d012. Together they
   are called "RASTER" in the following. A write access to these bits sets
   the comparison line for the raster interrupt (see section 3.12.).

3.3. Color palette
------------------

The VIC has a hard-wired palette of 16 colors that are encoded with 4 bits:

  0 black
  1 white
  2 red
  3 cyan
  4 pink
  5 green
  6 blue
  7 yellow
  8 orange
  9 brown
 10 light red
 11 dark gray
 12 medium gray
 13 light green
 14 light blue
 15 light gray
