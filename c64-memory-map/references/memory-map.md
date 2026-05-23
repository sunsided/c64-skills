> Source: c64prg.txt §Ch5 "Memory Management on the Commodore 64" and "Commodore 64 Memory Maps". Lightly cleaned from the Project 64 etext.

  MEMORY MANAGEMENT ON THE
  COMMODORE 64

    The Commodore 64 has 64K bytes of RAM. It also has 20K bytes of ROM,
  containing BASIC, the operating system, and the standard character set.
  It also accesses input/output devices as a 4K chunk of memory. How is
  this all possible on a computer with a 16-bit address bus, that is
  normally only capable of addressing 64K?
    The secret is in the 6510 processor chip itself. On the chip is an
  input/output port. This port is used to control whether RAM or ROM or I/O
  will appear in certain portions of the system's memory. The port is also
  used to control the Datassette(TM), so it is important to affect only the
  proper bits.
    The 6510 input/output port appears at location 1. The data direction
  register for this port appears at location 0. The port is controlled like
  any of the other input/output ports in the system... the data direction
  controls whether a given bit will be an input or an output, and the
  actual data transfer occurs through the port itself. The lines in the
  6510 control port are defined as follows:

  +---------+---+------------+--------------------------------------------+
  |  NAME   |BIT| DIRECTION  |                 DESCRIPTION                |
  +---------+---+------------+--------------------------------------------+
  |  LORAM  | 0 |   OUTPUT   | Control for RAM/ROM at $A000-$BFFF         |
  |  HIRAM  | 1 |   OUTPUT   | Control for RAM/ROM at $E000-$FFFF         |
  |  CHAREN | 2 |   OUTPUT   | Control for I/O/ROM at $D000-$DFFF         |
  |         | 3 |   OUTPUT   | Cassette write line                        |
  |         | 4 |   INPUT    | Cassette switch sense (0=play button down) |
  |         | 5 |   OUTPUT   | Cassette motor control (0=motor spins)     |
  +---------+---+------------+--------------------------------------------+

    The proper value for the data direction register is as follows:

                              BITS 5 4 3 2 1 0
                              ----------------
                                   1 0 1 1 1 1

  (where 1 is an output, and 0 is an input).

    This gives a value of 47 decimal. The Commodore 64 automatically sets
  the data direction register to this value.
    The control lines, in general, perform the function given in their de-
  scriptions. However, a combination of control lines are occasionally used
  to get a particular memory configuration.
    LORAM (bit 0) can generally be thought of as a control line which banks
  the 8K byte BASIC ROM in and out of the microprocessor address space.
  Normally, this line is HIGH for BASIC operation. If this line is
  programmed LOW, the BASIC ROM will disappear from the memory map and be
  replaced by 8K bytes of RAM from $A000-$BFFF.
    HIRAM (bit 1) can generally be thought of as a control line which banks
  the 8K byte KERNAL ROM in and out of the microprocessor address space.
  Normally, this line is HIGH for BASIC operation. If this line is
  programmed LOW, the KERNAL ROM will disappear from the memory map and be
  replaced by 8K bytes of RAM from $E000-$FFFF.
    CHAREN (bit 2) is used only to bank the 4K byte character generator ROM
  in or out of the microprocessor address space. From the processor point
  of view, the character ROM occupies the same address space as the I/O
  devices ($D000-$DFFF). When the CHAREN line is set to 1 (as is normal),
  the I/O devices appear in the microprocessor address space, and the
  character ROM is not accessable. When the CHAREN bit is cleared to 0, the
  character ROM appears in the processor address space, and the I/O devices
  are not accessable. (The microprocessor only needs to access the
  character ROM when downloading the character set from ROM to RAM. Special
  care is needed for this... see the section on PROGRAMMABLE CHARACTERS in
  the GRAPHICS chapter). CHAREN can be overridden by other control lines in
  certain memory configurations. CHAREN will have no effect on any memory
  configuration without I/O devices. RAM will appear from $D000-$DFFF
  instead.

  +-----------------------------------------------------------------------+
  | NOTE: In any memory map containing ROM, a WRITE (a POKE) to a ROM     |
  | location will store data in the RAM "under" the ROM. Writing to a ROM |
  | location stores data in the "hidden" RAM. For example, this allows a  |
  | hi-resolution screen to be kept underneath a ROM, and be changed      |
  | without having to bank the screen back into the processor address     |
  | space. Of course a READ of a ROM location will return the contents of |
  | the ROM, not the "hidden" RAM.                                        |
  +-----------------------------------------------------------------------+

  COMMODORE 64 FUNDAMENTAL MEMORY MAP

                                 +----------------------------+
                                 |       8K KERNAL ROM        |
                      E000-FFFF  |           OR RAM           |
                                 +----------------------------+
                      D000-DFFF  | 4K I/O OR RAM OR CHAR. ROM |
                                 +----------------------------+
                      C000-CFFF  |           4K RAM           |
                                 +----------------------------+
                                 |    8K BASIC ROM OR RAM     |
                      A000-BFFF  |       OR ROM PLUG-IN       |
                                 +----------------------------+
                                 |            8K RAM          |
                      8000-9FFF  |       OR ROM PLUG-IN       |
                                 +----------------------------+
                                 |                            |
                                 |                            |
                                 |          16 K RAM          |
                      4000-7FFF  |                            |
                                 +----------------------------+
                                 |                            |
                                 |                            |
                                 |          16 K RAM          |
                      0000-3FFF  |                            |
                                 +----------------------------+

  I/O BREAKDOWN

    D000-D3FF   VIC (Video Controller)                     1 K Bytes
    D400-D7FF   SID (Sound Synthesizer)                    1 K Bytes
    D800-DBFF   Color RAM                                  1 K Nybbles
    DC00-DCFF   CIA1 (Keyboard)                            256 Bytes
    DD00-DDFF   CIA2 (Serial Bus, User Port/RS-232)        256 Bytes
    DE00-DEFF   Open I/O slot #l (CP/M Enable)             256 Bytes
    DF00-DFFF   Open I/O slot #2 (Disk)                    256 Bytes

    The two open I/O slots are for general purpose user I/O, special pur-
  pose I/O cartridges (such as IEEE), and have been tentatively designated
  for enabling the Z-80 cartridge (CP/M option) and for interfacing to a
  low-cost high-speed disk system.
    The system provides for "auto-start" of the program in a Commodore 64
  Expansion Cartridge. The cartridge program is started if the first nine
  bytes of the cartridge ROM starting at location 32768 ($8000) contain
  specific data. The first two bytes must hold the Cold Start vector to be
  used by the cartridge program. The next two bytes at 32770 ($8002) must
  be the Warm Start vector used by the cartridge program. The next three
  bytes must be the letters, CBM, with bit 7 set in each letter. The last
  two bytes must be the digits "80" in PET ASCII.

  COMMODORE 64 MEMORY MAPS

    The following table lists the various memory configurations available
  on the COMMODORE 64, the states of the control lines which select each
  memory map, and the intended use of each map.
    The leftmost column of the table contains addresses in hexadecimal
  notation. The columns aside it introduce all possible memory
  configurations. The default mode is on the left, and the absolutely most
  rarely used Ultimax game console configuration is on the right. Each
  memory configuration column has one or more four-digit binary numbers as
  a title. The bits, from left to right, represent the state of the /LORAM,
  /HIRAM, /GAME and /EXROM lines, respectively. The bits whose state does
  not matter are marked with "X". For instance, when the Ultimax video game
  configuration is active (the /GAME line is shorted to ground, /EXROM kept
  high), the /LORAM and /HIRAM lines have no effect.

           LHGE   LHGE   LHGE   LHGE   LHGE   LHGE   LHGE   LHGE   LHGE

           1111   101X   1000   011X   001X   1110   0100   1100   XX01
  10000  default                00X0                             Ultimax
  -------------------------------------------------------------------------
   F000
          Kernal  RAM    RAM   Kernal  RAM   Kernal Kernal Kernal ROMH(*
   E000
  -------------------------------------------------------------------------
   D000    IO/C   IO/C  IO/RAM  IO/C   RAM    IO/C   IO/C   IO/C   I/O
  -------------------------------------------------------------------------
   C000    RAM    RAM    RAM    RAM    RAM    RAM    RAM    RAM     -
  -------------------------------------------------------------------------
   B000
          BASIC   RAM    RAM    RAM    RAM   BASIC   ROMH   ROMH    -
   A000
  -------------------------------------------------------------------------
   9000
           RAM    RAM    RAM    RAM    RAM    ROML   RAM    ROML  ROML(*
   8000
  -------------------------------------------------------------------------
   7000

   6000
           RAM    RAM    RAM    RAM    RAM    RAM    RAM    RAM     -
   5000

   4000
  -------------------------------------------------------------------------
   3000

   2000    RAM    RAM    RAM    RAM    RAM    RAM    RAM    RAM     -

   1000
  -------------------------------------------------------------------------
   0000    RAM    RAM    RAM    RAM    RAM    RAM    RAM    RAM    RAM
  -------------------------------------------------------------------------

     NOTE: (1)    (2)    (3)    (4)    (5)    (6)    (7)    (8)    (9)

    *) Internal memory does not respond to write accesses to these areas.

    Legend: Kernal      E000-FFFF       Kernal ROM.

	    IO/C        D000-DFFF       I/O address space or Character
					generator ROM, selected by -CHAREN.
					If the CHAREN bit is clear,
					the character generator ROM is
					chosen. If it is set, the
					I/O chips are accessible.

	    IO/RAM      D000-DFFF       I/O address space or RAM,
					selected by -CHAREN.
					If the CHAREN bit is clear,
					the character generator ROM is
					chosen. If it is set, the
					internal RAM is accessible.

	    I/O         D000-DFFF       I/O address space.
					The -CHAREN line has no effect.

	    BASIC       A000-BFFF       BASIC ROM.

	    ROMH        A000-BFFF or    External ROM with the -ROMH line
			E000-FFFF       connected to its -CS line.

	    ROML        8000-9FFF       External ROM with the -ROML line
					connected to its -CS line.

	    RAM         various ranges  Commodore 64's internal RAM.

	    -           1000-7FFF and   Open address space.
			A000-CFFF       The Commodore 64's memory chips
					do not detect any memory accesses
					to this area except the VIC-II's
					DMA and memory refreshes.

        (1)   This is the default BASIC memory map which provides
              BASIC 2.0 and 38K contiguous bytes of user RAM.

        (2)   This map provides 60K bytes of RAM and I/O devices.
              The user must write his own I/O driver routines.

        (3)   The same as 2, but the character ROM is not
              accessible by the CPU in this map.

        (4)   This map is intended for use with softload languages
              (including CP/M), providing 52K contiguous bytes of
              user RAM, I/O devices, and I/O driver routines.

        (5)   This map gives access to all 64K bytes of RAM. The
              I/O devices must be banked back into the processor's
              address space for any I/O operation.

        (6)   This is the standard configuration for a BASIC system
              with a BASIC expansion ROM. This map provides 32K
              contiguous bytes of user RAM and up to 8K bytes of
              BASIC "enhancement".

        (7)   This map provides 40K contiguous bytes of user RAM
              and up to 8K bytes of plug-in ROM for special ROM-
              based applications which don't require BASIC.

        (8)   This map provides 32K contiguous bytes of user RAM
              and up to 16K bytes of plug-in ROM for special
              applications which don't require BASIC (word
              processors, other languages, etc.).

        (9)   This is the ULTIMAX video game memory map. Note that
              the 2K byte "expansion RAM" for the ULTIMAX, if
              required, is accessed out of the COMMODORE 64 and
              any RAM in the cartridge is ignored.


