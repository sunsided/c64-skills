> Source: c64prg.txt §Appendix L "6510 Microprocessor Chip Specifications". Lightly cleaned from the Project 64 etext.

  6510 MICROPROCESSOR CHIP
  SPECIFICATIONS

  DESCRIPTION

    The 6510 is a low-cost microcomputer system capable of solving a broad
  range of small-systems and peripheral-control problems at minimum cost to
  the user.
    An 8-bit Bi-Directional I/O Port is located on-chip with the Output
  Register at Address 0000 and the Data-Direction Register at Address 0001.
  The I/O Port is bit-by-bit programmable.
    The Three-State sixteen-bit Address Bus allows Direct Memory Accessing
  (DMA) and multiprocessor systems sharing a common memory.
    The internal processor architecture is identical to the MOS Technology
  6502 to provide software compatibility.

  FEATURES OF THE 6510...

  o Eight-Bit Bi-Directional I/O Port
  o Single +5-volt supply
  o N-channel, silicon gate, depletion load technology
  o Eight-bit parallel processing
  o 56 Instructions
  o Decimal and binary arithmetic
  o Thirteen addressing modes
  o True indexing capability
  o Programmable stack pointer
  o Variable length stack
  o Interrupt capability
  o Eight-Bit Bi-Directional Data Bus
  o Addressable memory range of up to 64K bytes
  o Direct memory access capability
  o Bus compatible with M6800
  o Pipeline architecture
  o 1-MHz and 2-MHz operation
  o Use with any type or speed memory

                              PIN CONFIGURATION

                                +----+ +----+
                     01 IN   1 @|    +-+    |@ 40  /RES
                                |           |
                       RDY   2 @|           |@ 39  02 IN
                                |           |
                      /IRQ   3 @|           |@ 38  R/W
                                |           |
                      /NMI   4 @|           |@ 37  D0
                                |           |
                       AEC   5 @|           |@ 36  D1
                                |           |
                       VCC   6 @|           |@ 35  D2
                                |           |
                        A0   7 @|           |@ 34  D3
                                |           |
                        A1   8 @|           |@ 33  D4
                                |           |
                        A2   9 @|           |@ 32  D5
                                |           |
                        A3  10 @|           |@ 31  D6
                                |    6510   |
                        A4  11 @|           |@ 30  D7
                                |           |
                        A5  12 @|           |@ 29  P0
                                |           |
                        A6  13 @|           |@ 28  P1
                                |           |
                        A7  14 @|           |@ 27  P2
                                |           |
                        A8  15 @|           |@ 26  P3
                                |           |
                        A9  16 @|           |@ 25  P4
                                |           |
                       A10  17 @|           |@ 24  P5
                                |           |
                       A11  18 @|           |@ 23  A15
                                |           |
                       A12  19 @|           |@ 22  A14
                                |           |
                       A13  20 @|           |@ 21  GND
                                +-----------+

                         [THE PICTURE IS MISSING!]

                             6510 BLOCK DIAGRAM

  6510 CHARACTERISTICS

  MAXIMUM RATINGS
  +--------------------------+------------+-----------------+-------------+
  |          RATING          |   SYMBOL   |      VALUE      |    UNIT     |
  +--------------------------+------------+-----------------+-------------+
  |  SUPPLY VOLTAGE          |    Vcc     |   -0.3 to +7.0  |     VDC     |
  |  INPUT VOLTAGE           |    Vin     |   -0.3 to +7.0  |     VDC     |
  |  OPERATING TEMPERATURE   |    Ta      |    0 to +70     |   Celsius   |
  |  STORAGE TEMPERATURE     |    Tstg    |   -55 to +150   |   Celsius   |
  +--------------------------+------------+-----------------+-------------+
  +-----------------------------------------------------------------------+
  | NOTE: This device contains input protection against damage due to high|
  | static voltages or electric fields; however, precautions should be    |
  | taken to avoid application of voltages higher than the maximum rating.|
  +-----------------------------------------------------------------------+

  ELECTRICAL CHARACTERISTICS  (VCC=5.0V +-5%, VSS=0, Ta=0 to +70 Celsius)
  +------------------------------------+--------+-------+---+-------+-----+
  |           CHARACTERISTIC           | SYMBOL |  MIN. |TYP|  MAX. |UNIT |
  +------------------------------------+--------+-------+---+-------+-----+
  | Input High Voltage                 |        |       |   |       |     |
  |   01, 02(in)                       |  Vih   |Vcc-0.2| - |Vcc+1.0| VDC |
  | Input High Voltage                 |        |       |   |       |     |
  | /RES, P0-P7, /IRQ, Data            |        |Vss+2.0| - |   -   | VDC |
  +------------------------------------+--------+-------+---+-------+-----+
  | Input Low Voltage                  |        |       |   |       |     |
  | 01,02(in)                          |  Vil   |Vss-0.3| - |Vss+0.2| VDC |
  | /RES, P0-P7, /IRQ, Data            |        |   -   | - |Vss+0.8| VDC |
  +------------------------------------+--------+-------+---+-------+-----+
  | Input Leakage Current              |        |       |   |       |     |
  |   (Vin=0 to 5.25V, Vcc=5.25V       |        |       |   |       |     |
  |   Logic                            |  Iin   |   -   | - |  2.5  |  uA |
  |   01, 02(in)                       |        |   -   | - |  100  |  uA |
  +------------------------------------+--------+-------+---+-------+-----+
  | Three State(Off State)Input Current|        |       |   |       |     |
  | (Vin=0.4 to 2.4V, Vcc=5.25V)       |        |       |   |       |     |
  |   Data Lines                       |  Itsi  |   -   | - |   10  |  uA |
  +------------------------------------+--------+-------+---+-------+-----+
  | Output High Voltage                |        |       |   |       |     |
  | (Ioh=-100uADC, Vcc=4.75V)          |        |       |   |       |     |
  |   Data, A0-A15, R/W, P0-P7         |  Voh   |Vss+2.4| - |   -   | VDC |
  +------------------------------------+--------+-------+---+-------+-----+

  +------------------------------------+--------+-------+---+-------+-----+
  |           CHARACTERISTIC           | SYMBOL |  MIN. |TYP|  MAX. |UNIT |
  +------------------------------------+--------+-------+---+-------+-----+
  | Out Low Voltage                    |        |       |   |       |     |
  | (Iol=1.6mADC, Vcc=4.75V)           |        |       |   |       |     |
  |   Data, A0-A15, R/W, P0-P7         |   Vol  |   -   | - |Vss+0.4| VDC |
  +------------------------------------+--------+-------+---+-------+-----+
  | Power Supply Current               |   Icc  |   -   |125|       |  mA |
  +------------------------------------+--------+-------+---+-------+-----+
  | Capacitance                        |   C    |       |   |       |  pF |
  | Vin=0, Ta=25 Celsius, f=1MHz)      |        |       |   |       |     |
  |   Logic, P0-P7                     |   Cin  |   -   | - |   10  |     |
  |   Data                             |        |   -   | - |   15  |     |
  |   A0-A15, R/W                      |   Cout |   -   | - |   12  |     |
  |   01                               |   C01  |   -   | 30|   50  |     |
  |   02                               |   C02  |   -   | 50|   80  |     |
  +------------------------------------+--------+-------+---+-------+-----+

                               CLOCK TIMING

                          [THE PICTURE IS MISSING!]

               TIMING FOR READING DATA FROM MEMORY OR PERIPHERALS

                                CLOCK TIMING

                         [THE PICTURE IS MISSING!]

               TIMING FOR WRITING DATA TO MEMORY OR PERIPHERALS

  AC CHARACTERISTICS

  ELECTRICAL CHARACTERISTICS (Vcc=5V +-5%, Vss=0V, Ta=0-70 Celsius)

        CLOCK TIMING                        1 MHz TIMING 2 MHz TIMING
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | CHARACTERISTIC                  |SYMBOL|MIN.|TYP|MAX|MIN|TYP|MAX|UNITS|
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | Cycle Time                      | Tcyc |1000| - | - |500| - | - | ns  |
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | Clock Pulse Width 01            |PWH01 | 430| - | - |215| - | - | ns  |
  | (Measured at Vcc-0.2V) 02       |PWH02 | 470| - | - |235| - | - | ns  |
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | Fall Time, Rise Time            |      |    |   |   |   |   |   |     |
  | (Measured from 0.2V to Vcc-0.2V)|Tf, Tr|  - | - | 25| - | - | 15| ns  |
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | Delay Time between Clocks       |      |    |   |   |   |   |   |     |
  | (Measured at 0.2V)              |  Td  |  0 | - | - | 0 | - | - | ns  |
  +---------------------------------+------+----+---+---+---+---+---+-----+

  READ/WRITE TIMING (LOAD=1TTL)             1 MHz TIMING 2 MHz TIMING
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | CHARACTERISTIC                  |SYMBOL|MIN.|TYP|MAX|MIN|TYP|MAX|UNITS|
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | Read/Write Setup Time from 6508 | Trws |  - |100|300| - |100|150| ns  |
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | Address Setup Time from 6508    | Tads |  - |100|300| - |100|150| ns  |
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | Memory Read Access Time         | Tacc |  - | - |575| - | - |300| ns  |
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | Data Stability Time Period      | Tdsu | 100| - | - | 50|   |   | ns  |
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | Data Hold Time-Read             | Thr  |    | - | - |   |   |   | ns  |
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | Data Hold Time-Write            | Thw  |  10| 30| - | 10| 30|   | ns  |
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | Data Setup Time from 6510       | Tmds |  - |150|200| - | 75|100| ns  |
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | Address Hold Time               | Tha  |  10| 30| - | 10| 30|   | ns  |
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | R/W Hold Time                   | Thrw |  10| 30| - | 10| 30|   | ns  |
  +---------------------------------+------+----+---+---+---+---+---+-----+

  +---------------------------------+------+----+---+---+---+---+---+-----+
  | Delay Time, Address valid to    |      |    |   |   |   |   |   |     |
  | 02 positive transition          | Taew | 180| - | - |   |   |   | ns  |
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | Delay Time, 02 positive         |      |    |   |   |   |   |   |     |
  | transition to Data valid on bus | Tedr |  - | - |395|   |   |   | ns  |
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | Delay Time, data valid to 02    |      |    |   |   |   |   |   |     |
  | negative transition             | Tdsu | 300| - | - |   |   |   | ns  |
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | Delay Time, R/W negative        |      |    |   |   |   |   |   |     |
  | transition to 02 positive trans.| Twe  | 130| - | - |   |   |   | ns  |
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | Delay Time, 02 negative trans.  |      |    |   |   |   |   |   |     |
  | to Peripheral data valid        | Tpdw |  - | - | 1 |   |   |   | us  |
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | Peripheral Data Setup Time      | Tpdsu| 300| - | - |   |   |   | ns  |
  +---------------------------------+------+----+---+---+---+---+---+-----+
  | Address Enable Setup Time       | Taes |    |   | 60|   |   | 60| ns  |
  +---------------------------------+------+----+---+---+---+---+---+-----+

  SIGNAL DESCRIPTION

  Clocks (01, 02)

    The 6510 requires a two-phase non-overlapping clock that runs at the
  Vcc voltage level.

  Address Bus (A0-A15)

    These outputs are TTL compatible, capable of driving one standard TTL
  load and 130 pf.

  Data Bus (D0-D7)

    Eight pins are used for the data bus. This is a Bi-Directional bus,
  transferring data to and from the device and peripherals. The outputs are
  tri-state buffers capable of driving one standard TTL load and 130 pf.

  Reset

    This input is used to reset or start the microprocessor from a power
  down condition. During the time that this line is held low, writing to or
  from the microprocessor is inhibited. When a positive edge is detected on
  the input, the microprocessor will immediately begin the reset sequence.
    After a system initialization time of six clock cycles, the mask
  interrupt flag will be set and the microprocessor will load the program
  counter from the memory vector locations FFFC and FFFD. This is the start
  location for program control.
    After Vcc reaches 4.75 volts in a power-up routine, reset must be held
  low for at least two clock cycles. At this time the R/W signal will
  become valid.
    When the reset signal goes high following these two clock cycles, the
  microprocessor will proceed with the normal reset procedure detailed
  above.

  Interrupt Request (/IRQ)

    This TTL level input requests that an interrupt sequence begin within
  the microprocessor. The microprocessor will complete the current in-
  struction being executed before recognizing the request. At that time,
  the interrupt mask bit in the Status Code Register will be examined. If
  the interrupt mask flag is not set, the microprocessor will begin an

  interrupt sequence. The Program Counter and Processor Status Register are
  stored in the stack. The microprocessor will then set the interrupt mask
  flag high so that no further interrupts may occur. At the end of this
  cycle, the program counter low will be loaded from address FFFE, and
  program counter high from location FFFF, therefore transferring program
  control to the memory vector located at these addresses.

  Address Enable Control (AEC)

    The Address Bus is valid only when the Address Enable Control line is
  high. When low, the Address Bus is in a high-impedance state. This
  feature allows easy DMA and multiprocessor systems.

  I/O Port (P0-P7)

    Six pins are used for the peripheral port, which can transfer data to
  or from peripheral devices. The Output Register is located in RAM at
  address 0001, and the Data Direction Register is at Address 0000. The
  outputs are capable at driving one standard TTL load and 130 pf.

  Read/Write (R/W)

    This signal is generated by the microprocessor to control the direction
  of data transfers on the Data Bus. This line is high except when the
  microprocessor is writing to memory or a peripheral device.

  ADDRESSING MODES

  ACCUMULATOR ADDRESSING - This form of addressing is represented with a
  one byte instruction, implying an operation on the accumulator.

  IMMEDIATE ADDRESSING - In immediate addressing, the operand is contained
  in the second byte of the instruction, with no further memory addressing
  required.

  ABSOLUTE ADDRESSING - In absolute addressing, the second byte of the
  instruction specifies the eight low order bits of the effective address
  while the third byte specifies the eight high order bits. Thus, the
  absolute addressing mode allows access to the entire 64K bytes of
  addressable memory.

  ZERO PAGE ADDRESSING - The zero page instructions allow for shorter code

  and execution times by only fetching the second byte of the instruction
  and assuming a zero high address byte. Careful use of the zero page can
  result in significant increase in code efficiency.

  INDEXED ZERO PAGE ADDRESSING - (X, Y indexing)-This form of addressing is
  used in conjunction with the index register and is referred to as "Zero
  Page, X" or "Zero Page, Y." The effective address is calculated by adding
  the second byte to the contents of the index register. Since this is a
  form of "Zero Page" addressing, the content of the second byte references
  a location in page zero. Additionally, due to the "Zero Page" addressing
  nature of this mode, no carry is added to the high order 8 bits of memory
  and crossing of page boundaries does not occur.

  INDEXED ABSOLUTE ADDRESSING - (X, Y indexing)-This form of addressing is
  used in conjunction with X and Y index register and is referred to as
  "Absolute, X," and "Absolute, Y." The effective address is formed by
  adding the contents of X and Y to the address contained in the second and
  third bytes of the instruction. This mode allows the index register to
  contain the index or count value and the instruction to contain the base
  address. This type of indexing allows any location referencing and the
  index to modify multiple fields resulting in reduced coding and execution
  time.

  IMPLIED ADDRESSING - In the implied addressing mode, the address
  containing the operand is implicitly stated in the operation code of the
  instruction.

  RELATIVE ADDRESSING - Relative addressing is used only with branch
  instructions and establishes a destination for the conditional branch.

  The second byte of the instruction becomes the operand which is an
  "Offset" added to the contents of the lower eight bits of the program
  counter when the counter is set at the next instruction. The range of the
  offset is -128 to +127 bytes from the next instruction.

  INDEXED INDIRECT ADDRESSING - In indexed indirect addressing (referred to
  as [Indirect, X]), the second byte of the instruction is added to the
  contents of the X index register, discarding the carry. The result of
  this addition points to a memory location on page zero whose contents is
  the low order eight bits of the effective address. The next memory loca-
  tion in page zero contains the high order eight bits of the effective ad-
  dress. Both memory locations specifying the high and low order bytes of

  the effective address must be in page zero.

  INDIRECT INDEXED ADDRESSING - In indirect indexed addressing (referred to
  as [Indirect], Y), the second byte of the instruction points to a memory
  location in page zero. The contents of this memory location is added to
  the contents of the Y index register, the result being the low order
  eight bits of the effective address. The carry from this addition is
  added to the contents of the next page zero memory location, the result
  being the high order eight bits of the effective address.

  ABSOLUTE INDIRECT - The second byte of the instruction contains the low
  order eight bits of a memory location. The high order eight bits of that
  memory location is contained in the third byte of the instruction. The
  contents of the fully specified memory location is the low order byte of
  the effective address. The next memory location contains the high order
  byte of the effective address which is loaded into the sixteen bits of
  the program counter.

  INSTRUCTION SET - ALPHABETIC SEQUENCE

          ADC   Add Memory to Accumulator with Carry
          AND   "AND" Memory with Accumulator
          ASL   Shift left One Bit (Memory or Accumulator)

          BCC   Branch on Carry Clear
          BCS   Branch on Carry Set
          BEQ   Branch on Result Zero
          BIT   Test Bits in Memory with Accumulator
          BMI   Branch on Result Minus
          BNE   Branch on Result not Zero
          BPL   Branch on Result Plus
          BRK   Force Break
          BVC   Branch on Overflow Clear
          BVS   Branch on Overflow Set

          CLC   Clear Carry Flag
          CLD   Clear Decimal Mode
          CLI   Clear Interrupt Disable Bit
          CLV   Clear Overflow Flag
          CMP   Compare Memory and Accumulator
          CPX   Compare Memory and Index X
          CPY   Compare Memory and Index Y

          DEC   Decrement Memory by One
          DEX   Decrement Index X by One
          DEY   Decrement Index Y by One

          EOR   "Exclusive-OR" Memory with Accumulator

          INC   Increment Memory by One
          INX   Increment Index X by one
          INY   Increment Index Y by one

          JMP   Jump to New location
          JSR   Jump to New Location Saving Return Address

          LDA   Load Accumulator with Memory
          LDX   Load Index X with Memory
          LDY   Load Index Y with Memory
          LSR   Shift One Bit Right (Memory or Accumulator)

          NOP   No Operation

          ORA   "OR" Memory with Accumulator

          PHA   Push Accumulator on Stack
          PHP   Push Processor Status on Stack
          PLA   Pull Accumulator from Stack
          PLP   Pull Processor Status from Stack

          ROL   Rotate One Bit Left (Memory or Accumulator)
          ROR   Rotate One Bit Right (Memory or Accumulator)
          RTI   Return from Interrupt
          RTS   Return from Subroutine

          SBC   Subtract Memory from Accumulator with Borrow
          SEC   Set Carry Flag
          SED   Set Decimal Mode
          SEI   Set Interrupt Disable Status
          STA   Store Accumulator in Memory
          STX   Store Index X in Memory
          STY   Store Index Y in Merrory

          TAX   Transfer Accumulator to Index X
          TAY   Transfer Accumulator to Index Y
          TSX   Transfer Stack Pointer to Index X
          TXA   Transfer Index X to Accumulator
          TXS   Transfer Index X to Stack Register
          TYA   Transfer Index Y to Accumulator

  PROGRAMMING MODEL
                        +---------------+
                        |       A       |  ACCUMULATOR           A
                        +---------------+

                        +---------------+
                        |       Y       |  INDEX REGISTER        Y
                        +---------------+

                        +---------------+
                        |       X       |  INDEX REGISTER        X
                        +---------------+
        15               7             0
        +---------------+---------------+
        |      PCH      |      PCL      |  PROGRAM COUNTER     "PC"
        +---------------+---------------+
                       8 7             0
                      +-+---------------+
                      |1|       S       |  STACK POINTER        "S"
                      +-+---------------+
                         7             0
                        +-+-+-+-+-+-+-+-+
                        |N|V| |B|D|I|Z|C|  PROCESSOR STATUS REG "P"
                        +-+-+-+-+-+-+-+-+
                         | |   | | | | |
                         | |   | | | | +>  CARRY         1=TRUE
                         | |   | | | +-->  ZERO          1=RESULT ZERO
                         | |   | | +---->  IRQ DISABLE   1=DISABLE
                         | |   | +------>  DECIMAL MODE  1=TRUE
                         | |   +-------->  BRK COMMAND
                         | |
                         | +------------>  OVERFLOW      1=TRUE
                         +-------------->  NEGATIVE      1=NEG

      INSTRUCTION SET - OP CODES, EXECUTION TIME, MEMORY REQUIREMENTS

                          [THE PICTURE IS MISSING!]

  +-----------------------------------------------------------------------+
  | NOTE: COMMODORE SEMICONDUCTOR GROUP cannot assume liability for the   |
  | use of undefined OP CODES.                                            |
  +-----------------------------------------------------------------------+

      INSTRUCTION SET - OP CODES, EXECUTION TIME, MEMORY REQUIREMENTS

                          [THE PICTURE IS MISSING!]

  6510 MEMORY MAP

       +-------------------+
  FFFF |                   |
       |    ADDRESSABLE    |
       /      EXTERNAL     /
       /       MEMORY      /
       |                   |
  0200 |                   |
       +-------------------+           STACK
  01FF |  |    STACK    |  | 01FF <--- POINTER
  0100 | \|/   Page 1  \|/ |           INITIALIZED
       +-------------------+
  00FF |                   |
       |       Page 0      |
       +-------------------+
       |  OUTPUT REGISTER  | 0001 <-+- Used For
       +-------------------+        |  Internal
  0000 |DATA DIRECTION REG.| 0000 <-+  I/O Port
       +-------------------+

  APPLICATIONS NOTES

    Locating the Output Register at the internal I/O Port in Page Zero
  enhances the powerful Zero Page Addressing instructions of the 6510.
    By assigning the I/O Pins as inputs (using the Data Direction Register)
  the user has the ability to change the contents of address 0001 (the
  Output Register) using peripheral devices. The ability to change these
  contents using peripheral inputs, together with Zero Page Indirect
  Addressing instructions, allows novel and versatile programming tech-
  niques not possible earlier.

  +-----------------------------------------------------------------------+
  | COMMODORE SEMICONDUCTOR GROUP reserves the right to make changes to   |
  | any products herein to improve reliability, function or design.       |
  | COMMODORE SEMICONDUCTOR GROUP does not assume any liability arising   |
  | out of the application or use of any product or circuit described     |
  | herein; neither does it convey any license under its patent rights nor|
  | the rights of others.                                                 |
  +-----------------------------------------------------------------------+
