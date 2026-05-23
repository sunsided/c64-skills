> Source: c64prg.txt App I, "Pinouts for Input/Output Devices". Lightly cleaned from the Project 64 etext.

# Pinouts for Input/Output Devices

This appendix is designed to show you what connections may be made to the Commodore 64.

          1) Game I/O             4) Serial I/O (Disk/Printer)
          2) Cartridge Slot       5) Modulator Output
          3) Audio/Video          6) Cassette
                                  7) User Port

## Control Port 1

    +-----+-------------+-----------+
    | Pin |    Type     |   Note    |            1 2 3 4 5
    |  1  |    JOYA0    |           |            O O O O O
    |  2  |    JOYA1    |           |
    |  3  |    JOYA2    |           |             O O O O
    |  4  |    JOYA3    |           |             6 7 8 9
    |  5  |    POT AY   |           |
    |  6  | BUTTON A/LP |           |
    |  7  |     +5V     | MAX. 50mA |
    |  8  |     GND     |           |
    |  9  |   POT AX    |           |
    +-----+-------------+-----------+

## Control Port 2

    +-----+-------------+-----------+
    | Pin |    Type     |   Note    |
    |  1  |    JOYB0    |           |
    |  2  |    JOYB1    |           |
    |  3  |    JOYB2    |           |
    |  4  |    JOYB3    |           |
    |  5  |    POT BY   |           |
    |  6  |  BUTTON B   |           |
    |  7  |     +5V     | MAX. 50mA |
    |  8  |     GND     |           |
    |  9  |   POT BX    |           |
    +-----+-------------+-----------+

## Cartridge Expansion Slot

    Pin    Type       Pin    Type       Pin    Type       Pin    Type
    +----+----------+ +----+----------+ +----+----------+ +----+----------+
    |  1 | GND      | | 12 | BA       | |  A | GND      | |  N | A9       |
    |  2 | +5V      | | 13 | /DMA     | |  B | /ROMH    | |  P | A8       |
    |  3 | +5V      | | 14 | D7       | |  C | /RESET   | |  R | A7       |
    |  4 | /IRQ     | | 15 | D6       | |  D | /NMI     | |  S | A6       |
    |  5 | R/W      | | 16 | D5       | |  E | 02       | |  T | A5       |
    |  6 | Dot Clock| | 17 | D4       | |  F | A15      | |  U | A4       |
    |  7 | I/O1     | | 18 | D3       | |  H | A14      | |  V | A3       |
    |  8 | /GAME    | | 19 | D2       | |  J | A13      | |  W | A2       |
    |  9 | /EXROM   | | 20 | D1       | |  K | A12      | |  X | A1       |
    | 10 | I/O2     | | 21 | D0       | |  L | A11      | |  Y | A0       |
    | 11 | /ROML    | | 22 | GND      | |  M | A10      | |  Z | GND      |
    +----+----------+ +----+----------+ +----+----------+ +----+----------+
                   2 2 2 1 1 1 1 1 1 1 1 1 1
                   2 1 0 9 8 7 6 5 4 3 2 1 0 9 8 7 6 5 4 3 2 1
               +---@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@---+
               |                                                 |
               +---@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@---+
                   Z Y X W V U T S R P N M L K J H F E D C B A

## Audio/Video

       Pin            Type
    +-------+----------------------+
    |   1   |  LUMINANCE           |
    |   2   |  GND                 |
    |   3   |  AUDIO OUT           |
    |   4   |  VIDEO OUT           |
    |   5   |  AUDIO IN            |
    |   6   |  CHROMINANCE         |
    +-------+----------------------+

## Serial I/O

       Pin            Type
    +-------+----------------------+                 ++ ++
    |   1   |  /SERIAL SRQ IN      |                / +-+ \
    |   2   |  GND                 |               /5     1\
    |   3   |  SERIAL ATN OUT      |              +  O   O  +
    |   4   |  SERIAL CLK IN/OUT   |              |    6    |
    |   5   |  SERIAL DATA IN/OUT  |              |    O    |
    |   6   |  /RESET              |              +  O   O  +
    +-------+----------------------+               \4  O  2/
                                                    \  3  /
                                                     +---+

## Cassette

    +-------+--------------------+
    |  Pin  |        Type        |
    +-------+--------------------+
    |  A-1  |  GND               |              1 2 3 4 5 6
    |  B-2  |  +5V               |          +---@-@-@-@-@-@---+
    |  C-3  |  CASSETTE MOTOR    |          |                 |
    |  D-4  |  CASSETTE READ     |          +---@-@-@-@-@-@---+
    |  E-5  |  CASSETTE WRITE    |              A B C D E F
    |  F-6  |  CASSETTE SENSE    |
    +-------+--------------------+

## User I/O

    +-----+---------------+-----------+   +-----+---------------+-----------+
    | Pin |      Type     |    Note   |   | Pin |      Type     |    Note   |
    +-----+---------------+-----------+   +-----+---------------+-----------+
    |   1 |  GND          |           |   |  A  |  GND          |           |
    |   2 |  +5V          |MAX. 100 mA|   |  B  |  /FLAG2       |           |
    |   3 |  /RESET       |           |   |  C  |  PB0          |           |
    |   4 |  CNT1         |           |   |  D  |  PB1          |           |
    |   5 |  SP1          |           |   |  E  |  PB2          |           |
    |   6 |  CNT2         |           |   |  F  |  PB3          |           |
    |   7 |  SP2          |           |   |  H  |  PB4          |           |
    |   8 |  /PC2         |           |   |  I  |  PB5          |           |
    |   9 |  SER. ATN OUT |           |   |  K  |  PB6          |           |
    |  10 |  9 VAC        |MAX. 100 mA|   |  L  |  PB7          |           |
    |  11 |  9 VAC        |MAX. 100 mA|   |  M  |  PA2          |           |
    |  12 |  GND          |           |   |  N  |  GND          |           |
    +-----+---------------+-----------+   +-----+---------------+-----------+

                                             1 1 1
                           1 2 3 4 5 6 7 8 9 0 1 2
                        +--@-@-@-@-@-@-@-@-@-@-@-@--+
                        |                           |
                        +--@-@-@-@-@-@-@-@-@-@-@-@--+
                           A B C D E F H J K L M N
