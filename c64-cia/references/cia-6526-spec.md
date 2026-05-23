> Source: c64prg.txt §Appendix M "6526 Complex Interface Adapter (CIA) Chip Specifications". Lightly cleaned from the Project 64 etext.

  6526 COMPLEX INTERFACE ADAPTER
  (CIA) CHIP SPECIFICATIONS

  DESCRIPTION

    The 6526 Complex Interface Adapter (CIA) is a 65XX bus compatible
  peripheral interface device with extremely flexible timing and I/O
  capabilities.

  FEATURES

  o 16 Individually programmable 110 lines
  o 8 or 16-Bit handshaking on read or write
  o 2 independent, linkable 16-Bit interval timers
  o 24-hour (AM/PM) time of day clock with programmable alarm
  o 8-Bit shift register for serial I/O
  o 2 TTL load capability
  o CMOS compatible I/O lines
  o 1 or 2 MHz operation available

                              PIN CONFIGURATION

                                +----+ +----+
                       Vss   1 @|    +-+    |@ 40  CNT
                                |           |
                       PA0   2 @|           |@ 39  SP
                                |           |
                       PA1   3 @|           |@ 38  RS0
                                |           |
                       PA2   4 @|           |@ 37  RS1
                                |           |
                       PA3   5 @|           |@ 36  RS2
                                |           |
                       PA4   6 @|           |@ 35  RS3
                                |           |
                       PA5   7 @|           |@ 34  /RES
                                |           |
                       PA6   8 @|           |@ 33  D0
                                |           |
                       PA7   9 @|           |@ 32  D1
                                |           |
                       PB0  10 @|           |@ 31  D2
                                |    6526   |
                       PB1  11 @|           |@ 30  D3
                                |           |
                       PB2  12 @|           |@ 29  D4
                                |           |
                       PB3  13 @|           |@ 28  D5
                                |           |
                       PB4  14 @|           |@ 27  D6
                                |           |
                       PB5  15 @|           |@ 26  D7
                                |           |
                       PB6  16 @|           |@ 25  02
                                |           |
                       PB7  17 @|           |@ 24  /FLAG
                                |           |
                       /PC  18 @|           |@ 23  /CS
                                |           |
                       TOD  19 @|           |@ 22  R/W
                                |           |
                       Vcc  20 @|           |@ 21  /IRQ
                                +-----------+

                             6526 BLOCK DIAGRAM

                          [THE PICTURE IS MISSING!]

  MAXIMUM RATINGS

  Supply Voltage, Vcc                   -0.3V to +7.0V
  Input/Output Voltage, Vin             -0.3V to +7.0V
  Operating Temperature, Top             0 to 70 Celsius
  Storage Temperature, Tstg             -55 to 150 Celsius

    All inputs contain protection circuitry to prevent damage due to high
  static discharges. Care should be exercised to prevent unnecessary ap-
  plication of voltages in excess of the allowable limits.

  COMMENT

    Stresses above those listed under "Absolute Maximum Ratings" may cause
  permanent damage to the device. These are stress ratings oily. Functional
  operation of this device at these or any other conditions above those
  indicated in the operational sections of this specification is not
  implied and exposure to absolute maximum rating conditions for extended
  periods may affect device reliability.

  ELECTRICAL CHARACTERISTICS (Vcc +-5%, Vss=0V, Ta=0-70 Celsius)

  +-------------------------------+--------+-------+-------+-------+------+
  | CHARACTERISTIC                | SYMBOL | MIN.  | TYP.  | MAX.  | UNIT |
  +-------------------------------+--------+-------+-------+-------+------+
  | Input High Voltage            |  Vih   | +2.4  |   -   |  Vcc  |   V  |
  +-------------------------------+--------+-------+-------+-------+------+
  | Input Low Voltage             |  Vil   | -0.3  |   -   |   -   |   V  |
  +-------------------------------+--------+-------+-------+-------+------+
  | Input Leakage Current;        |  Iin   |   -   |  1.0  |  2.5  |  uA  |
  | Vin=Vss+5V                    |        |       |       |       |      |
  | (TOD, R/W, /FLAG, 02,         |        |       |       |       |      |
  | /RES, RS0-RS3, /CS)           |        |       |       |       |      |
  +-------------------------------+--------+-------+-------+-------+------+

  +-------------------------------+--------+-------+-------+-------+------+
  | CHARACTERISTIC                | SYMBOL | MIN.  | TYP.  | MAX.  | UNIT |
  +-------------------------------+--------+-------+-------+-------+------+
  | Port Input Pull-up Resistance |  Rpi   |  3.1  |  5.0  |   -   | kohms|
  +-------------------------------+--------+-------+-------+-------+------+
  | Output Leakage Current for    |  Itsi  |   -   |+-1.0  |+-10.0 |  uA  |
  | High Impedance State (Three   |        |       |       |       |      |
  | State); Vin=4V to 2.4V;       |        |       |       |       |      |
  | (D0-D7, SP, CNT, /IRQ)        |        |       |       |       |      |
  +-------------------------------+--------+-------+-------+-------+------+
  | Output High Voltage           |  Voh   | +2.4  |   -   |  Vcc  |   V  |
  | Vcc=MIN, Iload <              |        |       |       |       |      |
  | -200uA (PA0-PA7, /PC,         |        |       |       |       |      |
  | PB0-PB7, D0-D7)               |        |       |       |       |      |
  +-------------------------------+--------+-------+-------+-------+------+
  | Output Low Voltage            |  Vol   |   -   |   -   | +0.40 |   V  |
  | Vcc=MIN, Iload < 3.2 mA       |        |       |       |       |      |
  +-------------------------------+--------+-------+-------+-------+------+
  | Output High Current (Sourcing)|  Ioh   | -200  | -1000 |   -   |  uA  |
  | Voh > 2.4V (PA0-PA7,          |        |       |       |       |      |
  | PB0-PB7, /PC, D0-D7           |        |       |       |       |      |
  +-------------------------------+--------+-------+-------+-------+------+
  | Output Low Current (Sinking); |  Iol   |  3.2  |   -   |   -   |  mA  |
  | Vol <  .4V (PA0-PA7, /PC,     |        |       |       |       |      |
  | PB0-PB7, D0-D7                |        |       |       |       |      |
  +-------------------------------+--------+-------+-------+-------+------+
  | Input Capacitance             |  Cin   |   -   |    7  |   10  |  pf  |
  +-------------------------------+--------+-------+-------+-------+------+
  | Output Capacitance            |  Cout  |   -   |    7  |   10  |  pf  |
  +-------------------------------+--------+-------+-------+-------+------+
  | Power Supply Current          |  Icc   |   -   |   70  |  100  |  mA  |
  +-------------------------------+--------+-------+-------+-------+------+

                         6526 WRITE TIMING DIAGRAM

                          [THE PICTURE IS MISSING!]

                          6526 READ TIMING DIAGRAM

                          [THE PICTURE IS MISSING!]

  6526 INTERFACE SIGNALS

  02-Clock Input

    The 02 clock is a TTL compatible input used for internal device opera-
  tion and as a timing reference for communicating with the system data
  bus.

  /CS-Chip Select Input

    The /CS input controls the activity of the 6526. A low level on /CS
  while 02 is high causes the device to respond to signals on the R/W and
  address (RS) lines. A high on /CS prevents these lines from controlling
  the 6526. The /CS line is normally activated (low) at 02 by the
  appropriate address combination.

  R/W-Read/Write Input

    The R/W signal is normally supplied by the microprocessor and controls
  the direction of data transfers of the 6526. A high on R/W indicates
  a read (data transfer out of the 6526), while a low indicates a write
  (data transfer into the 6526).

  RS3-RS0-Address Inputs

    The address inputs select the internal registers as described by the
  Register Map.

  DB7-DB0-Data Bus Inputs/Outputs

    The eight data bus pins transfer information between the 6526 and the
  system data bus. These pins are high impedance inputs unless CS is low
  and R/W and 02 are high to read the device. During this read, the data
  bus output buffers are enabled, driving the data from the selected
  register onto the system data bus.

  IRQ-Interrupt Request Output

    IRQ is an open drain output normally connected to the processor inter-
  rupt input. An external pullup resistor holds the signal high, allowing
  multiple IRQ outputs to be connected together. The IRQ output is normally

  off (high impedance) and is activated low as indicated in the functional
  description.

  /RES-Reset Input

    A low on the RES pin resets all internal registers. The port pins are
  set as inputs and port registers to zero (although a read of the ports
  will return all highs because of passive pullups). The timer control
  registers are set to zero and the timer latches to all ones. All other
  registers are reset to zero.

                        6526 TIMING CHARACTERISTICS
  +--------+-----------------------+---------------+---------------+------+
  |        |                       |      1MHz     |      2MHz     |      |
  |        |                       +-------+-------+-------+-------+      |
  | Symbol |    Characteristic     |  MIN  |  MAX  |  MIN  |  MAX  | Unit |
  +--------+-----------------------+-------+-------+-------+-------+------+
  |        | 02 CLOCK              |       |       |       |       |      |
  | Tcyc   | Cycle Time            |  1000 |20,000 |   500 |20,000 |  ns  |
  | Tr, Tf | Rise and Fall Time    |   -   |    25 |   -   |    25 |  ns  |
  | Tchw   | Clock Pulse Width     |       |       |       |       |      |
  |        |   (High)              |   420 |10,000 |   200 |10,000 |  ns  |
  | Tclw   | Clock Pulse Width     |       |       |       |       |      |
  |        |   (Low)               |   420 |10,000 |   200 |10,000 |  ns  |
  +--------+-----------------------+-------+-------+-------+-------+------+
  |        | WRITE CYCLE           |       |       |       |       |      |
  | Tpd    | Output Delay From 02  |    -  |  1000 |   -   |   500 |  ns  |
  | Twcs   | /CS low while 02 high |   420 |   -   |   200 |   -   |  ns  |
  | Tads   | Address Setup Time    |     0 |   -   |     0 |   -   |  ns  |
  | Tadh   | Address Hold Time     |    10 |   -   |     5 |   -   |  ns  |
  | Trws   | R/W Setup Time        |     0 |   -   |     0 |   -   |  ns  |
  | Trwh   | R/W Hold Time         |     0 |   -   |     0 |   -   |  ns  |
  | Tds    | Data Bus Setup Time   |   150 |   -   |    75 |   -   |  ns  |
  | Tdh    | Data Bus Hold Time    |     0 |   -   |     0 |   -   |  ns  |
  +--------+-----------------------+-------+-------+-------+-------+------+
  |        | READ CYCLE            |       |       |       |       |      |
  | Tps    | Port Setup Time       |   300 |   -   |   150 |   -   |  ns  |
  | Twcs(2)| /CS low while 02 high |   420 |   -   |    20 |   -   |  ns  |
  | Tads   | Address Setup Time    |     0 |   -   |     0 |   -   |  ns  |
  | Tadh   | Address Hold Time     |    10 |   -   |     5 |   -   |  ns  |
  | Trws   | R/W Setup Time        |     0 |   -   |     0 |   -   |  ns  |
  | Trwh   | R/W Hold Time         |     0 |   -   |     0 |   -   |  ns  |

  +--------+-----------------------+---------------+---------------+------+
  |        |                       |      1MHz     |      2MHz     |      |
  |        |                       +-------+-------+-------+-------+      |
  | Symbol |    Characteristic     |  MIN  |  MAX  |  MIN  |  MAX  | Unit |
  +--------+-----------------------+-------+-------+-------+-------+------+
  | Tacc   | Data Access from      |       |       |       |       |      |
  |        | RS3-RS0               |   -   |   550 |   -   |   275 |  ns  |
  | Tco(3) | Data Access from /CS  |   -   |   320 |   -   |   150 |  ns  |
  | Tdr    | Data Release Time     |    50 |   -   |    25 |   -   |  ns  |
  +--------+-----------------------+-------+-------+-------+-------+------+

  +-----------------------------------------------------------------------+
  | NOTES: 1 -All timings are referenced from Vil max and Vih min on      |
  | inputs and Vol max and Voh min on outputs.                            |
  |        2 -Twcs is measured from the later of 02 high or /CS low. /CS  |
  | must be low at least until the end of 02 high.                        |
  |        3 -Tco is measured from the later of 02 high or /CS low.       |
  |        Valid data is available only after the later of Tacc or Tco.   |
  +-----------------------------------------------------------------------+

                                REGISTER MAP
  +---+---+---+---+---+----------+----------------------------------------+
  |RS3|RS2|RS1|RS0|REG|   NAME   |                                        |
  +---+---+---+---+---+----------+----------------------------------------+
  | 0 | 0 | 0 | 0 | 0 | PRA      |  PERIPHERAL DATA REG A                 |
  | 0 | 0 | 0 | 1 | 1 | PRB      |  PERIPHERAL DATA REG B                 |
  | 0 | 0 | 1 | 0 | 2 | DDRA     |  DATA DIRECTION REG A                  |
  | 0 | 0 | 1 | 1 | 3 | DDRB     |  DATA DIRECTION REG B                  |
  | 0 | 1 | 0 | 0 | 4 | TA LO    |  TIMER A LOW REGISTER                  |
  | 0 | 1 | 0 | 1 | 5 | TA HI    |  TIMER A HIGH REGISTER                 |
  | 0 | 1 | 1 | 0 | 6 | TB LO    |  TIMER B LOW REGISTER                  |
  | 0 | 1 | 1 | 1 | 7 | TB HI    |  TIMER B HIGH REGISTER                 |
  | 1 | 0 | 0 | 0 | 8 | TOD 10THS|  10THS OF SECONDS REGISTER             |
  | 1 | 0 | 0 | 1 | 9 | TOD SEC  |  SECONDS REGISTER                      |
  | 1 | 0 | 1 | 0 | A | TOD MIN  |  MINUTES REGISTER                      |
  | 1 | 0 | 1 | 1 | B | TOD HR   |  HOURS-AM/PM REGISTER                  |
  | 1 | 1 | 0 | 0 | C | SDR      |  SERIAL DATA REGISTER                  |
  | 1 | 1 | 0 | 1 | 0 | ICR      |  INTERRUPT CONTROL REGISTER            |
  | 1 | 1 | 1 | 0 | E | CRA      |  CONTROL REG A                         |
  | 1 | 1 | 1 | 1 | F | CRB      |  CONTROL REG B                         |
  +---+---+---+---+---+----------+----------------------------------------+

  6526 FUNCTIONAL DESCRIPTION

  I/O Ports (PRA, PRB, DDRA, DDRB).

    Ports A and B each consist of an 8-bit Peripheral Data Register (PR)
  and an 8-bit Data Direction Register (DDR). If a bit in the DDR is set to
  a one, the corresponding bit in the PR is an output; if a DDR bit is set
  to a zero, the corresponding PR bit is defined as an input. On a READ,
  the PR reflects the information present on the actual port pins (PA0-PA7,
  PB0-PB7) for both input and output bits. Port A and Port B have passive
  pull-up devices as well as active pull-ups, providing both CMOS and TTL
  compatibility. Both ports have two TTL load drive capability. In addition
  to normal I/O operation, PB6 and PB7 also provide timer output functions.

  Handshaking

    Handshaking on data transfers can be accomplished using the /PC output
  pin and the FLAG input pin. PC will go low for one cycle following a read
  or write of PORT B. This signal can be used to indicate "data ready" at
  PORT B or "data accepted" from PORT B. Handshaking on 16-bit data
  transfers (using both PORT A and PORT B) is possible by always reading or
  writing PORT A first. /FLAG is a negative edge sensitive input which can
  be used for receiving the /PC output from another 6526, or as a general
  purpose interrupt input. Any negative transition of /FLAG will set the
  /FLAG interrupt bit.
  +-----+---------+------+------+------+------+------+------+------+------+
  | REG |  NAME   |  D7  |  D6  |  D5  |  D4  |  D3  |  D2  |  D1  |  D0  |
  +-----+---------+------+------+------+------+------+------+------+------+
  |  0  |   PRA   |  PA7 |  PA6 |  PA5 |  PA4 |  PA3 |  PA2 |  PA1 |  PA0 |
  |  1  |   PRB   |  PB7 |  PB6 |  PB5 |  PB4 |  PB3 |  PB2 |  PB1 |  PB0 |
  |  2  |  DDRA   | DPA7 | DPA6 | DPA5 | DPA4 | DPA3 | DPA2 | DPA1 | DPA0 |
  |  3  |  DDRB   | DPB7 | DPB6 | DPB5 | DPB4 | DPB3 | DPB2 | DPB1 | DPB0 |
  +-----+---------+------+------+------+------+------+------+------+------+

  Interval Timers (Timer A, Timer B)

    Each interval timer consists of a 16-bit read-only Timer Counter and a
  16-bit write-only Timer Latch. Data written to the timer are latched in
  the Timer Latch, while data read from the timer are the present contents
  of the Time Counter. The timers can be used independently or linked for
  extended operations. The various timer modes allow generation of long
  time delays, variable width pulses, pulse trains and variable frequency

  waveforms. Utilizing the CNT input, the timers can count external pulses
  or measure frequency, pulse width and delay times of external signals.
  Each timer has an associated control register, providing independent
  control of the following functions:

  Start/Stop

    A control bit allows the timer to be started or stopped by the micro-
  processor at any time.

  PB On/Off:

    A control bit allows the timer output to appear on a PORT B output line
  (PB6 for TIMER A and PB7 for TIMER B). This function overrides the DDRB
  control bit and forces the appropriate PB line to an output.

  Toggle/Pulse

    A control bit selects the output applied to PORT B. On every timer
  underflow the output can either toggle or generate a single positive
  pulse of one cycle duration. The Toggle output is set high whenever the
  timer is started and is set low by /RES.

  One-Shot/Continuous

    A control bit selects either timer mode. In one-shot mode, the timer
  will count down from the latched value to zero, generate an interrupt,
  reload the latched value, then stop. In continuous mode, the timer will
  count from the latched value to zero, generate' an interrupt, reload the
  latched value and repeat the procedure continuously.

  Force Load

    A strobe bit allows the timer latch to be loaded into the timer counter
  at any time, whether the timer is running or not.

  Input Mode:

    Control bits allow selection of the clock used to decrement the timer.
  TIMER A can count 02 clock pulses or external pulses applied to the CNT
  pin. TIMER B can count (02 pulses, external CNT pulses, TIMER A underflow
  pulses or TIMER A underflow pulses while the CNT pin is held high.

    The timer latch is loaded into the timer on any timer underflow, on a
  force load or following a write to the high byte of the prescaler while
  the timer is stopped. If the timer is running, a write to the high byte
  will load the timer latch, but not reload the counter.

  READ (TIMER)
    REG    NAME
  +-----+---------+------+------+------+------+------+------+------+------+
  |  4  |  TA LO  | TAL7 | TAL6 | TAL5 | TAL4 | TAL3 | TAL2 | TAL1 | TAL0 |
  |  5  |  TA HI  | TAH7 | TAH6 | TAH5 | TAH4 | TAH3 | TAH2 | TAH1 | TAH0 |
  |  6  |  TB LO  | TBL7 | TBL6 | TBL5 | TBL4 | TBL3 | TBL2 | TBL1 | TBL0 |
  |  7  |  TB HI  | TBH7 | TBH6 | TBH5 | TBH4 | TBH3 | TBH2 | TBH1 | TBH0 |
  +-----+---------+------+------+------+------+------+------+------+------+
  WRITE (PRESCALER)
    REG    NAME
  +-----+---------+------+------+------+------+------+------+------+------+
  |  4  |  TA LO  | PAL7 | PAL6 | PAL5 | PAL4 | PAL3 | PAL2 | PAL1 | PAL0 |
  |  5  |  TA HI  | PAH7 | PAH6 | PAH5 | PAH4 | PAH3 | PAH2 | PAH1 | PAH0 |
  |  6  |  TB LO  | PBL7 | PBL6 | PBL5 | PBL4 | PBL3 | PBL2 | PBL1 | PBL0 |
  |  7  |  TB HI  | PBH7 | PBH6 | PBH5 | PBH4 | PBH3 | PBH2 | PBH1 | PBH0 |
  +-----+---------+------+------+------+------+------+------+------+------+

  Time of Day Clock (TOD)

    The TOD clock is a special purpose timer for real-time applications.
  TOD consists of a 24-hour (AM/PM) clock with 1/10th second resolution. It
  is organized into 4 registers: 10ths of seconds, Seconds, Minutes and
  Hours. The AM/PM flag is in the MSB of the Hours register for easy bit
  testing. Each register reads out in BCD format to simplify conversion for
  driving displays, etc. The clock requires an external 60 Hz or 50 Hz
  (programmable) TTL level input on the TOD pin for accurate time-keeping.
  In addition to time-keeping, a programmable ALARM is provided for
  generating an interrupt at a desired time. The ALARM registers or located
  at the same addresses as the corresponding TOD registers. Access to the
  ALARM is governed by a Control Register bit. The ALARM is write-only; any
  read of a TOD address will read time regardless of the state of the ALARM
  access bit.
    A specific sequence of events must be followed for proper setting and
  reading of TOD. TOD is automatically stopped whenever a write to the
  Hours register occurs. The clock will not start again until after a write
  to the 10ths of seconds register. This assures TOD will always start at
  the desired time. Since a carry from one stage to the next can occur at

  any time with respect to a read operation, a latching function is
  included to keep all Time Of Day information constant during a read
  sequence. All four TOD registers latch on a read of Hours and remain
  latched until after a read of 10ths of seconds. The TOD clock continues
  to count when the output registers are latched. If only one register is
  to be read, there is no carry problem and the register can be read "on
  the fly," provided that any read of Hours is followed by a read of 10ths
  of seconds to disable the latching.

  READ
    REG    NAME
  +-----+---------+------+------+------+------+------+------+------+------+
  |  8  |TOD 10THS|  0   |  0   |  0   |  0   |  T8  |  T4  |  T2  |  T1  |
  |  9  |TOD SEC  |  0   |  SH4 |  SH2 |  SH1 |  SL8 |  SL4 |  SL2 |  SL1 |
  |  A  |TOD MIN  |  0   |  MH4 |  MH2 |  MH1 |  ML8 |  ML4 |  ML2 |  ML1 |
  |  B  |TOD HR   |  PM  |  0   |  0   |  HH  |  HL8 |  HL4 |  HL2 |  HL1 |
  +-----+---------+------+------+------+------+------+------+------+------+

  WRITE

  CRB7=0 TOD
  CRB7=1 ALARM
  (SAME FORMAT AS READ)

  Serial Port (SDR)

    The serial port is a buffered, 8-bit synchronous shift register system.
  A control bit selects input or output mode. In input mode, data on the SP
  pin is shifted into the shift register on the rising edge of the signal
  applied to the CNT pin. After 8 CNT pulses, the data in the shift
  register is dumped into the Serial Data Register and an interrupt is
  generated. In the output mode, TIMER A is used for the baud rate
  generator. Data is shifted out on the SP pin at 1/2 the underflow rate of
  TIMER A. The maximum baud rate possible is 02 divided by 4, but the
  maximum useable baud rate will be determined by line loading and the
  speed at which the receiver responds to input data. Transmission will
  start following a write to the Serial Data Register (provided TIMER A is
  running and in continuous mode). The clock signal derived from TIMER A
  appears as an output on the CNT pin. The data in the Serial Data Register
  will be loaded into the shift register then shift out to the SP pin when
  a CNT pulse occurs. Data shifted out becomes valid on the falling edge of
  CNT and remains valid until the next falling edge. After 8 CNT pulses, an

  interrupt is generated to indicate more data can be sent. If the Serial
  Data Register was loaded with new information prior to this interrupt,
  the new data will automatically be loaded into the shift register and
  transmission will continue. If the microprocessor stays one byte ahead of
  the shift register, transmission will be continuous. If no further data
  is to be transmitted, after the 8th CNT pulse, CNT will return high and
  SP will remain at the level of the last data bit transmitted. SDR data is
  shifted out MSB first and serial input data should also appear in this
  format.
    The bidirectional capability of the Serial Port and CNT clock allows
  many 6526 devices to be connected to a common serial communication bus on
  which one 6526 acts as a master, sourcing data and shift clock, while all
  other 6526 chips act as slaves. Both CNT and SP outputs are open drain to
  allow such a common bus. Protocol for master/slave selection can be
  transmitted over the serial bus, or via dedicated handshaking lines.

    REG    NAME
  +-----+---------+------+------+------+------+------+------+------+------+
  |  C  |   SDR   |  S7  |  S6  |  S5  |  S4  |  S3  |  S2  |  S1  |  S0  |
  +-----+---------+------+------+------+------+------+------+------+------+

  Interrupt Control (ICR)

    There are five sources of interrupts on the 6526: underflow from TIMER
  A, underflow from TIMER B, TOD ALARM, Serial Port full/empty and /FLAG.
  A single register provides masking and interrupt information. The
  interrupt Control Register consists of a write-only MASK register and a
  read-only DATA register. Any interrupt will set the corresponding bit in
  the DATA register. Any interrupt which is enabled by the MASK register
  will set the IR bit (MSB) of the DATA register and bring the /IRQ pin
  low. In a multi-chip system, the IR bit can be polled to detect which
  chip has generated an interrupt request. The interrupt DATA register is
  cleared and the /IRQ line returns high following a read of the DATA
  register. Since each interrupt sets an interrupt bit regardless of the
  MASK, and each interrupt bit can be selectively masked to prevent the
  generation of a processor interrupt, it is possible to intermix polled
  interrupts with true interrupts. However, polling the IR bit will cause
  the DATA register to clear, therefore, it is up to the user to preserve
  the information contained in the DATA register if any polled interrupts
  were present.
    The MASK register provides convenient control of individual mask bits.
  When writing to the MASK register, if bit 7 (SET/CLEAR) of the data

  written is a ZERO, any mask bit written with a one will be cleared, while
  those mask bits written with a zero will be unaffected. If bit 7 of the
  data written is a ONE, any mask bit written with a one will be set, while
  those mask bits written with a zero will be unaffected. In order for an
  interrupt flag to set IR and generate an Interrupt Request, the corre-
  sponding MASK bit must be set.

  READ (INT DATA)
    REG    NAME
  +-----+---------+------+------+------+------+------+------+------+------+
  |  D  |   ICR   |  IR  |   0  |   0  |  FLG |  SP  | ALRM |  TB  |  TA  |
  +-----+---------+------+------+------+------+------+------+------+------+

  WRITE (INT MASK)
    REG    NAME
  +-----+---------+------+------+------+------+------+------+------+------+
  |  D  |   ICR   |  S/C |   X  |   X  |  FLG |  SP  | ALRM |  TB  |  TA  |
  +-----+---------+------+------+------+------+------+------+------+------+

  CONTROL REGISTERS

    There are two control registers in the 6526, CRA and CRB. CRA is
  associated with TIMER A and CRB is associated with TIMER B. The register
  format is as follows:

  CRA:
  Bit  Name    Function
   0  START    1=START TIMER A, 0=STOP TIMER A. This bit is automatically
               reset when underflow occurs during one-shot mode.
   1  PBON     1=TIMER A output appears on PB6, 0=PB6 normal operation.

   2  OUTMODE  1=TOGGLE, 0=PULSE
   3  RUNMODE  1=ONE-SHOT, 0=CONTINUOUS
   4  LOAD     1=FORCE LOAD (this is a STROBE input, there is no data
               storage, bit 4 will always read back a zero and writing a
               zero has no effect).
   5  INMODE   1=TIMER A counts positive CNT transitions, 0=TIMER A counts
               02 pulses.
   6  SPMODE   1=SERIAL PORT output (CNT sources shift clock),
               0=SERIAL PORT input (external shift clock required).
   7  TODIN    1=50 Hz clock required on TOD pin for accurate time,
               0=60 Hz clock required on TOD pin for accurate time.

  CRB:
  Bit  Name    Function
               (Bits CRB0-CRB4 are identical to CRA0-CRA4 for TIMER B with
               the exception that bit 1 controls the output of TIMER B on
               PB7).
  5,6 INMODE   Bits CRB5 and CRB6 select one of four input modes for
               TIMER B as:
               CRB6   CRB5
                0      0       TIMER B counts 02 pulses.
                0      1       TIMER B counts positive CNT transistions.
                1      0       TIMER B counts TIMER A underflow pulses.
                1      1       TIMER B counts TIMER A underflow pulses
                               while CNT is high.
  7   ALARM     1=writing to TOD registers sets ALARM, 0=writing to TOD
                registers sets TOD clock.

  REGNAME TODIN SP MODE IN MODE   LOAD  RUN MODE OUT MODE   PB ON   START
  +-+---+------+-------+-------+--------+-------+--------+--------+-------+
  |E|CRA|0=60Hz|0=INPUT| 0=02  |1=FORCE |0=CONT.|0=PULSE |0=PB6OFF|0=STOP |
  | |   |      |       |       |  LOAD  |       |        |        |       |
  | |   |1=50Hz|1=OUTP.| 1=CNT |(STROBE)|1=O.S. |1=TOGGLE|1=PB6ON |1=START|
  +-+---+------+-------+-------+--------+-------+--------+--------+-------+
                       +------------------ TA ----------------------------+

  REGNAME ALARM    IN MODE        LOAD  RUN MODE OUT MODE   PB ON   START
  +-+---+------+------+--------+--------+-------+--------+--------+-------+
  |E|CRB|0=TOD |   0  |0=02    |1=FORCE |0=CONT.|0=PULSE |0=PB7OFF|0=STOP |
  | |   |      |   1  |1=CNT   |LOAD    |       |        |        |       |
  | |   |1=    |   1  |0=TA    |        |       |        |        |       |
  | |   | ALARM|   1  |1=CNT&TA|(STROBE)|1=O.S. |1=TOGGLE|1=PB7ON |1=START|
  +-+---+------+------+--------+--------+-------+--------+--------+-------+
               +-------------------------- TB ----------------------------+

  All unused register bits are unaffected by a write and are forced to zero
  on a read.
  +-----------------------------------------------------------------------+
  | COMMODORE SEMICONDUCTOR GROUP reserves the right to make changes to   |
  | any products herein to improve reliability, function or design.       |
  | COMMODORE SEMICONDUCTOR GROUP does not assume any liability arising   |
  | out of the application or use of any product or circuit described     |
  | herein; neither does it convey any license under its patent rights nor|
  | the rights of others.                                                 |
  +-----------------------------------------------------------------------+
