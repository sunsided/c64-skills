Paddle read C64. Three parts:

## 1. Select which pair → CIA1 Port A ($DC00 / 56320), top two bits

SID got only one POTX/POTY pair. Two ports × two pots each = 4 paddles, but multiplexer connect only one port pair at time. Pick via **top 2 bits of CIA1 PRA $DC00**:

- Write `$40` (64) → connect **control port 1** paddles
- Write `$80` (128) → connect **control port 2** paddles

Write to PRA, wait briefly for RC line settle, then read SID pots.

## 2. SID registers return position

| Register | Addr | Value |
|----------|------|-------|
| POTX | 54297 / **$D419** | paddle X position 0–255 |
| POTY | 54298 / **$D41A** | paddle Y position 0–255 |

Fire buttons appear on joystick bits: **bit 2 = pot-X button, bit 3 = pot-Y button**.

## 3. Why awkward alongside keyboard

CIA1 PRA serve double duty: top 2 bits do paddle-port select, **lower bits drive keyboard-scan columns**. Writing select value clobbers keyboard scan; keyboard scan clobbers select. Plus pot read is **RC-timed analog** — need settle delay after switching mux, too tight for BASIC PEEK loop. So BASIC PEEK alone give garbage. SYS short ML routine, disable IRQ during read (stop keyboard scan IRQ touching $DC00), settle, read $D419/$D41A.

## Runnable read (assembly, port 1 = $40)

```asm
rdpdl   sei             ; stop keyboard-scan IRQ touching $DC00
        lda #$40        ; $40 = port 1 paddles ($80 = port 2)
        sta $dc00       ; set mux select on CIA1 PRA
        ldx #$80        ; settle delay for RC line
wait    dex
        bne wait
        lda $d419       ; POTX -> paddle X (0-255)
        sta padx
        lda $d41a       ; POTY -> paddle Y (0-255)
        sta pady
        lda #$ff        ; restore keyboard scan columns
        sta $dc00
        cli
        rts
padx    .byte 0
pady    .byte 0
```

BASIC caller: `SYS` routine, then `PX=PEEK(padx):PY=PEEK(pady)`. PRG manual ship this as `pdlrd` DATA-statement loader — full four-paddle version (both ports) in `references/game-ports.md`.

Fire test after read: `(PEEK(56320) AND 4)=0` → pot-X button pressed; `AND 8` → pot-Y button.