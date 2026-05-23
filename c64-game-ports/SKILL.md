---
name: c64-game-ports
description: >-
  The two Commodore 64 control (game) ports: reading joysticks, paddles, a light
  pen, and mouse, and how they map to hardware registers (CIA1 $DC00/$DC01, SID
  POT $D419/$D41A, VIC light-pen $D013/$D014). Use this skill WHEN a user asks
  "which port is player 1", "how do I read the joystick", "what bits are up/down/
  left/right/fire", "how do I read paddles", "why are paddles unreliable in
  BASIC", "how does the light pen work", or mentions control port 1/2, $DC00,
  $DC01, fire button, or POTX/POTY. Pairs with c64-cia, c64-sid, and c64-vic-ii.
---

# C64 Control (Game) Ports

The C64 has **two DE-9 control ports** on the right side. Each takes one joystick
or one paddle pair; a light pen goes in control port 1 only. The ports are wired
to **CIA1** (the joystick/fire-button/keyboard-scan chip) and, for paddles, to the
**SID** POT lines.

## Hardware mapping — which register is which port

| Read at | CIA1 register | Reads control port |
|---------|---------------|--------------------|
| 56321 / **$DC01** | Port B (PRB) | **Control port 1** |
| 56320 / **$DC00** | Port A (PRA) | **Control port 2** |

Note the crossover: port **1** is at the **higher** address ($DC01), port **2**
at the **lower** ($DC00). Each port's joystick uses the **low 5 bits**:

```
bit 4 3 2 1 0
    │ │ │ │ └─ 0 = UP     (switch 0)
    │ │ │ └─── 1 = DOWN   (switch 1)
    │ │ └───── 2 = LEFT   (switch 2)
    │ └─────── 3 = RIGHT  (switch 3)
    └───────── 4 = FIRE   (switch 4)
```

**Active LOW:** a bit reads **1 when the switch is open** (not pressed) and **0
when closed** (pressed/pushed). So "no input" reads `%11111` = 31 on the low 5
bits; pushing up pulls bit 0 to 0, etc. Bits 5–7 carry other CIA1 data (keyboard
matrix, paddle select).

## Reading a joystick

BASIC (port 2 here; use $DC01 / PEEK(56321) for port 1):

```basic
100 JV=PEEK(56320)        : REM raw port-2 value
110 FR=(JV AND 16)        : REM 0 = fire pressed, 16 = not pressed
120 JV=15-(JV AND 15)     : REM 0=none,1=up,2=down,4=left,8=right (combine for diagonals)
```

| JV (after line 120) | Direction |
|---------------------|-----------|
| 0 | none |
| 1 | up |
| 2 | down |
| 4 | left |
| 5 | up & left |
| 6 | down & left |
| 8 | right |
| 9 | up & right |
| 10 | down & right |

Assembly (reads port 2 at $DC00; use $DC01 for port 1; carry = fire state):

```asm
djrr    lda $dc00     ; read port (use $dc01 for the other port)
        ldy #0
        ldx #0
        lsr a         ; shift each direction bit into carry
        bcs djr0      ; bit 0 (up):   carry set = switch open
        dey           ;               switch closed -> dy = -1 (move up)
djr0    lsr a         ; bit 1 (down)
        bcs djr1
        iny
djr1    lsr a         ; bit 2 (left)
        bcs djr2
        dex
djr2    lsr a         ; bit 3 (right)
        bcs djr3
        inx
djr3    lsr a         ; bit 4 -> carry = FIRE (C=1 not pressed, C=0 pressed)
        stx dx        ; dx/dy are 2's-complement -1/0/+1 deltas
        sty dy
        rts
```

### Keyboard-scan conflict on port 1

CIA1 also scans the keyboard, and the keyboard matrix shares lines with the
control ports — especially **port 1** (PRB/$DC01), which is on the same side the
keyboard rows/columns use. Reading a joystick in port 1 can register phantom
keypresses and vice versa; pressing certain keys can look like joystick motion.
This is why single-joystick software overwhelmingly prefers port 2. The full CIA1
keyboard-scan register behavior is in **c64-cia**.

