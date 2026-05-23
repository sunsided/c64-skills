# C64 Orientation

**3 main chips:**

| Chip | Job | Base address |
|------|-----|--------------|
| **6510** | CPU (6502 + I/O port) | runs everything; I/O port at `$0000/$0001` |
| **VIC-II** (6567/6569) | video, sprites, screen | `$D000–$D02E` (53248+) |
| **SID** (6581/8580) | sound | `$D400–$D41C` (54272+) |
| **2× CIA** (6526) | timers, keyboard, joystick, serial bus | CIA1 `$DC00`, CIA2 `$DD00` |

## Memory map big picture
- `$0000–$00FF` zero page (fast access)
- `$0400–$07E7` default screen RAM (1000 bytes)
- `$0800–$9FFF` BASIC program + free RAM
- `$A000–$BFFF` BASIC ROM
- `$D000–$DFFF` I/O chips (VIC/SID/CIA) — or color RAM / char ROM, banked
- `$E000–$FFFF` KERNAL ROM

64K total. ROMs overlay RAM; `$0001` bank bits switch them in/out.

## Sound → SID `$D400` (54272)
3 voices, 7 registers each. Voice 1 example:
- `54272/3` freq lo/hi
- `54276` waveform+gate (e.g. `17` = sawtooth on)
- `54277` attack/decay, `54278` sustain/release
- `54296` master volume (0–15)

```basic
10 POKE 54296,15: REM VOLUME MAX
20 POKE 54277,9: POKE 54278,0: REM AD / SR
30 POKE 54273,40: REM FREQ HI
40 POKE 54276,33: REM TRIANGLE + GATE ON
50 FOR T=1 TO 300: NEXT
60 POKE 54276,32: REM GATE OFF
```

## Sprites → VIC-II `$D000` (53248)
- `$D000–$D00F` (53248–63) X/Y pos, sprite 0–7
- `$D015` (53269) enable bits (1 bit per sprite)
- `$D027–$D02E` (53287+) sprite colors
- pointers at end of screen RAM: `2040–2047` (×64 = data address)

```basic
10 POKE 2040,13: REM SPRITE 0 DATA AT 13*64=832
20 POKE 53269,1: REM ENABLE SPRITE 0
30 POKE 53248,100: POKE 53249,100: REM X,Y
40 POKE 53287,1: REM COLOR WHITE
```

## Joystick → CIA `$DC00`/`$DC01`
- **Port 2** = `$DC00` (56320)
- **Port 1** = `$DC01` (56321)
- bits 0–4 = up/down/left/right/fire, **active low** (0 = pressed)

```basic
10 J=PEEK(56320): REM PORT 2
20 IF (J AND 1)=0 THEN PRINT "UP"
30 IF (J AND 2)=0 THEN PRINT "DOWN"
40 IF (J AND 4)=0 THEN PRINT "LEFT"
50 IF (J AND 8)=0 THEN PRINT "RIGHT"
60 IF (J AND 16)=0 THEN PRINT "FIRE"
70 GOTO 10
```
Note: port 1 shares keyboard matrix lines (CIA1 reads keyboard too).

## Disk drive → serial bus via CIA2 + KERNAL
1541 = external, talks over IEC serial bus (CIA2 `$DD00` handles lines). Don't poke it directly — use BASIC/KERNAL:
```basic
LOAD "$",8     : REM DIRECTORY
LOAD "NAME",8  : REM LOAD PROGRAM
LOAD "NAME",8,1: REM LOAD TO ITS OWN ADDRESS
OPEN 1,8,15,"command$": REM COMMAND CHANNEL
```
`8` = device number. KERNAL routines: `SETLFS $FFBA`, `SETNAM $FFBD`, `LOAD $FFD5`, `SAVE $FFD8`.

## Quick mental model
Sound+graphics = on-chip (VIC/SID, poke registers directly). Input+disk = CIA chips (`$DC00`/`$DD00`), but disk you drive through KERNAL not raw pokes.

Want a deeper dive on any one chip?