> Source: C64ServiceManual.txt, "C64 CIRCUIT THEORY" sections (Power Supply, Reset Logic, Clock Circuits, I/O+ROM+Expansion Logic, RAM Control Logic, 5/8-pin Video & Audio Outputs, Cassette Interface, Keyboard/Joystick/Paddle Interfaces, Serial Interface + User Port). Lightly cleaned from the Project 64 etext. Schematics were too complex to render as ASCII and are marked [Figure: ...]; consult original scans for trace-level work. The register-level programming of the VIC, SID and CIA chips lives in c64-vic-ii / c64-sid / c64-cia; the PLA banking logic lives in c64-memory-map.

# C64 CIRCUIT THEORY

```
+-------------------------------------------------------------------------+
| There are three versions of the C64. The C64 with five pine connector   |
| video output (326106). The C64 with an eight pin connector video output |
| (251138), and the C64B which has improved system clock circuit design   |
| (251469). Most circuit theory explanations will be the same for all     |
| three versions. Refer to schematic 326106 unless noted otherwise.       |
+-------------------------------------------------------------------------+
```

## The Power Supply

The external power supply generates a regulated 5VDC and 9VAC. 5VDC is applied
to pins 5 and 1 of CN7 on the C64 pcb. Filtered by L5, C97, and C100 it is then
controlled by on/off switch S1. This 5VDC output supplies the microprocessor
logic.

9VAC is applied to pins 6 and 7 of CN7 on the C64 pcb. +12VDC, +5VDC CAN and
9VAC unregulated are outputs that are derived from this 9VAC supply. The 9VAC
supply is made available on pins 10 and 11 of the USER PORT CN2.

### 12VDC Generation

9VAC is added to 9VDC through CR6, and rectified by CR5. The unregulated DC
output is filtered by C88 and C89 then regulated at 12VDC by VR1. The regulated
output is filtered by C57 and C59. The 12VDC supplies the VIC and SID IC, and
the audio amplifiers.

### +5VDC CAN Generation

9VAC is rectified by CR4. The unregulated DC output is filtered by C19, and C95
then regulated at 5VDC by VR2. The regulated output is filtered by C102 and
C103. The output called 5VDC CAN is separated and individually filtered into two
outputs called Vvid and Vc. Vvid is the 5VDC supply for video circuits, and Vc
is the 5VDC supply for the clock circuits.

### 9VDC Unregulated Generation

CR4 rectifies the 9VAC input. The output is 9VDC unregulated. This supply powers
the cassette motor transistor amplifier circuits, and the RF modulator on the
C64B version.

[Figure: Power Supply Circuits]

## Reset Logic Circuits

[Figure: Reset Circuit schematic]

U20 is a 556 timer configured as a one shot multivibrator. The output pulse
width is determined by the size of R34 and C24. Pulse width = 1.1 x R34 x
C24 = .5 seconds. The output on pin 9 is "high" active. The output of U8 is
"low" active. Reset initializes all the processor logic and causes the
processor to load the program counter register with the address of the
first instruction of the operating system program called the KERNAL. The
starting address is stored in locations $FFFC and $FFFD. The first
instruction is decode and executed giving KERNAL control of the computer
operations. The reset pulse occurs when turning the power on to the
computer.

## The C64 Clock Circuits

[Figure: Clock circuit schematic]

Crystal Y1 develops a 14.31818MHz fundamental frequency clock signal. U31
is a Dual Voltage Controlled Oscillator. The output on pin 10 is a 14.31818
MHz clock signal called the color clock. R27 can be adjusted to obtain
exact output frequency. U30 is a frequency divider that outputs a 2MHz signal
on pin 6. U29 is a D flip flop which outputs a 1MHz signal on pin 9. U32 is
a Phase/Frequency Detector which compares the output of the U29 to the phase
0 clock, and outputs a dc voltage on pin 8 that is proportional to the phase
difference between the inputs. The second half of the Dual Voltage
Controller Oscillator U31 generates an 8.1818MHz clock signal called the
DOT Clock. The VIC IC divides the DOT clock by eight and outputs this as the
phase 0 clock on pin 17. The output of the Phase/Frequency Detector is
applied to the frequency control input pin 2 of U31. This causes tracking
of the dot clock and the color clock because one input, pin 4 of U32, is
the phase 0 clock which is derived from the dot clock, and the other pin 1
of U32, is derived from the color clock.

