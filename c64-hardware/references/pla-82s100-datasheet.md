> Source: pla.txt — the 82S100 manufacturer data sheet portion (and provenance intro). Lightly cleaned from the Project 64 etext (OCR mojibake in names fixed). The C64-specific PLA fuse map, JEDEC file, and the ROM/RAM/IO banking logic equations are NOT reproduced here — that logic and its banking semantics live in **c64-memory-map**. This file covers the 82S100 chip itself (U17, Commodore part 906114-01) as a hardware part.

# C64 PLA — provenance

On 30th August 1994, Jens Schönfeld (sysop@nostlgic.oche.de) posted the raw data
from the C64 PLAs in the German newsgroup
z-netz.rechner.c64+c128.allgemein. He read the chip with an EPROM programmer
device as a 27512 EPROM using a home-built adaptor.

From the 64kB raw data, Marko Mäkelä (Marko.Makela@HUT.FI) and several others
tried to manually create the logic equations, independent of each other. Marko
was the first one who completed the work. Especially the CASRAM equations took
lots of time. Andreas Boose (boose@unixserv.rz.fh-hannover.de) helped to
optimize the CASRAM equations a bit.

This work was finally verified by Mark Smith (mark@te.rl.ac.uk), who read out the
82S100 of the oldest C64 and converted the JEDEC file to logic equations with the
Abel program. Andreas Boose verified the new equations.

The original pla.txt file contains three sections:
1. a manufacturer data sheet of 82S100
2. a JEDEC file which can be used to burn a 82S100 to act like a C64 PLA
3. a logic equation file created with Abel

Only the manufacturer data sheet is reproduced below — it describes the physical
part. The JEDEC fuse map and the C64 banking equations (which define
ROM/RAM/I-O bank switching) are covered, with their banking semantics, in the
**c64-memory-map** skill.

Mark Smith writes:

"Anyone should be able to blow a new PLA from the JEDEC file I sent you, and when
supplies of the 82S100 chip finally dry up completely, the equations should be
able to be put into a different type of logic array chip. The only thing that
would have to be done is to make a printed circuit board adaptor to take the pins
on the new chip to the correct positions to plug into the C64 motherboard. As far
as I am aware, there are virtually no other PLA chips with a 28 pin footprint.
Modern ones are nearly all square packaged PLCC types. It is also very difficult
to find a modern PLA chip with 16 inputs and 8 outputs - most have only 22 dual
purpose I/Os or have many more. I think the next step up is a 44 pin device.

So a modern replacement would probably have to be a 44 pin PLCC square packaged
PAL (PLA) chip mounted onto a printed circuit board which takes the pins to a 28
pin dual in line header outline.

I'm sure it could be done. Maybe I should look into it, as 82S100s are very
difficult to come by now and out of the 3 C64s I have, the 2 that were faulty
both had duff PLA chips. The faulty PLA chips were both Commodore mass produced
replacements for the fuse programmable 82S100. I think that the commodore
replacement chips are probably less reliable than the original 82S100s used in
early machines."


# 82S100 data sheet

The 82S100 is a bipolar, fuse-link programmable logic array. It uses the
standard AND/OR/invert architecture to directly implement custom
sum-of-product logic equations.

Each device consists of 16 dedicated inputs and 8 dedicated outputs. Each output
is capable of being actively controlled by any or all of the 48 product terms.
The true, complement, or don't care condition of each of the 16 inputs ANDed
together comprise one P-Term. All 48 P-Terms are then OR-d to each output. The
user must then only select which P-Terms will activate an output by
disconnecting terms which do not affect the output. In addition, each output can
be fused as active high or active low.

The 82S100 is fully TTL compatible and includes chip-enable control for
expansion of input variables and output inhibit. It features three state
outputs.

```
Field programmable Ni-Cr links
16 inputs
8 outputs
48 product terms
Commercial verion - N82S100 - 50ns max address access time
Power dissipation - 600mW typ
Input loading - 100uA max
Chip enable input
Three state outputs
```

The 82S100 devices are shipped in an unprogrammed state characterised by:
All internal Ni-Cr links are intact and therefore each product term contains
both true and complement values of every input variable, the OR matrix contains
all 48 P-Terms, the polarity of each output is set to active high, all outputs
are at a low logic level.

(In the C64 the 82S100 is U17, Commodore stocked part number 906114-01. Its 28-pin
pinout is given in `board-identification.md` under "PIN ASSIGNMENTS". Later C64s
shipped with a Commodore-made HMOS replacement, part 906114, which is widely
reported to run hotter and fail more often than the original Signetics 82S100.)