## Which port is player 1?

Hardware facts: **control port 1 reads at $DC01**, **control port 2 reads at
$DC00**. There is no hardware notion of "player 1" — both ports are equal silicon.
By long-standing software **convention**, single-player and one-joystick games
most often use **control port 2** (it dodges the keyboard-scan interference on
port 1). Two-player games then use port 1 for player 2. But this is convention,
not a hardware law — always check the specific game; some titles use port 1.

## Paddles

A paddle pair connects through a game port to both CIA1 and SID. The analog
position is read from the **SID POT registers**:

| Register | Addr | |
|----------|------|-|
| POTX | 54297 / **$D419** | paddle X position (0–255) |
| POTY | 54298 / **$D41A** | paddle Y position (0–255) |

Each port has two pots (X and Y), so two paddles per port = up to **four paddles**
total. But SID has only one POTX/POTY pair, so you **select which port's pots are
connected** via the top two bits of **CIA1 Port A ($DC00)**: write `$40`/`$80` to
PRA to switch the multiplexer between the two paddle pairs, wait briefly for the
RC reading to settle, then read $D419/$D41A. Paddle fire buttons appear on the
joystick bits (bit 2 = pot-X button, bit 3 = pot-Y button).

**PADDLES ARE NOT RELIABLE READ FROM BASIC ALONE** — the timing/multiplexing is
too tight, so even from BASIC you SYS a short ML routine (the manual's `pdlrd`
routine, also given as DATA statements) and PEEK the results. Full routine in
`references/game-ports.md`. The SID POT register details live in **c64-sid**.

## Light pen

A light pen plugs into **control port 1 only**. On a low-going edge (the pen
sensing the beam) the VIC-II latches the current beam position:

| Register | Addr | Contents |
|----------|------|----------|
| LPX | 19 / **$D013** | X latch — high 8 bits of a 9-bit (512-state) X counter → 2-dot resolution |
| LPY | 20 / **$D014** | Y latch — 8 bits, single-raster resolution in the visible area |

The latch fires **at most once per frame** (later triggers in the same frame are
ignored), and reads are noisy, so **average several samples** (3+). Light-pen
register/IRQ detail is in **c64-vic-ii**.

## Mouse

The Commodore 1351 mouse plugs into a control port and, in its proportional mode,
reports movement through the same **SID POT registers ($D419/$D41A)** the paddles
use (its buttons appear on the joystick fire/direction bits). The C64 manuals
predate the 1351 and don't document it; treat it as a paddle-style POT device on
the control port.

## Quick answers

- **"Which port is player 1?"** Hardware: port 1 = $DC01, port 2 = $DC00, no
  built-in "player" meaning. By convention single-joystick games use **port 2**.
- **"How do I read the joystick?"** `JV=PEEK(56320)` (port 2) or `PEEK(56321)`
  (port 1); bits 0–4 = up/down/left/right/fire, active LOW.
- **"How do I tell if fire is pressed?"** `(PEEK(56320) AND 16)=0` → pressed.
- **"Why are paddles garbage in BASIC?"** Timing — SYS the ML read routine and
  PEEK the values from $D419/$D41A.

## How to read the references

- **`references/game-ports.md`** — verbatim PRG Ch6 "The Game Ports", "Paddles",
  and "Light Pen": the joystick switch diagram, the BASIC + assembly joystick
  read routines, the JV→direction table, the full four-paddle ML read routine
  (with DATA-statement BASIC loader), and the light-pen latch description. Read
  this for the exact code and the paddle multiplexing/select sequence.

## Cross-links

- CIA1 registers, data-direction, and the keyboard-scan that conflicts on port 1
  → **c64-cia**
- The SID POT (paddle) registers $D419/$D41A → **c64-sid**
- The VIC-II light-pen latch $D013/$D014 and its IRQ → **c64-vic-ii**
