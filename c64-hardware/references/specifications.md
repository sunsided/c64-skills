> Source: C64ServiceManual.txt, "Specifications", "Product Parts List", and "Block Diagram" intro. Lightly cleaned from the Project 64 etext. Schematics/figures were too complex to render as ASCII and are marked [Figure: ...]; consult original scans for trace-level work.

# C64 COMPUTER — Specifications

General description

The "All Purpose" Commodore 64 is the complete computer for education, home or
small business applications. Supported by quality peripherals and a full range
of software, the Commodore 64 is perfect for the family. No other computer can
offer such variety of uses and applications at such an affordable price.

```
Memory          64K RAM

ROM             20K ROM Standard (includes operating system and BASIC
                interpreter)

Microprocessor  6510A Microprocessor - 1.02 MHz clock
                Compatible with the 6502

Display         40 Columns X 25 lines of text

Colors          16 Background, border and character colors

Characters      Upper & lower case letters, numerals and symbols
                Reverse characters
                All PET graphic characters

Display modes   Text characters * High resolution graphics

Resolution      320 X 200 Pixels

Sprites         8 independent sprites
                Each consists of 24 X 21 pixels and up to 4 colors
                Each independently expandable horizontally and vertically
                Collision detection for sprite to sprite and data to sprite
                collisions

Sound           6581 Sound Interface Device includes 3 independent tone
                generators - each with 9 octaves
                Each voice includes programmable ADSR generator (Attack, Decay,
                Sustain, Release) and control of sawtooth, triangle, square,
                variable pulse and noise waveforms
                Full filtering capabilities with low, high and band pass
                filters
                External sound input

Keyboard        Full size typewriter style design

Keys            66 Keys total
                2 Cursor control keys
                4 Function keys (up to 8 user defined/programmable functions
                possible)
                Upper and lower case character set
                Graphic character set

Inputs/Outputs  User port
                Serial port
                ROM cartridge port
                2 Joystick/paddle ports
                Video port C1530 Cassette drive interface port

Features        Built-in BASIC 2.0 - over 70 commands, statements and functions
                Full screen editor

Peripherals     C1541 Disk drive
                C1530 Datasette
                MPS 801 Dot matrix printer
                MPS 802 Dot matrix printer
                MPS 803 Dot matrix printer
                DPS 1101 Daisey wheel printer
                C1520 Plotter/Printer
                C1702 Color monitor
                CM141 Color monitor

Power requirements
                120 Volts, 60 Hz
```

Specifications subject to change without notice.


# PARTS LIST C-64

PLEASE NOTE: Commodore part numbers are priced for reference only and do not
indicate the availability of parts from Commodore. Industry standard parts
(Resistors, Capacitors, Connectors) should be secured locally. Approved
cross-references for TTL-chips, Transistors, etc. will be available in manual
form through the Service Department in November of 1984. Unique or non-standard
part will be stocked by Commodore and are indicated on the parts list by a "C".

```
        TOP CASE ASSY
            Top Case                C 326113-01
            Keyboard                C 326166-02
            LED Plate               C 326160-01
            Nameplate               C 326161-01
            Lamp Hold Set           C 903820-03
            LED Assembly            C 1001039-01

        BOTTOM CASE ASSY
            Bottom Case             C 326114-01
            Foot, Self-Adhesive     C 950157-04
            PCB Shield Plate        C 326131-01
            PCB Insulation Sheet    C 326288-01

        ACCESSORIES
            Users Manual            C 326114-01
            Power Supply            C 950157-04
            RF Cable                C 326131-01
            Switch Box              C 326288-01
```


# BLOCK DIAGRAM

[Figure: C-64 Block Diagram]

(The block diagram figure was too complex to render as ASCII in the etext and is
omitted here. The "CIRCUIT THEORY" sections in `circuit-theory.md` describe each
functional block — power supply, reset, clock, I/O/RAM/expansion decoding, RAM
control, video/audio, cassette, keyboard/joystick/paddle, serial/user port — in
prose. For the actual trace-level block diagram and schematics, consult the
original scanned service manual.)