---

> Source: c64prg.txt §Ch5 "Commodore 64 Memory Map" (location-by-location). Lightly cleaned from the Project 64 etext.

  COMMODORE 64 MEMORY MAP

             HEX        DECIMAL
   LABEL   ADDRESS      LOCATION               DESCRIPTION
  -------------------------------------------------------------------------

  D6510   0000            0        6510 On-Chip Data-Direction Register
  R6510   0001            1        6510 On-Chip 8-Bit Input/Output Register
          0002            2        Unused
  ADRAY1  0003-0004       3-4      Jump Vector: Convert Floating-Integer

             HEX        DECIMAL
   LABEL   ADDRESS      LOCATION               DESCRIPTION
  -------------------------------------------------------------------------

  ADRAY2  0005-0006       5-6      Jump Vector: Convert Integer--Floating
  CHARAC  0007            7        Search Character
  ENDCHR  0008            8        Flag: Scan for Quote at End of String
  TRMPOS  0009            9        Screen Column From Last TAB
  VERCK   000A           10        Flag: 0 = Load, 1 = Verify
  COUNT   000B           11        Input Buffer Pointer / No. of Subscripts
  DIMFLG  000C           12        Flag: Default Array DiMension
  VALTYP  000D           13        Data Type: $FF = String, $00 = Numeric
  INTFLG  000E           14        Data Type: $80 = Integer, $00 = Floating
  GARBFL  000F           15        Flag: DATA scan/LIST quote/Garbage Coll
  SUBFLG  0010           16        Flag: Subscript Ref / User Function Call
  INPFLG  0011           17        Flag: $00 = INPUT, $40 = GET, $98 = READ
  TANSGN  0012           18        Flag TAN sign / Comparison Result
          0013           19        Flag: INPUT Prompt
  LINNUM  0014-0015      20-21     Temp: Integer Value
  TEMPPT  0016           22        Pointer Temporary String
  LASTPT  0017-0018      23-24     Last Temp String Address
  TEMPST  0019-0021      25-33     Stack for Temporary Strings
  INDEX   0022-0025      34-37     Utility Pointer Area

  INDEX1  0022-0023      34-35     First Utility Pointer.
  INDEX2  0024-0025      36-37     Second Utility Pointer.

  RESHO   0026-002A      38-42     Floating-Point Product of Multiply
  TXTTAB  002B-002C      43-44     Pointer: Start of BASIC Text
  VARTAB  002D-002E      45-46     Pointer: Start of BASIC Variables
  ARYTAB  002F-0030      47-48     Pointer: Start of BASIC Arrays
  STREND  0031-0032      49-50     Pointer End of BASIC Arrays (+1)
  FRETOP  0033-0034      51-52     Pointer: Bottom of String Storage
  FRESPC  0035-0036      53-54     Utility String Pointer
  MEMSIZ  0037-0038      55-56     Pointer: Highest Address Used by BASIC
  CURLIN  0039-003A      57-58     Current BASIC Line Number
  OLDLIN  003B-003C      59-60     Previous BASIC Line Number
  OLDTXT  003D-003E      61-62     Pointer: BASIC Statement for CONT
  DATLIN  003F-0040      63-64     Current DATA Line Number
  DATPTR  0041-0042      65-66     Pointer: Current DATA Item Address
  INPPTR  0043-0044      67-68     Vector: INPUT Routine
  VARNAM  0045-0046      69-70     Current BASIC Variable Name

             HEX        DECIMAL
   LABEL   ADDRESS      LOCATION               DESCRIPTION
  -------------------------------------------------------------------------

  VARPNT  0047-0048      71-72     Pointer: Current BASIC Variable Data
  FORPNT  0049-004A      73-74     Pointer: Index Variable for FOR/NEXT
          004B-0060      75-96     Temp Pointer / Data Area

  VARTXT  004B-004C      75-76     Temporary storage for TXTPTR during
                                     READ, INPUT and GET.
  OPMASK  004D           77        Mask used during FRMEVL.
  TEMPF3  004E-0052      78-82     Temporary storage for FLPT value.
  FOUR6   0053           83        Length of String Variable during Garbage
                                     collection.
  JMPER   0054-0056      84-86     Jump Vector used in Function Evaluation-
                                     JMP followed by Address ($4C,$LB,$MB).
  TEMPF1  0057-005B      87-91     Temporary storage for FLPT value.
  TEMPF2  005C-0060      92-96     Temporary storage for FLPT value.
  FACEXP  0061           97        Floating-Point Accumulator #1: Exponent
  FACHO   0062-0065      98-101    Floating Accum. #1: Mantissa
  FACSGN  0066          102        Floating Accum. #1: Sign
  SGNFLG  0067          103        Pointer: Series Evaluation Constant
  BITS    0068          104        Floating Accum. #1: Overflow Digit
  ARGEXP  0069          105        Floating-Point Accumulator #2: Exponent
  ARGHO   006A-006D     106-109    Floating Accum. #2: Mantissa
  ARGSGN  006E          110        Floating Accum. #2: Sign
  ARISGN  006F          111        Sign Comparison Result: Accum. # 1 vs #2
  FACOV   0070          112        Floating Accum. #1. Low-Order (Rounding)
  FBUFPT  0071-0072     113-114    Pointer: Cassette Buffer
  CHRGET  0073-008A     115-138    Subroutine: Get Next Byte of BASIC Text

  CHRGOT  0079          121        Entry to Get Same Byte of Text Again
  TXTPTR  007A-007B     122-123    Pointer: Current Byte of BASIC Text

  RNDX    008B-008F     139-143    Floating RND Function Seed Value
  STATUS  0090          144        Kernal I/O Status Word: ST
  STKEY   0091          145        Flag: STOP key / RVS key
  SVXT    0092          146        Timing Constant for Tape
  VERCK   0093          147        Flag: 0 = Load, 1 = Verify
  C3PO    0094          148        Flag: Serial Bus-Output Char. Buffered
  BSOUR   0095          149        Buffered Character for Serial Bus
  SYNO    0096          150        Cassette Sync No.

             HEX        DECIMAL
   LABEL   ADDRESS      LOCATION               DESCRIPTION
  -------------------------------------------------------------------------

          0097          151        Temp Data Area
  LDTND   0098          152        No. of Open Files / Index to File Table
  DFLTN   0099          153        Default Input Device (0)
  DFLTO   009A          154        Default Output (CMD) Device (3)
  PRTY    009B          155        Tape Character Parity
  DPSW    009C          156        Flag: Tape Byte-Received
  MSGFLG  009D          157        Flag: $80 = Direct Mode, $00 = Program
  PTR1    009E          158        Tape Pass 1 Error Log
  PTR2    009F          159        Tape Pass 2 Error Log
  TIME    00A0-00A2     160-162    Real-Time Jiffy Clock (approx) 1/60 Sec
          00A3-00A4     163-164    Temp Data Area
  CNTDN   00A5          165        Cassette Sync Countdown
  BUFPNT  00A6          166        Pointer: Tape I/O Buffer
  INBIT   00A7          167        RS-232 Input Bits / Cassette Temp
  BITCI   00A8          168        RS-232 Input Bit Count / Cassette Temp
  RINONE  00A9          169        RS-232 Flag: Check for Start Bit
  RIDATA  00AA          170        RS-232 Input Byte Buffer/Cassette Temp
  RIPRTY  00AB          171        RS-232 Input Parity / Cassette Short Cnt
  SAL     00AC-00AD     172-173    Pointer: Tape Buffer/ Screen Scrolling
  EAL     00AE-00AF     174-175    Tape End Addresses/End of Program
  CMP0    00B0-00B1     176-177    Tape Timing Constants
  TAPE1   00B2-00B3     178-179    Pointer: Start of Tape Buffer
  BITTS   00B4          180        RS-232 Out Bit Count / Cassette Temp
  NXTBIT  00B5          181        RS-232 Next Bit to Send/ Tape EOT Flag
  RODATA  00B6          182        RS-232 Out Byte Buffer
  FNLEN   00B7          183        Length of Current File Name
  LA      00B8          184        Current Logical File Number
  SA      00B9          185        Current Secondary Address
  FA      00BA          186        Current Device Number
  FNADR   00BB-00BC     187-188    Pointer: Current File Name
  ROPRTY  00BD          189        RS-232 Out Parity / Cassette Temp
  FSBLK   00BE          190        Cassette Read / Write Block Count
  MYCH    00BF          191        Serial Word Buffer
  CAS1    00C0          192        Tape Motor Interlock
  STAL    00C1-00C2     193-194    I/O Start Address
  MEMUSS  00C3-00C4     195-196    Tape Load Temps
  LSTX    00C5          197        Current Key Pressed: CHR$(n) 0 = No Key
  NDX     00C6          198        No. of Chars. in Keyboard Buffer (Queue)

             HEX        DECIMAL
   LABEL   ADDRESS      LOCATION               DESCRIPTION
  -------------------------------------------------------------------------

  RVS     00C7          199        Flag: Reverse Chars. - 1=Yes, 0=No Used
  INDX    00C8          200        Pointer: End of Logical Line for INPUT
  LXSP    00C9-00CA     201-202    Cursor X-Y Pos. at Start of INPUT
  SFDX    00CB          203        Flag: Print Shifted Chars.
  BLNSW   00CC          204        Cursor Blink enable: 0 = Flash Cursor
  BLNCT   00CD          205        Timer: Countdown to Toggle Cursor
  GDBLN   00CE          206        Character Under Cursor
  BLNON   00CF          207        Flag: Last Cursor Blink On/Off
  CRSW    00D0          208        Flag: INPUT or GET from Keyboard
  PNT     00D1-00D2     209-210    Pointer: Current Screen Line Address
  PNTR    00D3          211        Cursor Column on Current Line
  QTSW    00D4          212        Flag: Editor in Quote Mode, $00 = NO
  LNMX    00D5          213        Physical Screen Line Length
  TBLX    00D6          214        Current Cursor Physical Line Number
          00D7          215        Temp Data Area
  INSRT   00D8          216        Flag: Insert Mode, >0 = # INSTs
  LDTB1   00D9-00F2     217-242    Screen Line Link Table / Editor Temps
  USER    00F3-00F4     243-244    Pointer: Current Screen Color RAM loc.
  KEYTAB  00F5-00F6     245-246    Vector Keyboard Decode Table
  RIBUF   00F7-00F8     247-248    RS-232 Input Buffer Pointer
  ROBUF   00F9-00FA     249-250    RS-232 Output Buffer  Pointer
  FREKZP  00FB-00FE     251-254    Free 0-Page Space for User Programs
  BASZPT  00FF          255        BASIC Temp Data Area
          0100-01FF     256-511    Micro-Processor System Stack Area

          0100-010A     256-266    Floating to String Work Area
  BAD     0100-013E     256-318    Tape Input Error Log

  BUF     0200-02S8     512-600    System INPUT Buffer
  LAT     0259-0262     601-610    KERNAL Table: Active Logical File No's.
  FAT     0263-026C     611-620    KERNAL Table: Device No. for Each File
  SAT     026D-0276     621-630    KERNAL Table: Second Address Each File
  KEYD    0277-0280     631-640    Keyboard Buffer Queue (FIFO)
  MEMSTR  0281-0282     641-642    Pointer: Bottom of Memory for O.S.
  MEMSIZ  0283-0284     643-644    Pointer: Top of Memory for O.S.
  TIMOUT  0285          645        Flag: Kernal Variable for IEEE Timeout
  COLOR   0286          646        Current Character Color Code
  GDCOL   0287          647        Background Color Under Cursor

             HEX        DECIMAL
   LABEL   ADDRESS      LOCATION               DESCRIPTION
  -------------------------------------------------------------------------

  HIBASE  0288          648        Top of Screen Memory (Page)
  XMAX    0289          649        Size of Keyboard Buffer
  RPTFLG  028A          650        Flag: REPEAT Key Used, $80 = Repeat
  KOUNT   028B          651        Repeat Speed Counter
  DELAY   028C          652        Repeat Delay Counter
  SHFLAG  028D          653        Flag: Keyboard SHIFT Key/CTRL Key/C= Key
  LSTSHF  028E          654        Last Keyboard Shift Pattern
  KEYLOG  028F-0290     655-656    Vector: Keyboard Table Setup
  MODE    0291          657        Flag: $00=Disable SHIFT Keys, $80=Enable
  AUTODN  0292          658        Flag: Auto Scroll Down, 0 = ON
  M51CTR  0293          659        RS-232: 6551 Control Register Image
  MS1CDR  0294          660        RS-232: 6551 Command Register Image
  M51AJB  0295-0296     661-662    RS-232 Non-Standard BPS (Time/2-100) USA
  RSSTAT  0297          663        RS-232: 6551 Status Register Image
  BITNUM  0298          664        RS-232 Number of Bits Left to Send
  BAUDOF  0299-029A     665-666    RS-232 Baud Rate: Full Bit Time (us)
  RIDBE   029B          667        RS-232 Index to End of Input Buffer
  RIDBS   029C          668        RS-232 Start of Input Buffer (Page)
  RODBS   029D          669        RS-232 Start of Output Buffer (Page)
  RODBE   029E          670        RS-232 Index to End of Output Buffer
  IRQTMP  029F-02A0     671-672    Holds IRQ Vector During Tape I/O
  ENABL   02A1          673        RS-232 Enables
          02A2          674        TOD Sense During Cassette I/O
          02A3          675        Temp Storage For Cassette Read
          02A4          676        Temp D1 IRQ Indicator For Cassette Read
          02A5          677        Temp For Line Index
          02A6          678        PAL/NTSC Flag, 0= NTSC, 1 = PAL
          02A7-02FF     679-767    Unused
  IERROR  0300-0301     768-769    Vector: Print BASIC Error Message
  IMAIN   0302-0303     770-771    Vector: BASIC Warm Start
  ICRNCH  0304-0305     772-773    Vector: Tokenize BASIC Text
  IQPLOP  0306-0307     774-775    Vector: BASIC Text LIST
  IGONE   0308-0309     776-777    Vector: BASIC Char. Dispatch
  IEVAL   030A-030B     778-779    Vector: BASIC Token Evaluation
  SAREG   030C          780        Storage for 6502 .A Register
  SXREG   030D          781        Storage for 5502 .X Register
  SYREG   030E          782        Storage for 6502 .Y Register
  SPREG   030F          783        Storage for 6502 .SP Register

             HEX        DECIMAL
   LABEL   ADDRESS      LOCATION               DESCRIPTION
  -------------------------------------------------------------------------

  USRPOK  0310          784        USR Function Jump Instr (4C)
  USRADD  0311-0312     785-786    USR Address Low Byte / High Byte
          0313          787        Unused
  CINV    0314-0315     788-789    Vector: Hardware Interrupt
  CBINV   0316-0317     790-791    Vector: BRK Instr. Interrupt
  NMINV   0318-0319     792-793    Vector: Non-Maskable Interrupt
  IOPEN   031A-031B     794-795    KERNAL OPEN Routine Vector
  ICLOSE  031C-031D     796-797    KERNAL CLOSE Routine Vector
  ICHKIN  031E-031F     798-799    KERNAL CHKIN Routine
  ICKOUT  0320-0321     800-801    KERNAL CHKOUT Routine
  ICLRCH  0322-0323     802-803    KERNAL CLRCHN Routine Vector
  IBASIN  0324-0325     804-805    KERNAL CHRIN Routine
  IBSOUT  0326-0327     806-807    KERNAL CHROUT Routine
  ISTOP   0328-0329     808-809    KERNAL STOP Routine Vector
  IGETIN  032A-032B     810-811    KERNAL GETIN Routine
  ICLALL  032C-032D     812-813    KERNAL CLALL Routine Vector
  USRCMD  032E-032F     814-815    User-Defined Vector
  ILOAD   0330-0331     813-817    KERNAL LOAD Routine
  ISAVE   0332-0333     818-819    KERNAL SAVE Routine Vector
          0334-033B     820-827    Unused
  TBUFFR  033C-03FB     828-1019   Tape I/O Buffer
          03FC-03FF    1020-1023   Unused
  VICSCN  0400-07FF    1024-2047   1024 Byte Screen Memory Area

          0400-07E7    1024-2023   Video Matrix: 25 Lines X 40 Columns
          07F8-07FF    2040-2047   Sprite Data Pointers

          0800-9FFF   2048-40959   Normal BASIC Program Space
          8000-9FFF  32768-40959   VSP Cartridge ROM - 8192 Bytes
          A000-BFFF  40960-49151   BASIC ROM - 8192 Bytes (or 8K RAM)
          C000-CFFF  49152-53247   RAM - 4096 Bytes
          D000-DFFF  53248-57343   Input/Output Devices and
                                     Color RAM or Character Generator ROM
                                     or RAM - 4096 Bytes
          E000-FFFF  57344-65535   KERNAL ROM - 8192 Bytes (or 8K RAM)