[Figure: Clock circuit (C64B) schematic]

### The C64B Clock Circuits. Refer to schematic 251469

Crystal Y1 develops the fundamental 16Mhz clock signal. U31 is a Clock
Generator IC that outputs the 8.1818MHz DOT clock on pin 6, and the
14.31818 MHz color clock on pin 8.

## I/O and ROM Address Decoding and Expansion Port

[Figure: I/O, ROM and expansion port schematic]

### I/O Address Decoding Logic

U17 is a Programmable logic array (PLA). The output F5 on pin 12 called I/O
goes "low" when any of the I/O devices controlled by U15 are selected. The
addresses are listed below for each device.

```
        VIC IC       $D000 - $D02E
        SID IC       $D400 - $D7FF
        Color Ram    $D800 - $DBFF
        CIA 1        $DC00 - $DC0F
        CIA 2        $DD00 - $DD0F
        I/O 1        $DE00 - $DEFF
        I/O 2        $DF00 - $DFFF
```

### ROM Address Decoding

Basic ROM resides at locations $A000 - $BFFF. The output F1 pin 17 of the
PLA U17 goes "low" when the BASIC ROM is selected. The KERNAL ROM resides
at locations $E000 - $FFFF. The output F2 pin 16 of the PLA U17 goes "low"
when the KERNAL ROM is selected. The CHARACTER GENERATOR ROM resides at
locations $D000 - $DFFF. The output F3 pin 15 of the PLA U17 goes "low"
when the Character Generator ROM is selected.

### The Expansion Port Connections

The expansion port is an extension of the microprocessor address, data, and
control bus. ROML decodes addresses $8000 - $9FFF, and ROMH decodes
addresses $E000 - $FFFF. These are outputs from the PLA used to select the
catridge inserted in the expansion port. I/O 1 input from U15 decodes
addresses $DE00 - $DEFF. I/O 2 output from U15 decodes addresses $DF00 -
$DFFF.

## RAM Control Logic

[Figure: RAM control logic schematic]

U13 and U25 are multiplexers. The address output from the microprocessor
are passed to RAM via U13 and U25 when the output Address Enable Control
(AEC) from the VIC IC is "high". When AEC is "low" the VIC IC outputs
refresh addresses on pins 24 - 31. AEC goes "low" when the system clock,
phase 2, is "low". Since all I/O decoding occurs when phase 2 is "high",
refresh is transparent to the processor.

Eight 4164 DRAMS provide 64k bytes of memory. One 2114 RAM (U6) provides
512 bytes of memory allocated for screen color data storage.

## 5 Pin Video and Audio Output Circuits

[Figure: 5 pin video and audio schematic]

Pin 15 of the VIC IC is the sync/luminance output. Pin 14 is the color
output. A composite video output is created by mixing sync/luminance and
color. The composite output is applied to the RF modulator, and also passed
to the monitor connector CN5 on pin 4. The color output is not made
available on the monitor connector CN5 as on the 8 pin version, and the RF
modulator mixes audio with the composite video producing the TV RF output,
unlike the 8 pin version RF modulator which creates the composite video
output.

## 8 Pin Video and Audio Output Circuits. Refer to schematic 21469

[Figure: 8 pin video and audio schematic]

U19 is the Video Interface Chip (VIC). Sync (horizontal and vertical), and
luminance (video) is output on pin 15. This signal is passed to pin 2 of
the RF modulator. Color is output on pin 14, and passed to pin 3 of the
modulator. Light pen inputs are sensed by the VIC IC on pin 9. U18 is the
Sound Interface Device (SID). The audio output is on pin 27, and audio
input is on pin 26. The RF modulator mixes sync/luminance, color, and audio
out, generating a TV composite signal on pin 5. The RF modulator also
passes the VIC outputs to the monitor connector CN5. Audio out on pin 27 is
amplified by Q2, and output on pin 3 of CN5. Audio in is applied to pin 5
of CN5, then to pin 26 of the SID IC. Inputs from paddles connected to on
of the control ports are monitored by the SID IC on pins 23 and 24.

