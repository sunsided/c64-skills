**Paddle hardware basics.** SID has only ONE pot pair (POTX, POTY pins). Both control ports' paddles wire through analog mux. CIA1 picks which port's pair reaches SID.

**Select register — CIA1 Port A `$DC00` (56320), bits 6 & 7:**

| Value | Bits | Selects |
|-------|------|---------|
| `$40` (64) | PA6=1, PA7=0 | control **port 1** paddles |
| `$80` (128) | PA6=0, PA7=1 | control **port 2** paddles |

One pair at a time. PA6/PA7 must be outputs in DDRA `$DC02` (56322) — default already `$FF`, all outputs.

**Read position — SID pot registers (0–255 each):**
- POTX = `$D419` (54297)
- POTY = `$D41A` (54298)

After select: POTX = first paddle of pair, POTY = second.

**Fire buttons** = joystick left/right lines. Port 1 → read `$DC01` (56321); port 2 → read `$DC00`. Paddle A button = bit 2, paddle B button = bit 3 (0 = pressed).

---

**Why awkward with keyboard:**

1. `$DC00` PA6/PA7 do double duty — they're keyboard matrix **column drive** lines AND the paddle select. Forcing them for paddles drives keyboard columns 6/7.
2. KERNAL IRQ scans keyboard every jiffy (1/60s) and **rewrites `$DC00`**, clobbering your select → garbage reads. Must disable IRQ (`SEI`) or stop CIA1 timer during read.
3. SID measures pot via cap-charge timing: register updates only every **512 φ2 cycles**. Must wait after switching select before reading.

---

**Assembly — read port 1 paddles:**

```asm
        SEI                 ; stop KERNAL keyboard IRQ (it overwrites $DC00)
        LDA #$40            ; PA6=1, PA7=0 -> select control port 1
        STA $DC00
        LDX #$00
DELAY   DEX                 ; ~1280 cycles, lets SID pot settle (>512)
        BNE DELAY
        LDA $D419           ; POTX -> paddle A position
        STA $FB
        LDA $D41A           ; POTY -> paddle B position
        STA $FC
        LDA $DC01           ; port 1 buttons (bit2=A, bit3=B, 0=pressed)
        STA $FD
        CLI
        RTS
```

For port 2: `LDA #$80` and read buttons from `$DC00`.

**BASIC — disable timer IRQ instead of SEI:**

```basic
10 POKE 56334,PEEK(56334)AND254 : REM stop CIA1 timer A (kills kbd IRQ)
20 POKE 56320,64                : REM select port 1 paddles
30 FOR I=1 TO 5:NEXT            : REM settle delay
40 X=PEEK(54297):Y=PEEK(54298)  : REM POTX, POTY
50 POKE 56334,PEEK(56334)OR1    : REM restart timer
60 PRINT X,Y
```

Use 128 in line 20 for port 2. Keyboard dead while timer stopped — re-enable before needing keys.