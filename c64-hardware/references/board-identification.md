> Source: C64ServiceManual.txt, "C64 BOARD IDENTIFICATION", the per-board layouts, parts lists, and the "PIN ASSIGNMENTS" section. Lightly cleaned from the Project 64 etext. Board-layout figures, modulator schematics and the full circuit schematics were too complex to render as ASCII and are marked [Figure: ...]; consult original scans for trace-level work.

# C64 BOARD IDENTIFICATION

To date there are 4 version of 64 PCB assemblies in use.

```
VERSION     IDENTIFYING FACTORS         PCB ASSY #      SCHEMATIC #

Original    5 pin board                 326298-01       326106
            (CN5-Video port has 5 pins)

A (CR)      8 pin board                 250407-04       251138
            (CN5-Video port has 8 pins)

B           8 pin board                 250425          251469
            (Reduced oscillator circuit)

B-2         8 pin board                 250441-01*      251469
```

- These boards are interchangeable with casework, keyboard, etc.; however, care
  must be taken to provide the customer with a unit that is compatible with their
  monitor and cable.

- When component level repairs are necessary, be certain to acquire the
  appropriate part for the board you are repairing. Most modulators are
  different, as are many of the components.

* The 4th version of 64 board was recently developed and only a few may be in
the field. It is termed the 64B-2. All circuits remain the same as the 64B
(Schematic 251469) with a few component location changes:

1) Resistors 28, 29, 30, 36, 48 were reduced to Resistor Pack RP5.

2) Diodes CR100-105 are no longer piggybacked. Their new locations are CR9,
   12-16.


# BOARD LAYOUT #326298-01