## The Cassette Interface Circuits

[Figure: Cassette interface schematic]

U7 is a 6510 microprocessor. One of the features of the 6510 is a built in
parallel I/O port (P0-P5). P3 - P5 control most of the cassette interface
circuitry. P3 pin p6 of U7 outputs the write data signal to connector CN3
on pins E and 5. P4 is an input that senses the play switch depressed on the
cassette deck. P5 is on output that controls the cassette motor. When P5
goes "low", Q2 cuts off, CR2 regulates Vb of Q1 at 7.5 volts, this forward
biases Q1 and Q3, passing current through the cassette motor coil. U1 is a
Complex Interface Adapter (CIA). Parallel ports, serial outputs, and Timers
are standard features of the CIA. Read data enters on pins D, 4 of CN3. U1
accepts the read data signal on the FLAG input pin 24.

## Keyboard, Joystick, and Paddle Interface Circuits

[Figure: Interface control schematic]

### Keyboard Interface

U1 is a Complex Interface Adapter (CIA). Both parallel ports are used to
decode the keyswitches on the keyboard. Parallel port A signals (PA0 - PA7)
are outputs. PArallel port B signals (PB0 - PB7) are inputs. A "0" bin is
shifted through the parallel port A, when a key is depressed on the
keyboard the "0" bit is returned on one of the parallel port B inputs. A
program in the KERNAL ROM generates the shifting "0" bit output on parallel
port A, and decodes the signals returning on the parallel port B inputs.
Depressing the restore key causes U20 to trigger. U9 pin 6 goes "low"
generating a Non- Maskable Interrupt (NMI) at the processor. This causes
the processor to execute a subroutine which initializes the I/O interfaces.
If the STOP key is depressed at the same time, BASIC flags are initialized.

[Figure: Keyboard matrix]

### Joystick Interface

U1 also controls the joystick. Parallel port A accepts inputs from the B
joystick connected to control port 2. Parallel port B accepts inputs from
the A joystick connected to control port 1. When the joystick is moved up,
down, left, right, or the fire button is depressed, a ground potential is
applied to the appropriate input of U1.

### Paddle Interface

A Variable resistor is connected to adjusting knob on the paddle. When the
knob is rotated, the resistance varies controlling the time constant of an
RC network. The Voltage developed across the capacitor is input to an A/D
converter internal to the SID chip U18. The digital output is stored in one
of the SID registers. The paddle position can be determined by the reading
the contents of the appropriate register. U28 is a 4066 CMOS switch. The
signals from the paddles are passed to the SID chip when the Enable inputs
(E0 - E3) of U28 are "high".

NOTE: U1 port assignments are incorrect on schematics. Refer to Keyboard
      Matrix for correct assignments.

## The Serial Interface and User Port Circuits

[Figure: Serial interface schematic]

### The Serial Interface

U2 is a Complex Interface Adapter (CIA). Parallel port signals PA3-PA7
control the serial bus interface. PA3 is the Attention (ATN) output. This
signal is inverted by U8 before being transmitted to a device on the bus.
PA4 is the clock output. Data transmitted from the C64 to a device on the
bus is synchronized by this clock signal. U8 inverts the output PA4. PA5 is
the data output. U8 inverts this output also. Data transmitted from a device
on the bus to the C64 is synchronized by a clock generated by the
transmitting device. The Clock signal is input on PA6. Data transmitted
from a device on the bus to the C64 is input on PA7. When a device on the
bus wants to communicate with the C64, SQR IN goes "low" indicating service
is requested.

### The User Port

Parallel port B of U2 (PB0 - PB7) is made available on the user port.
Parallel data transfers with external device are made very easily through
this parallel port. SP2 and SP1 are bi-directional serial ports. CNT1 and
CNT2 are bi-directional synchronizing clock signals for each serial bus.
