> Source: vic-ii.txt §2, "The architecture of the Commodore 64" (overview, 6510, VIC-II chip, memory maps, memory access). By Christian Bauer (28.Aug.1996). Lightly cleaned (Φ clock-signal mojibake restored).

2. The architecture of the Commodore 64
---------------------------------------

This chapter gives an overview of the basic hardware architecture of the
C64 and the integration of the VIC into the system.

2.1. Overview
-------------

The C64 basically consists of the following units:

 · 6510 8 bit microprocessor
 · 6567/6569 VIC-II graphics chip
 · 6581 SID sound chip
 · Two 6526 CIA I/O chips
 · 64KB DRAM (64K*8 bit) main memory
 · 0.5KB SRAM (1K*4 bit) Color RAM
 · 16KB ROM (16K*8 bit) for operating system and BASIC interpreter
 · 4KB ROM (4K*8 bit) character generator

Most chips are manufactured in NMOS technology.

2.2. 6510 processor
-------------------

The 6510 microprocessor [1] has an 8 bit data bus and a 16 bit address bus
and is object code compatible with the famous 6502. It has two external
interrupt inputs (one maskable (IRQ) and one non-maskable (NMI)) and as a
special feature a 6 bit wide bidirectional I/O port. It is clocked at 1MHz
in the C64.

Important signals:

Φ2     Processor clock output
       This clock signal is the reference for the complete bus timing. Its
       frequency is 1022.7 kHz (NTSC models) or 985.248 kHz (PAL models).
       One period of this signal corresponds to one clock cycle consisting
       of two phases: Φ2 is low in the first phase and high in the second
       phase (hence the name 'Φ2' for "phase 2"). The 6510 only accesses
       the bus in the second clock phase, the VIC normally only in the
       first phase.

R/W    This signal flags a read (R/W high) or write (R/W low) access.

IRQ    If this input is held on low level, an interrupt sequence is
       triggered unless interrupts are masked with the interrupt mask bit
       in the status register. The interrupt sequence begins after two
       or more clock cycles at the start of the next instruction. With this
       pin, the VIC can trigger an interrupt in the processor. Interrupts
       are only recognized if the RDY line is high.

RDY    If this line is low during a read access, the processor stops with
       the address lines reflecting the current address being fetched. It
       is ignored during write accesses. In the C64, RDY is used to stop
       the processor if the VIC needs additional bus cycles for character
       pointer and sprite data accesses. It is connected to the BA signal
       on the VIC.

AEC    This pin tri-states the address lines. This is used for making the
       processor address bus inactive during VIC accesses. The signal is
       connected to the AEC output on the VIC.

P0-P5  This is the built-in 6 bit I/O port. Each line can be individually
       programmed as input or output. A data direction register and a data
       register are internally mapped to addresses 0 and 1, respectively.
       You may therefore expect that the processor cannot access the RAM
       addresses 0 and 1 (as they are overlayed by the I/O port), but more
       on this later...

2.3. 6567/6569 graphics chip
----------------------------

The 656* series graphics chip by MOS Technologies were originally designed
to be used in video games and graphics terminals. But as the sales in these
markets have been rather poor, Commodore decided to use the chips when they
were planning to make their own home computers.

In the C64, the "Video Interface Controller II (VIC-II)" [2] has been used,
featuring 3 text based (40x25 characters with 8x8 pixels each) and 2 bitmap
based (320x200 pixels) video modes, 8 hardware sprites and a fixed palette
of 16 colors. It can manage up to 16KB of dynamic RAM (including the
generation of RAS and CAS and the RAM refresh) and also has a light pen
input and interrupt possibilities.

Two VIC types appear in the C64: The 6567 in NTSC machines and the 6569 in
PAL machines. There are several mask steppings of both types, but the
differences are mostly neglectable with the exception of the 6567R56A.
Newer C64 versions are bearing the functionally equivalent chips 8562
(NTSC) and 8565 (PAL). In the following, only 6567/6569 will be mentioned,
but all statements are applicable for the 856* chips. There is also a 6566
designed to be connected to static RAM but this one was never used in C64s.

Important signals:

A0-A13  The 14 bit video address bus used by the VIC to address 16KB of
        memory. The address bits A0-A5 and A8-A13 are multiplexed in pairs
        (i.e. A0/A8, A1/A9 etc.) on one pin each. The bits A6-A11 are
        (additionally) available on separate lines.

D0-D11  A 12 bit wide data bus over which the VIC accesses the memory. The
        lower 8 bits are connected to the main memory and the processor
        data bus, the upper 4 bits are connected to a special 4 bit wide
        static memory (1024 addresses, A0-A9) used for storing color
        information, the Color RAM.

IRQ     This output is wired to the IRQ input on the processor and makes it
        possible for the VIC to trigger interrupts. The VIC has four
        interrupt sources: On reaching a certain raster line (raster
        interrupt), on the collision of two or more sprites, on the
        collision of sprites with graphics data and on a negative edge on
        the light pen input.

