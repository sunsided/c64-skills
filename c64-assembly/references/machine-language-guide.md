> Source: c64prg.txt §Ch5 "BASIC to Machine Language" (intro, addressing modes, indexing, subroutines, tips). Lightly cleaned from the Project 64 etext.

                                                 CHAPTER 5

                                                  BASIC TO
                                                   MACHINE
                                                  LANGUAGE

                           o What Is Machine Language?
                           o How Do You Write Machine
                             Language Programs?
                           o Hexadecimal Notation
                           o Addressing Modes
                           o Indexing
                           o Subroutines
                           o Useful Tips for the Beginner
                           o Approaching a Large Task
                           o MCS6510 Microprocessor
                             Instruction Set
                           o Memory Management on the
                             Commodore 64
                           o The KERNAL
                           o KERNAL Power-Up Activities
                           o Using Machine Language From
                             BASIC
                           o Commodore 64 Memory Map

                                     209

  WHAT IS MACHINE LANGUAGE?

    At the heart of every microcomputer, is a central microprocessor. It's
  a very special microchip which is the "brain" of the computer. The
  Commodore 64 is no exception. Every microprocessor understands its own
  language of instructions. These instructions are called machine language
  instructions. To put it more precisely, machine language is the ONLY
  programming language that your Commodore 64 understands. It is the NATIVE
  language of the machine.
    If machine language is the only language that the Commodore 64
  understands, then how does it understand the CBM BASIC programming
  language? CBM BASIC is NOT the machine language of the Commodore 64.
  What, then, makes the Commodore 64 understand CBM BASIC instructions like
  PRINT and GOTO?
    To answer this question, you must first see what happens inside your
  Commodore 64. Apart from the microprocessor which is the brain of the
  Commodore 64, there is a machine language program which is stored in a
  special type of memory so that it can't be changed. And, more impor-
  tantly, it does not disappear when the Commodore 64 is turned off, unlike
  a program that you may have written. This machine language program is
  called the OPERATING SYSTEM of the Commodore 64. Your Commodore 64 knows
  what to do when it's turned on because its OPERATING SYSTEM (program) is
  automatically "RUN."

    The OPERATING SYSTEM is in charge of "organizing" all the memory in
  your machine for various tasks. It also looks at what characters you type
  on the keyboard and puts them onto the screen, plus a whole number of
  other functions. The OPERATING SYSTEM can be thought of as the
  "intelligence and personality" of the Commodore 64 (or any computer for
  that matter). So when you turn on your Commodore 64, the OPERATING SYSTEM
  takes control of your machine, and after it has done its housework, it
  then says:

    READY.

    The OPERATING SYSTEM of the Commodore 64 then allows you to type on the
  keyboard, and use the built-in SCREEN EDITOR on the Commodore 64. The
  SCREEN EDITOR allows you to move the cursor, DELete, INSert, etc., and
  is, in fact, only one part of the operating system that is built in for
  your convenience.
    All of the commands that are available in CBM BASIC are simply
  recognized by another huge machine language program built into your
  Commodore 64. This huge program "RUNS" the appropriate piece of machine
  language depending on which CBM BASIC command is being executed. This
  program is called the BASIC INTERPRETER, because it interprets each
  command, one by one, unless it encounters a command it does not
  understand, and then the familiar message appears:

    ?SYNTAX ERROR

    READY.

  WHAT DOES MACHINE CODE LOOK LIKE?

    You should be familiar with the PEEK and POKE commands in the CBM BASIC
  language for changing memory locations. You've probably used them for
  graphics on the screen, and for sound effects. Each memory location has
  its own number which identifies it. This number is known as the "address"
  of a memory location. If you imagine the memory in the Commodore 64 as a
  street of buildings, then the number on each door is, of course, the
  address. Now let's look at which parts of the street are used for what
  purposes.

  SIMPLE MEMORY MAP OF THE COMMODORE 64

  +-------------+---------------------------------------------------------+
  |   ADDRESS   |                      DESCRIPTION                        |
  +-------------+---------------------------------------------------------+
  |             |                                                         |
  |    0 & 1    | -6510 Registers.                                        |
  |             |                                                         |
  |     2       | -Start of memory.                                       |
  |             |                                                         |
  |     2-1023  | -Memory used by the operating system.                   |
  |             |                                                         |
  |  1024-2039  | -Screen memory.                                         |
  |             |                                                         |
  |  2040-2047  | -SPRITE pointers.                                       |
  |             |                                                         |
  |  2048-40959 | -This is YOUR memory. This is where your BASIC or       |
  |             |  machine language programs, or both, are stored.        |
  |             |                                                         |
  | 40960-49151 | -8K CBM BASIC Interpreter.                              |
  |             |                                                         |
  | 49152-53247 | -Special programs RAM area.                             |
  |             |                                                         |
  | 53248-53294 | -VIC-II.                                                |
  |             |                                                         |
  | 54272-55295 | -SID Registers.                                         |
  |             |                                                         |
  | 55296-56296 | -Color RAM.                                             |
  |             |                                                         |
  | 56320-57343 | -I/O Registers. (6526's)                                |
  |             |                                                         |
  | 57344-65535 | -8K CBM KERNAL Operating System.                        |
  |             |                                                         |
  +-------------+---------------------------------------------------------+

    If you don't understand what the description of each part of memory
  means right now, this will become clear from other parts of this manual.
    Machine language programs consist of instructions which may or may not
  have operands (parameters) associated with them. Each instruction takes
  up one memory location, and any operand is contained in one or two
  locations following the instruction.
    In your BASIC programs, words like PRINT and GOTO do, in fact, only
  take up one memory location, rather than one for each character of the
  word. The contents of the location that represents a particular BASIC
  keyword is called a token. In machine language, there are different
  tokens for different instructions, which also take up just one byte (mem-
  ory location=byte).
    Machine language instructions are very simple. Therefore, each indi-
  vidual instruction cannot achieve a great deal. Machine language in-
  structions either change the contents of a memory location, or change one
  of the internal registers (special storage locations) inside the micro-
  processor. The internal registers form the very basis of machine lan-
  guage.

  THE REGISTERS INSIDE THE 6510 MICROPROCESSOR

  THE ACCUMULATOR

    This is THE most important register in the microprocessor. Various ma-
  chine language instructions allow you to copy the contents of a memory
  location into the accumulator, copy the contents of the accumulator into
  a memory location, modify the contents of the accumulator or some other
  register directly, without affecting any memory. And the accumulator is
  the only register that has instructions for performing math.

  THE X INDEX REGISTER

    This is a very important register. There are instructions for nearly
  all of the transformations you can make to the accumulator. But there are
  other instructions for things that only the X register can do. Various
  machine language instructions allow you to copy the contents of a memory
  location into the X register, copy the contents of the X register into a
  memory location, and modify the contents of the X, or some other register
  directly.

  THE Y INDEX REGISTER

    This is a very important register. There are instructions for nearly
  all of the transformations you can make to the accumulator, and the X
  register. But there are other instructions for things that only the Y
  register can do. Various machine language instructions allow you to copy
  the contents of a memory location into the Y register, copy the contents
  of the Y register into a memory location, and modify the contents of the
  Y, or some other register directly.

  THE STATUS REGISTER

    This register consists of eight "flags" (a flag = something that indi-
  cates whether something has, or has not occurred).

  THE PROGRAM COUNTER

    This contains the address of the current machine language instruction
  being executed. Since the operating system is always "RUN"ning in the
  Commodore 64 (or, for that matter, any computer), the program counter is
  always changing. It could only be stopped by halting the microprocessor
  in some way.

  THE STACK POINTER

    This register contains the location of the first empty place on the
  stack. The stack is used for temporary storage by machine language pro-
  grams, and by the computer.

  THE INPUT/OUTPUT PORT

    This register appears at memory locations 0 (for the DATA DIRECTION
  REGISTER) and 1 (for the actual PORT). It is an 8-bit input/output port.
  On the Commodore 64 this register is used for memory management, to
  allow the chip to control more than 64K of RAM and ROM memory.
    The details of these registers are not given here. They are explained
  as the principles needed to explain them are explained.

  HOW DO YOU WRITE MACHINE LANGUAGE PROGRAMS?

    Since machine language programs reside in memory, and there is no
  facility in your Commodore 64 for writing and editing machine language

  programs, you must use either a program to do this, or write for yourself
  a BASIC program that "allows" you to write machine language.
    The most common methods used to write machine language programs are
  assembler programs. These packages allow you to write machine language
  instructions in a standardized mnemonic format, which makes the machine
  language program a lot more readable than a stream of numbers! Let's
  review: A program that allows you to write machine language programs in
  mnemonic format is called an assembler. Incidentally, a program that
  displays a machine language program in mnemonic format is called a
  disassembler. Available for your Commodore 64 is a machine language
  monitor cartridge (with assembler/disassembler, etc.) made by Commodore:

  64MON

    The 64MON cartridge available from your local dealer, is a program that
  allows you to escape from the world of CBM BASIC, into the land of
  machine language. It can display the contents of the internal registers
  in the 6510 microprocessor, and it allows you to display portions of mem-
  ory, and change them on the screen, using the screen editor. It also has
  a built-in assembler and disassembler, as well as many other features
  that allow you to write and edit machine language programs easily. You
  don't HAVE to use an assembler to write machine language, but the task is
  considerably easier with it. If you wish to write machine language
  programs, it is strongly suggested that you purchase an assembler of some
  sort. Without an assembler you will probably have to "POKE" the machine
  language program into memory, which is totally unadvisable. This manual
  will give its examples in the format that 64MON uses, from now on. Nearly
  all assembler formats are the same, therefore the machine language
  examples shown will almost certainly be compatible with any assembler.
  But before explaining any of the other features of 64MON, the hexadecimal
  numbering system must be explained.

  HEXADECIMAL NOTATION

  Hexadecimal notation is used by most machine language programmers when
  they talk about a number or address in a machine language program.
    Some assemblers let you refer to addresses and numbers in decimal
  (base 10), binary (base 2), or even octal (base 8) as well as hexadecimal

  (base 16) (or just "hex" as most people say). These assemblers do the
  conversions for you.
    Hexadecimal probably seems a little hard to grasp at first, but like
  most things, it won't take long to master with practice.
    By looking at decimal (base 10) numbers, you can see that each digit
  fails somewhere in the range between zero and a number equal to the base
  less one (e.g., 9). THIS IS TRUE OF ALL NUMBER BASES. Binary (base 2)
  numbers have digits ranging from zero to one (which is one less than the
  base). Similarly, hexadecimal numbers should have digits ranging from
  zero to fifteen, but we do not have any single digit figures for the
  numbers ten to fifteen, so the first six letters of the alphabet are used
  instead:

                    +---------+-------------+----------+
                    | DECIMAL | HEXADECIMAL |  BINARY  |
                    +---------+-------------+----------+
                    |    0    |      0      | 00000000 |
                    |    1    |      1      | 00000001 |
                    |    2    |      2      | 00000010 |
                    |    3    |      3      | 00000011 |
                    |    4    |      4      | 00000100 |
                    |    5    |      5      | 00000101 |
                    |    6    |      6      | 00000110 |
                    |    7    |      7      | 00000111 |
                    |    8    |      8      | 00001000 |
                    |    9    |      9      | 00001001 |
                    |   10    |      A      | 00001010 |
                    |   11    |      B      | 00001011 |
                    |   12    |      C      | 00001100 |
                    |   13    |      D      | 00001101 |
                    |   14    |      E      | 00001110 |
                    |   15    |      F      | 00001111 |
                    |   16    |     10      | 00010000 |
                    +---------+-------------+----------+

    Let's look at it another way; here's an example of how a base 10
  (decimal number) is constructed:

    Base raised by
    increasing powers:... 10^3 10^2 10^1 10^0
                         ---------------------
    Equals:.............. 1000  100   10    1
                         ---------------------

    Consider 4569 (base 10)  4    5    6    9 = (4*1000)+(5*100)+(6*10)+9

  Now look at an example of how a base 16 (hexadecimal number) is
  constructed:

    Base raised by
    increasing powers:... 16^3 16^2 16^1 16^0
                         ---------------------
    Equals:.............. 4096  256   16    1
                         ---------------------

    Consider 11D9 (base 16)  1    1    D    9 = 1*4096+1*256+13*16+9

  Therefore, 4569 (base 10) = 11D9 (base 16)
    The range for addressable memory locations is 0-65535 (as was stated
  earlier). This range is therefore 0-FFFF in hexadecimal notation.
    Usually hexadecimal numbers are prefixed with a dollar sign ($). This
  is to distinguish them from decimal numbers. Let's look at some "hex"
  numbers, using 64MON, by displaying the contents of some memory by
  typing:

    SYS 8*4096   (or SYS 12*4096)
    B*
       PC  SR AC XR YR SP
    .;0401 32 04 5E 00 F6 (these may be different)

  Then if you type in:

  .M 0000 0020 (and press <RETURN>).

  you will see rows of 9 hex numbers. The first 4-digit number is the ad-
  dress of the first byte of memory being shown in that row, and the other
  eight numbers are the actual contents of the memory locations beginning
  at that start address.

    You should really try to learn to "think" in hexadecimal. It's not too
  difficult, because you don't have to think about converting it back into
  decimal. For example, if you said that a particular value is stored at
  $14ED instead of 5357, it shouldn't make any difference.

  YOUR FIRST MACHINE LANGUAGE INSTRUCTION

  LDA - LOAD THE ACCUMULATOR

    In 6510 assembly language, mnemonics are always three characters. LDA
  represents "load accumulator with...", and what the accumulator should be
  loaded with is decided by the parameter(s) associated with that
  instruction. The assembler knows which token is represented by each
  mnemonic, and when it "assembles" an instruction, it simply puts into
  memory (at whatever address has been specified), the token, and what
  parameters, are given. Some assemblers give error messages, or warnings
  when you try to assemble something that either the assembler, or the 6510
  microprocessor, cannot do.
    If you put a "#" symbol in front of the parameter associated with the
  instruction, this means that you want the register specified in the
  instruction to be loaded with the "value" after the "#". For example:

    LDA #$05  <----[ $=HEX ]

  This instruction will put $05 (decimal 5) into the accumulator register.
  The assembler will put into the specified address for this instruction,
  $A9 (which is the token for this particular instruction, in this mode),
  and it will put $05 into the next location after the location containing
  the instruction ($A9).
    If the parameter to be used by an instruction has "#" before it; i.e.,
  the parameter is a "value," rather than the contents of a memory loca-
  tion, or another register, the instruction is said to be in the
  "immediate" mode. To put this into perspective, let's compare this with
  another mode:
    If you want to put the contents of memory location $102E into the
  accumulator, you're using the "absolute" mode of instruction:

    LDA $102E

  The assembler can distinguish between the two different modes because the
  latter does not have a "#" before the parameter. The 6510 microprocessor

  can distinguish between the immediate mode, and the absolute mode of the
  LDA instruction, because they have slightly different tokens. LDA
  (immediate) has $A9 as its token, and LDA (absolute), has $AD as its
  token.
    The mnemonic representing an instruction usually implies what it does.
  For instance, if we consider another instruction, LDX, what do you think
  this does?
    If you said "load the X register with...", go to the top of the class.
  If you didn't, then don't worry, learning machine language does take
  patience, and cannot be learned in a day.
    The various internal registers can be thought of as special memory
  locations, because they too can hold one byte of information. It is not
  necessary for us to explain the binary numbering system (base 2) since it
  follows the same rules as outlined for hexadecimal and decimal outlined
  previously, but one "bit" is one binary digit and eight bits make up one
  byte! This means that the maximum number that can be contained in a
  byte is the largest number that an eight digit binary number can be. This
  number is 11111111 (binary), which equals $FF (hexadecimal), which equals
  255 (decimal). You have probably wondered why only numbers from zero to
  255 could be put into a memory location. If you try POKE 7680,260 (which
  is a BASIC statement that "says": "Put the number two hundred and sixty,
  into memory location seven thousand, six hundred and eighty", the BASIC
  interpreter knows that only numbers 0 - 255 can be put in a memory
  location, and your Commodore 64 will reply with:

    ?ILLEGAL QUANTITY ERROR

    READY.

  If the limit of one byte is $FF (hex), how is the address parameter in
  the absolute instruction "LDA $102E" expressed in memory? It's expressed
  in two bytes (it won't fit into one, of course). The lower (rightmost)
  two digits of the hexadecimal address form the "low byte" of the address,
  and the upper (leftmost) two digits form the "high byte."
    The 6510 requires any address to be specified with its low byte first,
  and then the high byte. This means that the instruction "LDA $102E" is
  represented in memory by the three consecutive values:

    $AD, $2E, $10

  Now all you need to know is one more instruction and then you can write
  your first program. That instruction is BRK. For a full explanation of

  this I instruction, refer to M.O.S. 6502 Programming Manual. But right
  now, you can think of it as the END instruction in machine language.
    If we write a program with 64MON and put the BRK instruction at the
  end, then when the program is executed, it will return to 64MON when it
  is finished. This might not happen if there is a mistake in your program,
  or the BRK instruction is never reached (just like an END statement in
  BASIC may never get executed). This means that if the Commodore 64 didn't
  have a STOP key, you wouldn't be able to abort your BASIC programs!

  WRITING YOUR FIRST PROGRAM

    If you've used the POKE statement in BASIC to put characters onto the
  screen, you're aware that the character codes for POKEing are different
  from CBM ASCII character values. For example, if you enter:

    PRINT ASC("A") (and press <RETURN> )

  the Commodore 64 will respond with:

    65

    READY.

  However, to put an "A" onto the screen by POKEing, the code is 1, enter:

    <SHIFT+CLR/HOME> to clear the screen

    POKE 1024,1:POKE 55296,14 (and <RETURN> (1024 is the start of screen
    memory)

  The "P" in the POKE statement should now be an "A."
    Now let's try this in machine language. Type the following in 64MON:
  (Your cursor should be flashing alongside a "." right now.)

    .A 1400 LDA#$01 (and press <RETURN>)

  The Commodore 64 will prompt you with:

    .A 1400 A9 01      LDA #$01
    .A 1402

  Type:

    .A 1402 STA $0400

  (The STA instruction stores the contents of the accumulator in a
  specified memory location.)
  The Commodore 64 will prompt you with:

    .A 1405

  Now type in:

    .A 1405 LDA #$0E
    .A 1407 STA $D800
    .A 140A BRK

  Clear the screen, and type:

    G 1400

    The G should turn into an "A" if you've done everything correctly. You
  have now written your first machine language program. Its purpose is to
  store one character ("A") at the first location in the screen memory.
  Having achieved this, we must now explore some of the other instructions,
  and principles.

  ADDRESSING MODES

  ZERO PAGE

    As shown earlier, absolute addresses are expressed in terms of a high
  and a low order byte. The high order byte is often referred to as the
  page of memory. For example, the address $1637 is in page $16 (22), and
  $0277 is in page $02 (2). There is, however, a special mode of addressing
  known as zero page addressing and is, as the name implies, associated

  with the addressing of memory locations in page zero. These addresses,
  therefore, ALWAYS have a high order byte of zero. The zero page mode of
  addressing only expects one byte to describe the address, rather than two
  when using an absolute address. The zero page addressing mode tells the
  microprocessor to assume that the high order address is zero. Therefore
  zero page addressing can reference memory locations whose addresses are
  between $0000 and $00FF. This may not seem too important at the moment,
  but you'll need the principles of zero page addressing soon.

  THE STACK

    The 6510 microprocessor has what is known as a stack. This is used by
  both the programmer and the microprocessor to temporarily remember
  things, and to remember, for example, an order of events. The GOSUB
  statement in BASIC, which allows the programmer to call a subroutine,
  must remember where it is being called from, so that when the RETURN
  statement is executed in the subroutine, the BASIC interpreter "knows"
  where to go back to continue executing. When a GOSUB statement is
  encountered in a program by the BASIC interpreter, the BASIC interpreter
  "pushes" its current position onto the stack before going to do the
  subroutine, and when a RETURN is executed, the interpreter "pulls" off
  the stack the information that tells it where it was before the
  subroutine call was made. The interpreter uses instructions like PHA,
  which pushes the contents of the accumulator onto the stack, and PLA (the
  reverse) which pulls a value off the stack and into the accumulator. The
  status register can also be pushed and pulled with the PHP and PLP,
  respectively.
    The stack is 256 bytes long, and is located in page one of memory. It
  is therefore from $01 00 to $01 FF. It is organized backwards in memory.
  In other words, the first position in the stack is at $01 FF, and the
  last is at $0100. Another register in the 651 0 microprocessor is called
  the stack pointer, and it always points to the next available location in
  the stack. When something is pushed onto the stack, it is placed where
  the stack pointer points to, and the stack pointer is moved down to the
  next position (decremented). When something is pulled off the stack, the
  stack pointer is incremented, and the byte pointed to by the stack
  pointer is placed into the specified register.

    Up to this point, we have covered immediate, zero page, and absolute
  mode instructions. We have also covered, but have not really talked
  about, the "implied" mode. The implied mode means that information is
  implied by an instruction itself. In other words, what registers, flags,
  and memory the instruction is referring to. The examples we have seen are
  PHA, PLA, PHP, and PLP, which refer to stack processing and the
  accumulator and status registers, respectively.

  +-----------------------------------------------------------------------+
  | NOTE: The X register will be referred to as X from now on, and        |
  | similarly A (accumulator), Y (Y index register), S (stack pointer),   |
  | and P (processor status).                                             |
  +-----------------------------------------------------------------------+

  INDEXING

    Indexing plays an extremely important part in the running of the 6510
  microprocessor. It can be defined as "creating an actual address from a
  base address plus the contents of either the X or Y index registers."
    For example, if X contains $05, and the microprocessor executes an LDA
  instruction in the "absolute X indexed mode" with base address (e.g.,
  $9000), then the actual location that is loaded into the A register is
  $9000 + $05 = $9005. The mnemonic format of an absolute indexed
  instruction is the same as an absolute instruction except a ",X" or ",Y"
  denoting the index is added to the address.

  EXAMPLE:

    LDA $9000,X

    There are absolute indexed, zero page indexed, indirect indexed, and
  indexed indirect modes of addressing available on the 6510
  microprocessor.

  INDIRECT INDEXED

    This only allows usage of the Y register as the index. The actual ad-
  dress can only be in zero page, and the mode of instruction is called
  indirect because the zero page address specified in the instruction con-
  tains the low byte of the actual address, and the next byte to it
  contains the high order byte.

  EXAMPLE:

    Let us suppose that location $02 contains $45, and location $03 con-
  tains $1E. If the instruction to load the accumulator in the indirect
  indexed mode is executed and the specified zero page address is $02, then
  the actual address will be:

    Low order = contents of $02
    High order = contents of $03
    Y register = $00

  Thus the actual address = $1E45 + Y = $1E45.
    The title of this mode does in fact imply an indirect principle,
  although this may be difficult to grasp at first sight. Let's look at it
  another way:
    "I am going to deliver this letter to the post office at address $02,
  MEMORY ST., and the address on the letter is $05 houses past $1600,
  MEMORY street." This is equivalent to the code:

    LDA #$00      - load low order actual base address
    STA $02       - set the low byte of the indirect address
    LDA #$16      - load high order indirect address
    STA $03       - set the high byte of the indirect address
    LDY #$05      - set the indirect index (Y)
    LDA ($02),Y   - load indirectly indexed by Y

  INDEXED INDIRECT

    Indexed indirect only allows usage of the X register as the index. This
  is the some as indirect indexed, except it is the zero page address of
  the pointer that is indexed, rather than the actual base address.
  Therefore, the actual base address IS the actual address because the
  index has already been used for the indirect. Index indirect would also
  be used if a table of indirect pointers were located in zero page memory,
  and the X register could then specify which indirect pointer to use.

  EXAMPLE:

    Let us suppose that location $02 contains $45, and location $03 con-
  tains $10. If the instruction to load the accumulator in the indexed
  indirect mode is executed and the specified zero page address is $02,
  then the actual address will be:

    Low order = contents of ($02+X)
    High order = contents of ($03+X)
    X register = $00

  Thus the actual pointer is in = $02 + X = $02.
    Therefore, the actual address is the indirect address contained in $02
  which is again $1045.
    The title of this mode does in fact imply the principle, although it
  may be difficult to grasp at first sight. Look at it this way:
    "I am going to deliver this letter to the fourth post office at address
  $01,MEMORY ST., and the address on the letter will then be delivered to
  $1600, MEMORY street." This is equivalent to the code:

    LDA #$00    - load low order actual base address
    STA $06     - set the low byte of the indirect address
    LDA #$16    - load high order indirect address
    STA $07     - set the high byte of the indirect address
    LDX #$05    - set the indirect index (X)
    LDA ($02,X) - load indirectly indexed by X

  +-----------------------------------------------------------------------+
  | NOTE: Of the two indirect methods of addressing, the first (indirect  |
  | indexed) is far more widely used.                                     |
  +-----------------------------------------------------------------------+

  BRANCHES AND TESTING

    Another very important principle in machine language is the ability to
  test, and detect certain conditions, in a similar fashion to the "IF...
  THEN, IF... GOTO" structure in CBM BASIC.
    The various flags in the status register are affected by different in-
  structions in different ways. For example, there is a flag that is set
  when an instruction has caused a zero result, and is reset when a result
  is not zero. The instruction:

    LDA #$00

  will cause the zero result flag to be set, because the instruction has
  resulted in the accumulator containing a zero.
    There are a set of instructions that will, given a particular
  condition, branch to another part of the program. An example of a branch
  instruction is BEQ, which means Branch if result EQual to zero. The
  branch instructions branch if the condition is true, and if not, the
  program continues onto the next instruction, as if nothing had occurred.
  The branch instructions branch not by the result of the previous
  instructions), but by internally examining the status register. As was
  just mentioned, there is a zero result flag in the status register. The
  BEQ instruction branches if the zero result flag (known as Z) is set.
  Every branch instruction has an opposite branch instruction. The BEQ
  instruction has an opposite instruction BNE, which means Branch on result
  Not Equal to zero (i.e., Z not set).
    The index registers have a number of associated instructions which
  modify their contents. For example, the INX instruction INcrements the X
  index register. If the X register contained $FF before it was incremented
  (the maximum number the X register can contain), it will "wrap around"
  back to zero. If you wanted a program to continue to do something until
  you had performed the increment of the X index that pushed it around to
  zero, you could use the BNE instruction to continue "looping" around,
  until X became zero.
    The reverse of INX, is DEX, which is DEcrement the X index register. If
  the X index register is zero, DEX wraps around to $FF. Similarly, there
  are INY and DEY for the Y index register.

    But what if a program didn't want to wait until X or Y had reached (or
  not reached) zero? Well there are comparison instructions, CPX and CPY,
  which allow the machine language programmer to test the index registers
  with specific values, or even the contents of memory locations. If you
  wanted to see if the X register contained $40, you would use the
  instruction:

    CPX #$40         - compare X with the "value" $40.
    BEQ              - branch to somewhere else in the
    (some other        program, if this condition is "true."
     part of the
     program)

  The compare, and branch instructions play a major part in any machine
  language program.
    The operand specified in a branch instruction when using 64MON is the
  address of the part of the program that the branch goes to when the
  proper conditions are met. However, the operand is only an offset, which
  gets you from where the program currently is to the address specified.
  This offset is just one byte, and therefore the range that a branch
  instruction can branch to is limited. It can branch from 128 bytes back-
  ward, to 127 bytes forward.

  +-----------------------------------------------------------------------+
  | NOTE: This is a total range of 255 bytes which is, of course, the     |
  | maximum range of values one byte can contain.                         |
  +-----------------------------------------------------------------------+

    64MON will tell you if you "branch out of range" by refusing to "as-
  semble" that particular instruction. But don't worry about that now be-
  cause it's unlikely that you will have such branches for quite a while.
  The branch is a "quick" instruction by machine language standards because
  of the "offset" principle as opposed to an absolute address. 64MON allows
  you to type in an absolute address, and it calculates the correct offset.
  This is just one of the "comforts" of using an assembler.

  +-----------------------------------------------------------------------+
  | NOTE: It is NOT possible to cover every single branch instruction. For|
  | further information, refer to the Bibliography section in Appendix F. |
  +-----------------------------------------------------------------------+

  SUBROUTINES

    In machine language (in the same way as using BASIC), you can call
  subroutines. The instruction to call a subroutine is JSR (Jump to Sub-
  Routine), followed by the specified absolute address.
    Incorporated in the operating system, there is a machine language
  subroutine that will PRINT a character to the screen. The CBM ASCII code
  of the character should be in the accumulator before calling the
  subroutine. The address of this subroutine is $FFD2.
    Therefore, to print "Hi" to the screen, the following program should be
  entered:

    .A 1400 LDA #$48     - load the CBM ASCII code of "H"
    .A 1402 JSR $FFD2    -  print it
    .A 1405 LDA #$49     - load the CBM ASCII code of "I"
    .A 1407 JSR $FFD2    -  print that too
    .A 140A LDA #$0D     - print a carriage return as well
    .A 140C JSR $FFD2
    .A 140F BRK          - return to 64MON
    .G 1400              - will print "HI" and return to 64MON

    The "PRINT a character" routine we have just used is part of the KERNAL
  jump table. The instruction similar to GOTO in BASIC is JMP, which means
  JUMP to the specified absolute address. The KERNAL is a long list of
  "standardized" subroutines that control ALL input and output of the
  Commodore 64. Each entry in the KERNAL JMPs to a subroutine in the
  operating system. This "jump table" is found between memory locations
  $FF84 to $FFF5 in the operating system. A full explanation of the KERNAL
  is available in the "KERNAL Reference Section" of this manual. However,
  certain routines are used here to show how easy and effective the KERNAL
  is.
    Let's now use the new principles you've just learned in another pro-
  gram. It will help you to put the instructions into context:

    This program. will display the alphabet using a KERNAL routine. The
  only new instruction introduced here is TXA Transfer the contents of the
  X index register, into the Accumulator.

    .A 1400 LDX #$41     - X = CBM ASCII of "A"
    .A 1402 TXA          - A = X
    .A 1403 JSR $FFD2    - print character
    .A 1406 INX          - bump count
    .A 1407 CPX #$5B     - have we gone past "Z"?
    .A 1409 BNE $1402    - no, go back and do more
    .A 140B BRK          - yes, return to 64MON

    To see the Commodore 64 print the alphabet, type the familiar command:

    .G 1400

    The comments that are beside the program, explain the program flow and
  logic. If you are writing a program, write it on paper first, and then
  test it in small parts if possible.

  USEFUL TIPS FOR THE BEGINNER

    One of the best ways to learn machine language is to look at other
  peoples' machine language programs. These are published all the time in
  magazines and newsletters. Look at them even if the article is for a
  different computer, which also uses the 6510 (or 6502) microprocessor.
  You should make sure that you thoroughly understand the code that you
  look at. This will require perseveres I ce, especially when you see a new
  technique that you have never come across before. This can be infuriat-
  ing, but if patience prevails, you will be the victor.
    Having looked at other machine language programs, you MUST write your
  own. These may be utilities for your BASIC programs, or they may be an
  all machine language program.

    You should also use the utilities that are available, either IN your
  computer, or in a program, that aid you in writing, editing, or tracking
  down errors in a machine language program. An example would be the
  KERNAL, which allows you to check the keyboard, print text, control
  peripheral devices like disk drives, printers, modems, etc., manage
  memory and the screen. It is extremely powerful and it is advised
  strongly that it is used (refer to KERNAL section, Page 268).
    Advantages of writing programs in machine language:

    1. Speed - Machine language is hundreds, and in some cases thousands of
       times faster than a high level language such as BASIC.

    2. Tightness - A machine language program can be made totally
       "watertight," i.e., the user can be made to do ONLY what the program
        allows, and no more. With a high level language, you are relying on
        the user not "crashing" the BASIC interpreter by entering, for
        example, a zero which later causes a:

  ?DIVISION BY ZERO ERROR IN LINE 830

  READY.

  In essence, the computer can only be maximized by the machine language
  programmer.

  APPROACHING A LARGE TASK

    When approaching a large task in machine language, a certain amount of
  subconscious thought has usually taken place. You think about how certain
  processes are carried out in machine language. When the task is started,
  it is usually a good idea to write it out on paper. Use block diagrams of
  memory usage, functional modules of code required, and a program flow.
  Let's say that you wanted to write a roulette game in machine language.
  You could outline it something like this:

    o Display title
    o Ask if player requires instructions
    o YES - display them-Go to START
    o NO - Go to START
    o START Initialize everything
    o MAIN display roulette table
    o Take in bets
    o Spin wheel
    o Slow wheel to stop
    o Check bets with result
    o Inform player
    o Player any money left?
    o YES - Go to MAIN
    o NO - Inform user!, and go to START

    This is the main outline. As each module is approached, you can break
  it down further. If you look at a large indigestable problem as something
  that can be broken down into small enough pieces to be eaten, then you'll
  be able to approach something that seems impossible, and have it all fall
  into place.
    This process only improves with practice, so KEEP TRYING.

  +------------------------------------------------------------------------
  |