[Figure: Board Layout #326298-01]

## PARTS LIST - PCB ASSEMBLY #326298

C - Indicates Commodore Stocked Part Numbers

```
  INTEGRATED CIRCUITS
U1,U2   6526 CIA                    C 906108-01
U3      2364 Basic ROM              C 901226-01
U4      2364 Kernal ROM             C 901227-03
U5      2364 Char ROM               C 901225-01
U6      2114L-30 RAM                  901453-01
U7      6510 uProcessor             C 906107-01
U8      7406                          901522-06
U9-U12  4164 (200 nS)                 901505-01
U13     74LS257                       901521-57
U14     74LS258                       901521-58
U15     74LS139                       901521-18
U16     4066                          901502-01
U17     82S100 PLA                  C 906114-01
U18     6581 SID                    C 906112-01
U19     6567 VIC II                 C 906109-04
U20     LM556                         901523-03
U21-U24 4161 (200 nS)                 901505-01
U25     74LS257                       901521-57
U26     74LS373                       901521-29
U27     74LS08                        901521-03
U28     4066                          901502-01
U29     74LS74                        901521-06
U30     74LS193                       901521-26
U31     74LS629                       901521-68
U32     MC4044                        906128-01
  TRANSISTORS
Q1      2N4401                        902652-01
Q2      2N3904                        902658-01
Q3      TIP29 B                       902653-01
Q4-8    2N2222                        902686-01
  DIODES
CR1     2.7V Zener IN4371
CR2     7.5V Zener IN755
CR3     IN914
CR4     Bridge, Varo VMO8             906129-01
CR5,6   Rectifier IN4001
  RESISTORS - All values are in ohms- 1/4W,
              5%, unless noted otherwise.
R1  3.3K        R7  10K
R2  1.5K        R8  390
R3  10K         R9  75
R4  1K          R10 120
R5  560         R11 120
R6  1K          R13 1K
  RESISTORS (continued)
R14 100         R30 1K
R16 1K          R31 180
R17 1.2K        R33 47K
R19 15K         R34 47K
R20 6.8K        R35 470K
R21 4.7K        R37 2.7K
R22 1.5K        R38 1K
R23 1K          R39 390
R24 3.3K        R41 1M
R25 Pot 1K      R43 3.3K
R26 75          R44 3.3K
R27 Pot 2K      R45 3.3K
R28 1K          R46 2K
R29 1K          R51 1.5K
NOTE: The input video line requires a 470 ohm,
      1/4 watt, resistor soldered to ground.

  RESISTOR PACKS
RP1,2   33, 8 Pin (Bourne No. 430BR-102-330)
RP3     33K, 8 Pin (Bourne No. 430BR-101-332)
RP4     3.3K, 10 Pin
  CAPACITORS
C1-3        Ceramic          .1 uF, 50V
C4-7        Ceramic         .47 uF, 50V, 20%
C8          Electrolytic     10 uF, 25V, +50%, -10%
C9          Ceramic         .47 uF, 50V, 20%
C10-11      Ceramic         470 pF, 50V
C12-15      Electrolytic     10 uF, 25V, +50%, -10%
C16         Ceramic          .1 uF, 50V
C17         Electrolytic     10 uF, 25V, +50%, -10%
C18         Ceramic          .1 uF, 50V
C19         Electrolytic   2200 uF, 16V
C20,21      Film            .22 uF, 100V, 20%
C22         Ceramic          .1 uF, 50V
C23         Ceramic         360 pF, 50V
C24         Electrolytic     10 uF, 25V, +50%, -10%
C25-28      Ceramic         .22 uF, 50V
C29         Ceramic         .47 uF, 50V, 20%
C30,31,32   Ceramic          .1 uF, 50V
C33         Ceramic         .47 uF, 50V, 20%
C34         Electrolytic     10 uF, 25V, +50%, -10%
C35         Ceramic          .1 uF, 50V
C36         Ceramic          20 pF, 50V
C37         Ceramic        1000 pF, 50V
C38         Ceramic          51 uF, 50V
C39         Ceramic          .1 uF, 50V
C40-43      Ceramic         .22 uF, 25V, +50%, -10%
C44         Ceramic         .47 uF, 50V, 20%
C45,46,47   Ceramic          .1 uF, 50V
C48         Ceramic        1800 uF, 50V
C49         Ceramic         470 pF, 50V
C50         Ceramic         .22 uF, 50V
C51         Ceramic         .47 uF, 50V, 20%
C52,53      Ceramic         470 pF, 50V
C54         Ceramic         .22 uF, 50V
C55         Ceramic          .1 uF, 50V
C56         Ceramic          .1 uF, 50V
C57         Electrolytic     10 uF, 25V, +50%, -10%
C58         Ceramic          .1 uF, 50V
C59         Ceramic         .22 uF, 50V
C60,61      Ceramic         .47 uF, 50V, 20%
C62         Electrolytic     10 uF, 25V, +50%, -10%
C63         Ceramic         .47 uF, 50V, 20%
C64,65      Electrolytic     10 uF, 25V, +50%, -10%
C66,67      Ceramic         .47 uF, 50V, 20%
C68         Ceramic          .1 uF, 50V
C69
C70         Mica             10 pF, 500V, 5%
C71         Ceramic          .1 uF, 50V
C72         Ceramic         220 pF, 50V
C73         Ceramic         150 pF, 50V
C74         Ceramic          .1 uF, 50V
C77         Ceramic          .1 uF, 50V
C78         Ceramic         220 pF, 50V
C79         Ceramic         510 pF, 50V
C80         Ceramic          51 pF, 50V
C81         Ceramic          20 pF, 50V
C82         Ceramic          .1 uF, 50V
C83         Mica            .33 pF, 500V, 5%
C84         Ceramic          .1 uF, 50V
C85         Ceramic         .47 uF, 50V, 20%
C86         Mica             39 pF, 500V, 5%
C87         Ceramic          .1 uF, 50V
C88         Electrolytic    470 uF, 50V
C89         Ceramic          .1 uF, 50V
C90         Electrolytic    470 uF, 50V
C91         Electrolytic    100 uF, 16V
C92         Ceramic         .22 uF, 50V
C93         Ceramic        1800 uF, 50V
C94         Electrolytic     10 uF, 25V, +50%, -10%
C95,96      Ceramic          .1 uF, 50V
C97         Ceramic         .22 uF, 25V
C98,99      Ceramic          .1 uF, 50V
C100        Ceramic         .22 uF, 25V
C101        Ceramic          .1 uF, 50V
C102        Electrolytic     10 uF, 25V, +50%, -10%
C103        Ceramic          .1 uF, 50V
C105        Ceramic          .1 uF, 50V

  CONNECTORS
CN1     Header Assy 20 Pin            903331-20
CN4     6 Pin Din                   C 903361-01
CN5     5 Pin Din                   C 903362-01
CN6     44 Pin Card Edge            C 906100-02
CN7     7 Pin Din                   C 906130-01
CN8,9   Plug Assy, 8 Pin Rt. Angle  C 906126-01
CN10    Header Assy, 3 Pin

  MISCELLANEOUS
L1,2    Coil Inductor 2.2 uH          901151-17
L3      Coil Inductor 3.0 uH          901151-21
L4      Filter Line Assy            C 906127-01
L5      Coil Inductor 1.2 uH          901152-01
Y1      Crystal 14.31818 MHz        C 900558-01
SW1     Rocker Switch DPDT          C 904500-01
VR1     Voltage Regulator MC7812CT
VR2     Voltage Regulator MC7805CT
M1      Modulator                   C 326130-01
F1      Fuse, Normal Blo, 250V, 1.5A
FB1-23  Ferrite Bread                 903025-01
        Connector Panel
            (ON, OFF, Joystick)       326299-01
        Catridge Guide                326116-01
        Shield Box                  C 326265-01
        Shield Cap                  C 326267-01
```

[Figure: Schematic #326106 sheet 1 of 2]
[Figure: Schematic #326106 sheet 2 of 2]


# BOARD LAYOUT #250407-04

[Figure: Board Layout #250407-04]

## PARTS LIST - PCB ASSEMBLY #250407-04

C - Indicates Commodore Stocked Part Numbers

```
  INTEGRATED CIRCUITS
U1,U2   6526 CIA                    C 906108-01
U3      2364 Basic ROM              C 901226-01
U4      2364 Kernal ROM             C 901227-03
U5      2364 Char ROM               C 901225-01
U6      2114L-30 RAM                  901453-01
U7      6510 uProcessor             C 906107-01
U8      7406                          901522-06 sub:
        7416                          901522-14
U9-U12  4164 (200 nS)                 901505-01
U13     74LS257                       901521-57
U14     74LS258                       901521-58
U15     74LS139                       901521-18
U16     4066                          901502-01
U17     82S100 PLA                  C 906114-01
U18     6581 SID                    C 906112-01
U19     6567 VIC II                 C 906109-04
U20     LM556                         901523-03
U21-U24 4161 (200 nS)                 901505-01
U25     74LS257                       901521-57
U26     74LS373                       901521-29
U27     74LS08                        901521-03
U28     4066                          901502-01
U29     74LS74                        901521-06
U30     74LS193                       901521-26
U31     74LS629                       901521-68
U32     MC4044                        906128-01
  TRANSISTORS
Q1,2    2SC1815                     C 902693-01
Q3      TIP29 A                       902653-01
Q7,8    2SC1815                     C 902693-01
  DIODES
CR1     2.7V Zener IN4371             906103-02
CR2     7.5V Zener IN755              900941-01
CR4     Bridge S2VB10               C 251026-01
               DBA20B                 251026-02
               DBA20C                 251026-03
CR5,6   Rectifier IN4001             900750-01
  RESISTORS - All values are in ohms- 1/4W,
              5%, unless noted otherwise.
R1  3.3K        R6   1K
R2  1.5K        R7   10K
R3  10K         R16  1K
R4  1K          R17  2.7K
R5  560         R19  15K
  RESISTORS (continued)
R26 75          R39  390
R27 Pot 2K      R41  1M
R28 1K          R42  82
R29 1K          R43  3.3K
R30 1K          R44  3.3K
R31 180         R45  3.3K
R33 47K         R50  1M
R34 47K         R51  1.5K
R35 470K        R52  300
R36 1K          R53  390
R37 2.7K        R100 1K
R38 1K          R101 22K
  RESISTOR PACKS
RP1,2   33, 8 Pin (Bourne No. 430BR-102-330)
RP3     33K, 8 Pin (Bourne No. 430BR-101-332)
RP4     3.3K, 10 Pin
  CAPACITORS
C1-7        Ceramic          .1 uF, 25V
C8          Electrolytic     10 uF, 25V, +50%, -10%
C9          Ceramic          .1 uF, 25V
C10,11      Ceramic         470 pF, 50V
C12         Ceramic          .1 uF, 25V
C13,14,15   Electrolytic     10 uF, 25V, +50%, -10%
C16         Ceramic          .1 uF, 25V
C17         Electrolytic     10 uF, 25V, +50%, -10%
C18         Ceramic          .1 uF, 25V
C19         Electrolytic   2200 uF, 16V
C20,21      Film            .22 uF, 100V, 20%
C22         Ceramic          .1 uF, 25V
C23         Ceramic         360 pF, 50V
C24         Electrolytic     10 uF, 25V, +50%, -10%
C25-33      Ceramic          .1 uF, 25V
C34         Electrolytic     10 uF, 25V, +50%, -10%
C35         Ceramic          .1 uF, 50V
C36         Ceramic          20 pF, 50V, 5% SL
C37         Ceramic        1000 pF, 50V, 10% B
C38         Ceramic          51 uF, 50V, 5% SL
C39-47      Ceramic          .1 uF, 25V
C48         Ceramic        1800 pF, 50V, 10% B
C49-54      Ceramic          .1 uF, 25V
C55         Ceramic          .1 uF, 50V
C56         Ceramic          .1 uF, 25V
C57         Electrolytic     10 uF, 25V, +50%, -10%
C58         Ceramic          .1 uF, 50V
C59,60      Ceramic          .1 uF, 25V
C62,65      Electrolytic     10 uF, 25V, +50%, -10%
C66,67,68   Ceramic          .1 uF, 25V
C70         Film             16 pF, 5%
C74,82      Ceramic          .1 uF, 25V
C83         Ceramic          82 pF, 5%
C84         Ceramic          .1 uF, 25V
C85         Ceramic         .47 uF, 50V, 10%
C88         Electrolytic   1000 uF, 25V
C89         Ceramic          .1 uF, 25V
C90         Electrolytic    470 uF, 50V
C91         Electrolytic    100 uF, 16V, +50%, -10%
C92         Ceramic          .1 uF, 25V
C93         Ceramic        1800 pF, 50V, 10% B
C94         Electrolytic     10 uF, 25V, +50%, -10%
C95,96      Ceramic          .1 uF, 25V
C97         Ceramic         .22 uF, 25V
C98,99      Ceramic          .1 uF, 25V, +80%, -20%
C100        Ceramic         .22 uF, 25V
C101        Ceramic          .1 uF, 50V, +80%, -20%
C102        Electrolytic     10 uF, 25V, +50%, -10%
C103        Ceramic          .1 uF, 25V
C104
C105        Ceramic          .1 uF, 25V
C108        Electrolytic     10 uF, 25V, +50%, -10%
C200        Ceramic          .1 uF, 25V

  CONNECTORS
CN1     Header Assy 20 Pin            903331-20
CN4     6 Pin Din                   C 903361-01
CN5     8 Pin Din                   C 325573-01
CN6     44 Pin Card Edge            C 906100-02
CN7     7 Pin Din                   C 251116-01
CN8,9   Plug Assy, 9 Pin MINID      C 906126-01
CN10    Header Assy, 3 Pin            903332-03

  MISCELLANEOUS
L2      Coil Inductor 2.2 uH          901151-17
L4      Coil Inductor 1.2 uH          325570-01
L5      Choke Coil                  C 325559-02
Y1      Crystal 14.31818 MHz        C 900558-01
SW1     Rocker Switch DPDT          C 904500-01
VR1     Voltage Regulator MC7812CT    901527-01
VR2     Voltage Regulator MC7805CT    901527-02
M1      Modulator                   C 251080-01
F1      Fuse, Normal Blo, 250V, 1.5A
FB1-23  Ferrite Bread                 903025-01
        Connector Panel
            (ON, OFF, Joystick)       251095-01
        Catridge Guide                326116-01
        Shield Box                  C 251023-01
        Shield Cap                  C 251024-01
```

[Figure: Modulator schematic #251025]
[Figure: Schematic #251138 sheet 1 of 2]
[Figure: Schematic #251138 sheet 2 of 2]


# BOARD LAYOUT #250425-01

[Figure: Board Layout #250425-01]

## PARTS LIST - PCB ASSEMBLY #250425-01

C - Indicates Commodore Stocked Part Numbers

```
  INTEGRATED CIRCUITS
U1,U2   6526 CIA                    C 906108-01
U3      2364 Basic ROM              C 901226-01
U4      2364 Kernal ROM             C 901227-03
U5      2364 Char ROM               C 901225-01
U6      2114L-30 RAM                  901453-01
U7      6510 uProcessor             C 906107-01
U8      7406                          901522-06 sub:
        7416                          901522-14
U9-U12  4164 (200 nS)                 901505-01
U13     74LS257                       901521-57
U14     74LS258                       901521-58
U15     74LS139                       901521-18
U16     4066                          901502-01
U17     82S100 PLA                  C 906114-01
U18     6581 SID                    C 906112-01
U19     6567 VIC II                 C 906109-04
U20     LM556                         901523-03
U21-U24 4161 (200 nS)                 901505-01
U25     74LS257                       901521-57
U26     74LS373                       901521-29
U27     74LS08                        901521-03
U28     4066                          901502-01
U31     7701/8701                   C 251527-01
  TRANSISTORS
Q1      TIP29 A                       902653-01
Q2-4    2SC1815                     C 902693-01
  DIODES
CR1     2.7V Zener IN4371             906103-02
CR2     6.8V Zener IN755
CR4     Bridge S2VB10               C 251026-01 sub:
               DBA20B                 251026-02 sub:
               DBA20C                 251026-03
CR5,6   Rectifier IN4001             900750-01
CR9,            IN4148 sub:
CR12-16         IN914
CR100-105
  RESISTORS - All values are in ohms- 1/4W,
              5%, unless noted otherwise.
R1  3.3K        R26  3.3K
R2  1.5K        R31 180
R3  10K         R33 47K
R4  1K          R34 47K
R5  560         R35 470K
R6   1K         R37 2.7K
R7   10K        R38 1K
  RESISTORS (continued)
R39  390        R50  1M
R41  1M         R51  1.5K
R42  82         R60  100
R43  3.3K       R100 1K
R44  3.3K       R101 22K
R45  3.3K
  RESISTOR PACKS
RP1,2   33, 8 Pin (Bourne No. 430BR-102-330)
RP3     33K, 8 Pin (Bourne No. 430BR-101-332)
RP4     3.3K, 10 Pin
RP5     1K, 6 Pin
  CAPACITORS
C1-7        Ceramic          .1 uF, 25V
C9          Ceramic          .1 uF, 25V
C10,11      Ceramic         470 pF, 50V, 10%
C12         Ceramic          .1 uF, 25V
C13         Electrolytic     10 uF, 25V, +50%, -10%
C15         Tantalum        4.7 uF, 16V, 20%
C19         Electrolytic   2200 uF, 16V
C20         Film            .22 uF, 100V, 20%
C22         Ceramic          .1 uF, 25V
C23         Ceramic         360 pF, 50V, 10% sub: 390 pF
C24         Electrolytic     22 uF, 25V, +50%, -10%
C31,33,34   Ceramic          .1 uF, 25V
C37         Ceramic        1000 pF, 50V, 10% B
C38         Ceramic          51 pF, 50V, 5% SL
C39-46      Ceramic          .1 uF, 25V
C48         Ceramic        1800 pF, 50V, 10% B
C50,51,53   Ceramic          .1 uF, 25V
C59         Ceramic          .1 uF, 25V
C88         Electrolytic   1000 uF, 25V
C90         Electrolytic    470 uF, 50V
C91         Electrolytic    100 uF, 16V, +50%, -10%
C93         Ceramic        1800 pF, 50V, 10% B
C101        Ceramic          .1 uF, 50V, +80%, -20%
C102        Electrolytic     10 uF, 25V, +50%, -10%
C150-152    Ceramic         470 pF, 50V, 10%
C153        Ceramic          68 pF, 50V, 5%
C154        Ceramic         470 pF, 50V, 10%
C200        Ceramic          .1 uF, 25V
C204        Ceramic         150 pF, 50V, 10%
C205        Ceramic         220 pF, 50V, 5%
CT1         Trimmer          40 pF

  CONNECTORS
CN1     Header Assy 20 Pin            903331-20
CN4     6 Pin Din                   C 903361-01
CN5     8 Pin Din                   C 325573-01
CN6     44 Pin Card Edge            C 906100-02
CN7     7 Pin Din                   C 251116-01
CN8,9   Plug Assy, 9 Pin MINID      C 251057-01
CN10    Header Assy, 3 Pin            903332-03

  MISCELLANEOUS
L2      Coil Inductor 2.2 uH          901151-17
L4      Line Filter Assy            C 251701-01
L5      Coil Inductor 1.2 uH          901152-01
Y1      Crystal 14.31818 MHz        C 251707-01
SW1     Rocker Switch DPDT          C 904500-01
VR1     Voltage Regulator MC7812CT    901527-01
VR2     Voltage Regulator MC7805CT    901527-02
M1      Modulator                   C 251696-01
        Connector Panel
            (ON, OFF, Joystick)       251095-01
        Catridge Guide                326116-01
F1      Fuse, Normal Blo, 250V, 1.5A
```

(NOTE: in the etext the connectors/miscellaneous block for the #250425-01 board
is printed under a "PCB ASSEMBLY #250407-04 (Continued)" running header; it
belongs to the #250425-01 / #250441-01 board family per the layout sequence.)

[Figure: Modulator schematic #251696]
[Figure: Schematic #251469 sheet 1 of 2]
[Figure: Schematic #251469 sheet 2 of 2]


# PIN ASSIGNMENTS

## U1, U2 - 906108-01 — 6526 COMPLEX INTERFACE ADAPTER (CIA)

```
  GND-+ 1     40+-CNT
  PA0-+ 2     39+-SP
  PA1-+ 3     38+-RS0
  PA2-+ 4     37+-RS1
  PA3-+ 5     36+-RS2
  PA4-+ 6     35+-RS3
  PA5-+ 7     34+-_RES
  PA6-+ 8     33+-DB0
  PA7-+ 9     32+-DB1
  PA0-+10     31+-DB2
  PB1-+11     30+-DB3
  PB2-+12     29+-DB4
  PB3-+13     28+-DB5
  PB4-+14     27+-DB6
  PB5-+15     26+-DB7
  PB6-+16     25+-O2
  PB7-+17     24+-_FLAG
  PPC-+18     23+-_CS
  TOD-+19     22+-R/_W
  VCC-+20     21+-_IRQ
```

```
1       VSS     Ground connection
2-9     PA0-PA7 Parallel port a signals. Bidirectional parallel port.
10-17   PB0-PB7 Parallel port b signals. Bidirectional parallel port.
18      PC      Handshake output. A low pulse is generated after a read or
                write on port b.
19      TOD     Time od day clock input. Programmable 50hz or 60hz.
20      VCC     5VDC input.
21      IRQ     Interrupt output to microprocessor input IRQ.
22      R/W     READ/WRITE input from microprocessor's R/W output.
23      CS      Chip select input. A low pulse will activate CIA.
24      FLAG    Negative edge sensitive interrupt input. Can be used as a
                handshake line for either parallel port.
25      O2      O2 clock input. Connected to processor common O2 clock.
26-33   DB0-DB7 Bidirectional data bus. Connects to processor data bus.
34      RES     Low active reset input. Initializes CIA.
35-38   RS0-RS3 Register select inputs. Used to select all internal registers
                for communications with the parallel ports, time of day clock
                and serial port (SP).
39      SP      Serial Port bidirectional connection. An internal shift
                register converts microprocessor parallel data into serial
                data, and vice versa.
40      CNT     Count input. Internal timers can count pulses applied to this
                input. cAn be used for frequency dependant operations.
```

## U18 - 906112-01 — 6581 SOUND INTERFACE DEVICE (SID)

```
  CAP-+1A     28+-12V
  CAP-+1B     27+-A.OUT
  CAP-+2A     26+-EXT IN
  CAP-+2B     25+-5V
 _RES-+ 5     24+-POT X
   O2-+ 6     23+-POT Y
 R/_W-+ 7     22+-D7
  _CS-+ 8     21+-D6
   A0-+ 9     20+-D5
   A1-+10     19+-D4
   A2-+11     18+-D3
   A3-+12     17+-D2
   A4-+13     16+-D1
  GND-+14     15+-D0
```

```
1,2,    CAP1A,1B
3,4     2A,2B   Capacitor filter connections
5       RES     Reset input. A low pulse initializes the SID.
6       O2      Processor phase 2 clock input.
7       R/W     Processor read/write input.
8       CS      Chip select input.
9-13    A0-A4   Address lines from processor.
14      GND     Dc ground connection.
15-22   D0-D7   Data Bus connections.
23      POT Y   Input to a A/D converter used to detect the value of a variable
                resistor. Commonly connected to game paddles.
24      POT X   Same as POT Y.
25      VCC     5VDC.
26      EXT IN  External audio input.
27      A.OUT   Audio output. Should be AC coupled to audio amp.
28      Vdd     12VDC.
```

## U7 - 906107-01 — 6510 MICROPROCESSOR

```
   O1-+ 1     40+-_RES
  RDY-+ 2     39+-O2
 _IRQ-+ 3     38+-R/_W
 _NMI-+ 4     37+-DB0
  AEC-+ 5     36+-DB1
  VCC-+ 6     35+-DB2
   A0-+ 7     34+-DB3
   A1-+ 8     33+-DB4
   A2-+ 9     32+-DB5
   A3-+10     31+-DB6
   A4-+11     30+-DB7
   A5-+12     29+-P0
   A6-+13     28+-P1
   A7-+14     27+-P2
   A8-+15     26+-P3
   A9-+16     25+-P4
  A10-+17     24+-P5
  A11-+18     23+-A15
  A12-+19     22+-A14
  A13-+20     21+-GND
```

```
1       O1      Phase 1 clock input. This clock input is used to develop the
                internal overlapping phase 2 clock. 1MegHz or 2 MegHz speeds.
2       RDY     Single step operation input. A low applied will cause the
                processor to halt. The current address line being fetched will
                be on the address bus. Can also be used to interface slower
                devices to the microprocessor.
3       IRQ     Interrupt request input. When a low pulse is applied a jump to a
                location specified by the contents of FFFE and FFFF will occur
                to service the interrupt, if the interrupt mask flag is not set.
                This is a maskable interrupt.
4       NMI     Non-maskable interrupt input. A low transition will cause a jump
                to a location specified by FFFA and FFFB to a subroutine which
                will service the interrupt.
5       AEC     Address enable control input. A low applied to will cause the
                address bus to enter hi impedance state, so other devices can
                control the address bus.
6       VCC     5VDC input.
7-20    A0-A15  Address bus outputs.
22,23           Unidirectional bus used to address memory and I/O devices. The
                address bus can be disabled by controlling the AEC input.
21      GND     Dc ground connection.
24-29   P0-P5   I/O bidirectional port. This port can be controlled via memory
                locations 0000 and 0001.
                0001 = Output register
                0000 = Data direction register
30-37   DB0-DB7 Bidirectional data bus. This is the bus that passes the data to
                or from any I/O device or memory.
38      R/W     Read/Write output. The processor generates a low level when
                writing, and a high level when reading. This signal is usually
                decoded for read or write operations to memory or I/O.
39      O2      Phase 2 output. The processor generates this clock signal from
                the phase 1 clock applied. The two clock signals are 180 degrees
                out of the phase. The phase 2 clock is used in decoding I/O and
                memory on the positive half cycle.
40      RES     Reset input interrupt. A low pulse causes a jump to a subroutine
                specified by FFFC and FFFD, which will initialize the all
                processor controlled devices. This occurs during a power up
                sequence.
```

## U17 - 906114-01 — PROGRAMMABLE LOGIC ARRAY (PLA)

```
  PE+ -+ 1     28+-VCC
   I7-+ 2     27+-I8
   I6-+ 3     26+-I9
   I5-+ 4     25+-I10
   I4-+ 5     24+-I11
   I3-+ 6     23+-I12
   I2-+ 7     22+-I13
   I1-+ 8     21+-I14
   I0-+ 9     20+-I15
   F7-+10     19+-CE
   F6-+11     18+-F0
   F5-+12     17+-F1
   F4-+13     16+-F2
  GND-+14     15+-F3
```

(See `pla-82s100-datasheet.md` for the 82S100 part itself; the C64-specific
input/output assignments and the banking logic equations live in
**c64-memory-map**.)

## U19 - 906109-01 — 6567 VIDEO INTERFACE CHIP II (VIC II)

```
                            DB6-+ 1      40+-VCC
                            DB5-+ 2      39+-DB7
                            DB4-+ 3      38+-DB8
                            DB3-+ 4      37+-DB9
                            DB2-+ 5      36+-DB10
                            DB1-+ 6      35+-DB11
                            DB0-+ 7      34+-A10
                           _IRQ-+ 8      33+-A9
                             LP-+ 9      32+-A8
                            _CS-+10      31+-A7
                           R/_W-+11      30+-A6 ("1")
                             BA-+12      29+-A5
                            VDD-+13      28+-A4
                          COLOR-+14      27+-A3
                       SYNC/LUM-+15      26+-A2
                            AEC-+16      25+-A1
                            PH0-+17      24+-A0
                           _RAS-+18      23+-A11
                           _CAS-+19      22+-PHIN
                            VSS-+20      21+-PHCL
                                MULTIPLEXED
                          ADDRESSES IN PARENTHESES
```

```
1-7/39  DB0-DB7 Processor data bus connections. Bidirectional data.
8       IRQ     Interrupt output. Generates a interrupt signal to the processor
                indicating service is needed. The light pen input can be
                acknowledged thru use of this interrupt.
10      CS      Chip select input. A low signal selects the VIC II.
11      R/W     Processor read/write connection.
12      BA      Bus available output. A low pulse output indicates the VIC II
                chip wants control of the processor network to process faster
                video operations that the system clock can handle.
13      VDD     12VDC input.
14      COLOR   Output contains chrominance, color reference burst, and color of
                display data.
15      SYNC/   Output containing video, horizontal and vertical sync, and
        LUM     luminance information.
16      AEC     Address enable output. This is usually connected to the processor
                AEC input controlling the address bus.
                AEC = 0 processor address bus disabled, refresh ram.
                AEC = 1 processor address bus enabled. This allows transparent
                        system operations.
17      PH0     Phase 0 output. Generated from the phase in signal.
18      RAS     Row address strobe output. Selects proper row when addressing
                dynamic ram for read/write operations or refresh.
19      CAS     Column address strobe output. Selects proper column when
                addressing dynamic memory for read or write operation.
20      VSS     Ground connection.
21      PHCL    Color clock, 14.31818 MHZ NTSC.
22      PHIN    Clock input. Determines the dot transfer rate to the display.
23-24   A0-A13  Dual function address bus. During a microprocessor read or write
                operation (AEC = 1), A0 thru A5 are inputs used to address 47
                internal registers. When AEC = 0 = O2 is low, then A0 thru A13
                are outputs used to refresh dynamic memory.
35-38   D8-D11  Data bus extension. Color display memory data.
        A8-A11  Address bus extension. Color display memory addressing.
40      VCC     5VDC input.
```

## U9-12, U21-24 — 64K DYNAMIC RAM (901505-01)

```
                             NC-+ 1      16+-VSS
                            DIN-+ 2      15+-_CAS
                            _WE-+ 3      14+-DOUT
                           _RAS-+ 4      13+-A6
                             A0-+ 5      12+-A3
                             A2-+ 6      11+-A4
                             A1-+ 7      10+-A5
                            VCC-+ 8       9+-A7
```

```
+------------+------------+------------+--------+--------+--------+---------+
|COMMODORE   |APPROVED    |VENDOR      |ACCESS  |        |    POWER         |
|PART        |SOURCE      |PART        |TIME    |CYCLES  |ACTIVE  |STANDBY  |
|NUMBER      |OF SUPPLY   |NUMBER      |(ns)    |(ns)    |(MW)    |(MAX)(MW)|
+------------+------------+------------+--------+--------+--------+---------+
|901505-01   |HITACHI     |HM4864-3    |200     |335     |330     |20       |
|901505-01   |NEC         |uPD4164-2   |200     |375     |250     |28       |
|901505-01   |MITSUBISHI  |M5K416NS-20 |200     |330     |275     |28       |
|901505-01   |MOSTEK      |MK4564N-20  |200     |345     |300     |22       |
|901505-01   |OKI         |MSM3764-20  |200     |330     |248     |23       |
|901505-01   |HITACHI     |HM4864P-3   |200     |335     |330     |20       |
|901505-01   |MATSUSHITA  |MN4164P-20  |200     |330     |275     |27.5     |
|            |(PANASONIC) |            |        |        |        |         |
|901505-01   |SIEMENS     |HYB4164-3   |200     |330     |150     |20       |
|901505-01   |SHARP       |LH2164-Z1   |200     |330     |248     |28       |
|901505-01   |HITACHI     |HM4864AP-3  |200     |330     |242     |20       |
|901505-01   |TOSHIBA     |TMM4164AP-20|200     |330     |275     |22       |
+------------+------------+------------+--------+--------+--------+---------+
```

[Figure: DRAM functional diagram]
