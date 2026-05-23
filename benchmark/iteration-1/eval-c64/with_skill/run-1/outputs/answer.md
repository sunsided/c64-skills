# C64 Orientation — caveman map

## Five chips run machine

| Chip | Job | Lives at |
|------|-----|----------|
| **6510** CPU | runs code; port `$00/$01` banks ROM/RAM | — |
| **VIC-II** (6567 NTSC / 6569 PAL) | screen, sprites, raster | `$D000-$D3FF` |
| **SID** 6581 | 3-voice sound + filter | `$D400-$D7FF` |
| **CIA1** 6526 | keyboard, joysticks, timer IRQ | `$DC00-$DCFF` |
| **CIA2** 6526 | serial bus (disk!), user port, NMI | `$DD00-$DDFF` |

ROM: BASIC `$A000`, KERNAL `$E000`. Color RAM `$D800`. Default screen RAM `$0400`.

## Memory map quick

```
$0000-$00FF  zero page ($00/$01 = bank switch)
$0100-$01FF  CPU stack
$0200-$03FF  OS work area (IRQ vector $0314)
$0400-$07FF  screen RAM (sprite pointers $07F8-$07FF)
$0800-$9FFF  BASIC program / free RAM
$A000-$BFFF  BASIC ROM (or RAM)
$C000-$CFFF  free 4K RAM — favourite ML spot
$D000-$DFFF  I/O: VIC/SID/colorRAM/CIA1/CIA2
$E000-$FFFF  KERNAL ROM
```

## Where look for...

**Sound** → SID at `$D400` (53248+ decimal... no, 54272). Voice 1 freq `$D400/$D401`, waveform `$D404`, volume `$D418`. Skill: **c64-sid**.

```basic
POKE 54296,15 : POKE 54277,9 : POKE 54278,0
POKE 54273,40 : POKE 54276,17
```

**Sprites** → VIC-II. Enable `$D015` (53269). X/Y pos `$D000-$D00F`. Pointers `$07F8-$07FF`. Skill: **c64-sprites**.

```basic
POKE 53269,1 : POKE 2040,13 : POKE 53248,160 : POKE 53249,100
```

**Joystick** → CIA1. Port 2 = `$DC00` (56320), port 1 = `$DC01` (56321). Bits 0-4 = up/down/left/right/fire, **0 = pressed**. Most games use port 2. Skill: **c64-game-ports**.

```basic
J = PEEK(56320) : IF (J AND 16)=0 THEN PRINT "FIRE"
```

**Disk drive** → device 8 on serial bus, runs through CIA2 `$DD00`. Use KERNAL/BASIC, not POKEs. Directory `LOAD"$",8` then `LIST`. Load file `LOAD"NAME",8` (or `,8,1` for ML at its address). Skill: **c64-disk**.

## Next step

Pick task → open matching `c64-*` skill for registers + code. New coder: start **c64-basic** + **c64-petscii**, then **c64-sprites**/**c64-sid** for fun.