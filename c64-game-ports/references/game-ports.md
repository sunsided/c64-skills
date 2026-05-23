> Source: c64prg.txt Ch6, "The Game Ports", "Paddles", and "Light Pen". Lightly cleaned from the Project 64 etext.

# The Game Ports

The Commodore 64 has two 9-pin Game Ports which allow the use of joysticks, paddles, or a light pen. Each port will accept either one joystick or one paddle pair. A light pen can be plugged into Port A (only) for special graphic control, etc. This section gives you examples of how to use the joysticks and paddles from both BASIC and machine language.

The digital joystick is connected to CIA #1 (MOS 6526 Complex Interface Adapter). This input/output device also handles the paddle fire buttons and keyboard scanning. The 6526 CIA chip has 16 registers which are in memory locations 56320 through 56335 inclusive ($DC00 to $DC0F). Port A data appears at location 56320 ($DC00) and Port B data is found at location 56321 ($DC01).

A digital joystick has five distinct switches, four of the switches are used for direction and one of the switches is used for the fire button. The joystick switches are arranged as shown:

                                    (Top)
                FIRE
             (Switch 4)
                                     UP
                                 (Switch 0)
                                      |
                                      |
                                      |
                         LEFT         |         RIGHT
                               -------+-------
                      (Switch 2)      |       (Switch 3)
                                      |
                                      |
                                      |
                                    DOWN
                                 (Switch 1)

These switches correspond to the lower 5 bits of the data in location 56320 or 56321. Normally the bit is set to a one if a direction is NOT chosen or the fire button is NOT pressed. When the fire button is pressed, the bit (bit 4 in this case) changes to a 0. To read the joystick from BASIC, the following subroutine should be used:

    10 fork=0to10:rem set up direction string
    20 readdr$(k):next
    30 data"","n","s","","w","nw"
    40 data"sw","","e","ne","se"
    50 print"going...";
    60 gosub100:rem read the joystick
    65 ifdr$(jv)=""then80:rem check if a direction was chosen
    70 printdr$(jv);" ";:rem output which direction
    80 iffr=16then60:rem check if fire button was pushed
    90 print"-----f-----i-----r-----e-----!!!":goto60
    100 jv=peek(56320):rem get joystick value
    110 fr=jvand16:rem form fire button status
    120 jv=15-(jvand15):rem form direction value
    130 return

    NOTE: For the second joystick, set JV = PEEK (56321).

The values for JV correspond to these directions:

                       +-------------+---------------+
                       | JV EQUAL TO |   DIRECTION   |
                       +-------------+---------------+
                       |      0      |          NONE |
                       |      1      |            UP |
                       |      2      |          DOWN |
                       |      3      |             - |
                       |      4      |          LEFT |
                       |      5      |     UP & LEFT |
                       |      6      |   DOWN & LEFT |
                       |      7      |             - |
                       |      8      |         RIGHT |
                       |      9      |    UP & RIGHT |
                       |     10      |  DOWN & RIGHT |
                       +-------------+---------------+

A small machine code routine which accomplishes the same task is as follows:

                      ; joystick - button read routine
                      ;
                      ; author - bill hindorff
                      ;
    dx = $c110
    dy = $c111

    * = $c200

    djrr    lda $dc00     ; get input from port a only
    djrrb   ldy #0        ; this routine reads and decodes the
            ldx #0        ; joystick/firebutton input data in
            lsr a         ; the accumulator. this least significant
            bcs djr0      ; 5 bits contain the switch closure
            dey           ; information. if a switch is closed then it
    djr0    lsr a         ; produces a zero bit. if a switch is open then
            bcs djr1      ; it produces a one bit. The joystick dir-
            iny           ; ections are right, left, forward, backward
    djr1    lsr a         ; bit3=right, bit2=left, bit1=backward,
            bcs djr2      ; bit0=forward and bit4=fire button.
            dex           ; at rts time dx and dy contain 2's compliment
    djr2    lsr a         ; direction numbers i.e. $ff=-1, $00=0, $01=1.
            bcs djr3      ; dx=1 (move right), dx=-1 (move left),
            inx           ; dx=0 (no x change). dy=-1 (move up screen),
    djr3    lsr a         ; dy=0 (move down screen), dy=0 (no y change).
            stx dx        ; the forward joystick position corresponds
            sty dy        ; to move up the screen and the backward
            rts           ; position to move down screen.
                          ;
                          ; at rts time the carry flag contains the fire
                          ; button state. if c=1 then button not pressed.
                          ; if c=0 then pressed.
    .end