BA      With this signal, the VIC indicated that the bus is available to
        the processor during the second clock phase (Φ2 high). BA is
        normally high as the VIC accesses the bus mostly during the first
        phase. But for the character pointer and sprite data accesses, the
        VIC also needs the bus sometimes during the second phase. In this
        case, BA goes low three cycles before the VIC access. After that,
        AEC remains low during the second phase and the VIC performs the
        accesses. Why three cycles? BA is connected to the RDY line of the
        processor as mentioned, but this line is ignored on write accesses
        (the CPU can only be interrupted on reads), and the 6510 never does
        more than three writes in sequence (see [5]).

AEC     This pin is wired to the processor signal with the same name (see
        there). It reflects the state of the data and address line drivers
        of the VIC. If AEC is high, they are in tri-state. AEC is normally
        low during the first clock phase (Φ2 low) and high during the
        second phase so that the VIC can access the bus during the first
        phase and the 6510 during the second phase. If the VIC also needs
        the bus in the second phase, AEC remains low.

LP      This input is intended for connecting a light pen. On a negative
        edge, the current position of the raster beam is latched to the
        registers LPX and LPY. As this pin shares a line with the keyboard
        matrix, it can also be accessed by software.

ΦIN     This is the feed for the pixel clock of 8.18 MHz (NTSC) or 7.88 MHz
        (PAL) that is generated from the crystal frequency. Eight pixels
        are displayed per bus clock cycle (Φ2).

Φ0      From the pixel clock on ΦIN, the VIC generates the system clock of
        1.023 MHz (NTSC) or 0.985 MHz (PAL) by dividing ΦIN by eight. It is
        available on this pin and fed into the processor which in turn
        generated the signal Φ2 from it.

2.4. Memory
-----------

Three memory areas in the C64 are involved with the graphics:

 · The 64KB main memory
 · The 1K*4 bit Color RAM
 · The 4KB character generator ROM (Char ROM)

In the following two sections it is explained how these memory areas share
the address space as seen by the CPU and the VIC. After that, the basics of
memory access and DRAM handling are mentioned.

2.4.1 Memory map as seen by the 6510
------------------------------------

The 6510 can address 64KB linearly with its 16 address lines. With the aid
of a special PAL chip in the C64, many different memory configurations can
be used via the 6510 I/O port lines and control lines on the expansion
port (see [3]). Only the standard configuration will be discussed here as
the other configurations don't change the position of the different areas.
They only map in additional areas of the main memory.

So this is the memory map as seen by the 6510:


                               The area at $d000-$dfff with
                                  CHAREN=1     CHAREN=0

 $ffff +--------------+  /$e000 +----------+  +----------+
       |  Kernal ROM  | /       |  I/O  2  |  |          |
 $e000 +--------------+/  $df00 +----------+  |          |
       |I/O, Char ROM |         |  I/O  1  |  |          |
 $d000 +--------------+\  $de00 +----------+  |          |
       |     RAM      | \       |  CIA  2  |  |          |
 $c000 +--------------+  \$dd00 +----------+  |          |
       |  Basic ROM   |         |  CIA  1  |  |          |
 $a000 +--------------+   $dc00 +----------+  | Char ROM |
       |              |         |Color RAM |  |          |
       .     RAM      .         |          |  |          |
       .              .   $d800 +----------+  |          |
       |              |         |   SID    |  |          |
 $0002 +--------------+         |registers |  |          |
       | I/O port DR  |   $d400 +----------+  |          |
 $0001 +--------------+         |   VIC    |  |          |
       | I/O port DDR |         |registers |  |          |
 $0000 +--------------+   $d000 +----------+  +----------+


Basically, the 64KB main memory can be accessed in a linear fashion, but
they are overlaid by ROM and register areas at several positions. A write
access to a ROM area will store the byte in the RAM lying "under" the ROM.
The 6510 I/O port is mapped to addresses $0000 (for the data direction
register) and $0001 (for the data register).

In the area at $d000-$dfff you can switch between the I/O chip registers
and the Color RAM, or the character generator ROM, with the signal CHAREN
(which is bit 2 of the 6510 I/O port). The Color RAM is mapped at
$d800-$dbff and connected to the lower 4 data bits. The upper 4 bits are
open and have "random" values on reading. The two areas named "I/O 1" and
"I/O 2" are reserved for expansion cards and also open under normal
circumstances. Hence, a read access will fetch "random" values here too (it
will be explained in chapter 4 that these values are not really random.
Reading from open addresses fetches the last byte read by the VIC on many
C64s).

The 47 registers of the VIC are mapped in at $d000. Due to the incomplete
address decoding, they are repeated every 64 bytes in the area $d000-$d3ff.

2.4.2 Memory map as seen by the VIC
-----------------------------------

The VIC has only 14 address lines, so it can only address 16KB of memory.
It can access the complete 64KB main memory all the same because the 2
missing address bits are provided by one of the CIA I/O chips (they are the
inverted bits 0 and 1 of port A of CIA 2). With that you can select one of
4 16KB banks for the VIC at a time.