# Paddles

A paddle is connected to both CIA #1 and the SID chip (MOS 6581 Sound Interface Device) through a game port. The paddle value is read via the SID registers 54297 ($D419) and 54298 ($D41A). PADDLES ARE NOT RELIABLE WHEN READ FROM BASIC ALONE!!!! The best way to use paddles, from BASIC or machine code, is to use the following machine language routine... (SYS to it from BASIC then PEEK the memory locations used by the subroutine).

                      ; four paddle read routine (can also be used for two)
                      ;
                      ; author - bill hindorff
                      ;
    porta=$dc00
    ciddra=$dc02
    sid=$d400

    *=$c100

    buffer  *=*+1
    pdlx    *=*+2
    pdly    *=*+2
    btna    *=*+1
    btnb    *=*+1

    * = $c000

    pdlrd   ldx #1        ; for four paddles or two analog joysticks
    pdlrd0                ; entry point for one pair (condition x 1st)
            sei
            lda ciddra    ; get current value of ddr
            sta buffer    ; save it away
            lda #$c0
            sta ciddra    ; set port a for input
            lda #$80
    pdlrd1
            sta porta     ; address a pair of paddles
            ldy #$80      ; wait a while
    pdlrd2
            nop
            dey
            bpl pdlrd2
            lda sid+25    ; get x value
            sta pdlx,x
            lda sid+26
            sta pdly,x    ; get y value
            lda porta     ; time to read paddle fire buttons
            ora #80       ; make it the same as other pair
            sta btna      ; bit 2 is pdl x, bit 3 is pdl y
            lda #$40
            dex           ; all pairs done?
            bpl pdlrd1    ; no
            lda buffer
            sta ciddra    ; restore previous value of ddr
            lda porta+1   ; for 2nd pair -
            sta btnb      ; bit 2 is pdl x, bit 3 is pdl y
            cli
            rts
    .end

The paddles can be read by using the following BASIC program:

    10 c=12*4096:rem set paddle routine start
    11 rem poke in the paddle reading routine
    15 fori=0to63:reada:pokec+i,a:next
    20 sysc:rem call the paddle routine
    30 p1=peek(c+257):rem set paddle one value
    40 p2=peek(c+258):rem set paddle two value
    50 p3=peek(c+259):rem set paddle three value
    60 p4=peek(c+260):rem set paddle four value
    61 rem read fire button status
    62 s1=peek(c+261):s2=peek(c+262)
    70 printp1,p2,p3,p4:rem print paddle values
    72 rem print fire button status
    75 print:print"fire a ";s1,"fire b ";s2
    80 forw=1to50:next:rem wait a while
    90 print"{clear}":print:goto20:rem clear screen and do again
    95 rem data for machine code routine
    100 data162,1,120,173,2,220,141,0,193,169,192,141,2,220,169
    110 data128,141,0,220,160,128,234,136,16,252,173,25,212,157
    120 data1,193,173,26,212,157,3,193,173,0,220,9,128,141,5,193
    130 data169,64,202,16,222,173,0,193,141,2,220,173,1,220,141
    140 data6,193,88,96

# Light Pen

The light pen input latches the current screen position into a pair of registers (LPX, LPY) on a low-going edge. The X position register 19 ($13) will contain the 8 MSB of the X position at the time of transition. Since the X position is defined by a 512-state counter (9 bits), resolution to 2 horizontal dots is provided. Similarly, the Y position is latched in its register 20 ($14), but here 8 bits provide single raster resolution within the visible display. The light pen latch may be triggered only once per frame, and subsequent triggers within the same frame will have no effect. Therefore, you must take several samples before turning the pen to the screen (3 or more samples average), depending upon the characteristics of your light pen.