The (extended) memory map as seen by the VIC looks like this:


 $ffff +----------+   --
       |          |
       |          |
       |          |
       |   RAM    | Bank 3
       |          |
       |          |
       |          |
 $c000 +----------+   --
       |          |
       |   RAM    |
       |          |
 $a000 +----------+ Bank 2
       | Char ROM |
 $9000 +----------+
       |   RAM    |
 $8000 +----------+   --
       |          |
       |          |
       |          |
       |   RAM    | Bank 1
       |          |
       |          |
       |          |
 $4000 +----------+   --
       |          |
       |   RAM    |
       |          |
 $2000 +----------+ Bank 0
       | Char ROM |
 $1000 +----------+
       |   RAM    |
 $0000 +----------+   --


The Char ROM is mapped in at the VIC addresses $1000-$1fff in banks 0 and
2 (it appears at $9000 in the above diagram, but remember that the VIC
doesn't know about the two address bits generated by the CIA. From the
VIC's point of view, the Char ROM is at $1000-$1fff also in bank 2).

The attentive reader will already have noticed that the Color RAM doesn't
appear anywhere. But as explained earlier, the VIC has a 12 bit data bus of
which the upper 4 bits are connected with the Color RAM. Generally
speaking, the sole purpose of the upper 4 bits of the VIC data bus is to
read from the Color RAM. The Color RAM is addressed by the lower 10 bits of
the VIC address bus and is therefore available in all banks at all
addresses.

2.4.3 Memory access of the 6510 and VIC
---------------------------------------

6510 and VIC are both based on a relatively simple hard-wired design. Both
chips make a memory access in EVERY clock cycle, even if that is not
necessary at all. E.g if the processor is busy executing an internal
operation like indexed addressing in one clock cycle, that really doesn't
require an access to memory, it nevertheless performs a read and discards
the read byte. The VIC only performs read accesses, while the 6510 performs
both reads and writes.

There are no wait states, no internal caches and no sophisticated access
protocols for the bus as seen with more modern processors. Every access is
done in a single cycle.

The VIC generates the clock frequencies for the system bus and the RAS and
CAS signals for accessing the dynamic RAM (for both the processor and the
VIC). So it has primary control over the bus and may "stun" the processor
sometime or another when it needs additional cycles for memory accesses.
Besides this, the VIC takes care of the DRAM refresh by reading from 5
refresh addresses in each raster line.

The division of accesses between 6510 and VIC is basically static: Each
clock cycle (one period of the Φ2 signal) consists of two phases. The VIC
accesses in the first phase (Φ2 low), the processor in the second phase (Φ2
high). The AEC signal closely follows Φ2. That way the 6510 and VIC can
both use the memory alternatively without disturbing each other.

However, the VIC sometimes needs more cycles than made available to it by
this scheme. This is the case when the VIC accesses the character pointers
and the sprite data. In the first case it needs 40 additional cycles, in
the second case it needs 2 cycles per sprite. BA will then go low 3 cycles
before the VIC takes over the bus completely (3 cycles is the maximum
number of successive write accesses of the 6510). After 3 cycles, AEC stays
low during the second clock phase so that the VIC can output its addresses.

The following diagram illustrates the process of the take-over:

       _ _ _ _ _ _ _ _ _ _ _ _ _    _ _ _ _ _ _ _ _ _ _ _ _ _
 Φ2   _ _ _ _ _ _ _ _ _ _ _ _ _ ..._ _ _ _ _ _ _ _ _ _ _ _ _
      ______________                       __________________
 BA                 ____________...________
       _ _ _ _ _ _ _ _ _ _                  _ _ _ _ _ _ _ _ _
 AEC  _ _ _ _ _ _ _ _ _ _ ______..._________ _ _ _ _ _ _ _ _

 Chip VPVPVPVPVPVPVPVpVpVpVVVVVV...VVVVVVVVVPVPVPVPVPVPVPVP

           1       |  2  |       3        |       4
         Normal    |Take-| VIC has taken  |  VIC releases
      bus activity |over | over the bus   |    the bus


The line "Chip" designates which chip is just accessing the bus (as said
before, there is an access in every cycle). "V" stands for the VIC, "P" for
the 6510. The cycles designated with "p" are accesses of the 6510 that are
only performed if they are write accesses. The first "p" read access stops
the 6510, at least after the third "p" as the 6510 never does more than 3
write accesses in succession. On a "p" read access the processor addresses
are still output on the bus because AEC is still high.

The diagram describes the normal process of a bus take-over. By
appropriately modifying the VIC register $d011, it is possible to force a
bus take-over at extraordinary times. This is explained in chapter 3 as
well as the complete bus timing of a VIC raster line.


3. Description of the VIC
-------------------------

This chapter is about the single function units in the VIC, their way of
working and their unspecified behavior, and the insights into the internal
functions of the VIC that can be gained by that.
