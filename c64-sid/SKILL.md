---
name: c64-sid
description: >-
  The MOS 6581 SID sound chip and making sound and music on the Commodore 64 —
  the register map at $D400-$D41C, the three voices, the four waveforms
  (triangle, sawtooth, pulse, noise), the ADSR envelope generator, pulse width,
  the multimode filter, master volume, ring modulation and oscillator sync, and
  the frequency/note tables. Use this skill WHEN asked to "play a note/sound on
  the C64", "program the SID", "what does $D418 do", "set up an ADSR envelope",
  "make a sound effect", "why is my SID silent", or any POKE/STA into $D4xx.
  Pairs with c64-game-ports (SID reads the paddles), c64-memory-map, c64-vic-ii
  and c64-cia (raster/timer-driven music players).
---

# SID 6581 — sound and music

The SID sits at **$D400** (54272). It has 3 independent voices, each with a tone
oscillator (4 selectable waveforms), an ADSR envelope, and a route into one shared
multimode analog filter, plus a master volume. Most registers are **write-only** —
you cannot read back what you POKEd; only $D419-$D41C are readable. Getting sound
out is mostly: set volume, set an envelope, set a frequency, then **gate** the
voice on.

In BASIC people use a base variable `S = 54272` and POKE `S+offset`. In assembly
you `STA $D4xx`. Both are shown below.

## Register map ($D400 + offset)

Voice block repeats at base **+0 (voice 1)**, **+7 (voice 2 → $D407)**,
**+14 (voice 3 → $D40E)**:

| Off | Reg | Name | Contents |
|-----|-----|------|----------|
| +0 | $D400 | FREQ LO | oscillator frequency, low byte |
| +1 | $D401 | FREQ HI | oscillator frequency, high byte |
| +2 | $D402 | PW LO | pulse width, low byte |
| +3 | $D403 | PW HI | pulse width, high nibble (12-bit total) |
| +4 | $D404 | CONTROL | `NOISE PULSE SAW TRI | TEST RING SYNC GATE` (bit7..bit0) |
| +5 | $D405 | ATK/DCY | attack (hi nibble) / decay (lo nibble) |
| +6 | $D406 | SUS/REL | sustain (hi nibble) / release (lo nibble) |

Filter & global (shared by all voices):

| Reg | Name | Contents |
|-----|------|----------|
| $D415 | FC LO | filter cutoff, low 3 bits |
| $D416 | FC HI | filter cutoff, high 8 bits (11-bit cutoff) |
| $D417 | RES/FILT | `RES3-0 | FILTEX FILT3 FILT2 FILT1` — resonance + which voices/ext are filtered |
| $D418 | MODE/VOL | `3OFF HP BP LP | VOL3-0` — filter mode select, voice-3 disconnect, master volume in low nibble |
| $D419 | POTX | paddle X (read-only) — see **c64-game-ports** |
| $D41A | POTY | paddle Y (read-only) |
| $D41B | OSC3 | voice-3 oscillator output / random (read-only) |
| $D41C | ENV3 | voice-3 envelope output (read-only) |

## The control register ($D404 / +4) — bit by bit

| Bit | Val | Name | Effect |
|-----|-----|------|--------|
| 0 | 1 | GATE | 1 = start ATTACK/DECAY/SUSTAIN; 0 = begin RELEASE |
| 1 | 2 | SYNC | hard-sync this oscillator to the previous voice's oscillator |
| 2 | 4 | RING MOD | ring-modulate this voice's **triangle** with the previous voice's osc |
| 3 | 8 | TEST | reset & lock the oscillator (also used to silence noise lock-up) |
| 4 | 16 | TRIANGLE | select triangle waveform (soft, few harmonics) |
| 5 | 32 | SAWTOOTH | select sawtooth (rich, buzzy) |
| 6 | 64 | PULSE | select pulse — duty cycle set by PW LO/HI |
| 7 | 128 | NOISE | select noise (explosions, wind, hi-hats) |

Pick **one** waveform bit + GATE. E.g. sawtooth on = `32+1 = 33`; pulse on = `65`.

## ADSR envelope

`$D405` = attack:decay (one nibble each), `$D406` = sustain:release. Attack/decay/
release are **rates** (0–15), sustain is a **level** (0 = silent … 15 = peak). The
rate→time table (from the chip spec):

| Value | Attack | Decay/Release |
|-------|--------|---------------|
| 0 | 2 ms | 6 ms |
| 2 | 16 ms | 48 ms |
| 5 | 56 ms | 168 ms |
| 9 | 250 ms | 750 ms |
| 11 | 800 ms | 2.4 s |
| 15 | 8 s | 24 s |

(Full 16-row table in `references/sid-chip-spec.md`, Table 2.) **The envelope only
advances while GATE is 1; clearing GATE jumps to RELEASE.** That gate edge is the
single most common reason a SID program is silent or stuck.

## Frequency

Output frequency: **Fout = (Fn × Fclk) / 16777216**, where Fn is the 16-bit value
in FREQ HI:LO and Fclk ≈ 1,022,727 Hz (NTSC) / 985,248 Hz (PAL). You normally don't
compute it — use the note table: `references/music-note-values.md` lists Note#,
note name, decimal Fn, and the HI/LO bytes to POKE. (PAL pitch is ~4% lower for the
same Fn; retune if it matters.)

## Play one note

BASIC:
```basic
10 S=54272
20 FOR L=S TO S+24: POKE L,0: NEXT     : REM clear all SID registers
30 POKE S+24,15                        : REM master volume = 15
40 POKE S+5,9 : POKE S+6,0             : REM attack=0 decay=9, sustain=0 release=0
50 POKE S+1,17: POKE S,37              : REM freq HI=17 LO=37  (a mid note)
60 POKE S+4,33                         : REM sawtooth (32) + gate on (1)
70 FOR T=1 TO 300: NEXT
80 POKE S+4,32                         : REM gate off -> release
```

Assembly:
```asm
        LDA #$0F : STA $D418      ; master volume
        LDA #$09 : STA $D405      ; attack 0 / decay 9
        LDA #$00 : STA $D406      ; sustain 0 / release 0
        LDA #$25 : STA $D400      ; freq lo
        LDA #$11 : STA $D401      ; freq hi
        LDA #$21 : STA $D404      ; sawtooth + GATE on  (%00100001)
        ; ... delay ...
        LDA #$20 : STA $D404      ; GATE off -> release
```

## Filter, ring mod, sync

- **Filter**: set cutoff in `$D415/$D416`, resonance + per-voice routing bits in
  `$D417`, then choose mode in `$D418` (bit4 LP, bit5 BP, bit6 HP — combinable; bit7
  `3OFF` disconnects voice 3 from the output, handy when using voice 3 only as a
  modulation source via OSC3/ENV3). A voice is only filtered if its FILT bit in
  `$D417` is set.
- **Ring modulation**: set RING MOD (bit2) and **triangle** on voice *n*; it is
  modulated by voice *n−1*'s oscillator (voice 1 ← voice 3). Metallic, bell tones.
- **Sync**: set SYNC (bit1) on voice *n* to hard-sync it to voice *n−1*'s
  oscillator. Both effects need the modulating voice's frequency set even if it's
  silent.

## Gotchas

- Silent output? Check: master volume `$D418` low nibble > 0; a waveform bit set;
  GATE toggled on; a non-zero envelope (all-zero ADSR + sustain 0 can be inaudible).
- Registers are write-only — keep your own shadow copy if you need to read state.
- Pulse width only matters with the PULSE waveform selected.
- Don't combine multiple waveform bits casually; mixing **noise** with another
  waveform can lock the noise generator silent until a TEST-bit or RES reset.
- Volume is global — there is no per-voice volume; balance with envelopes/filter.

## References

- **`references/sid-chip-spec.md`** — PRG Appendix O: the authoritative register
  map, every bit's meaning, the full Table 2 envelope rates, filter math, and the
  SID pinout. Read for exact semantics and edge cases.
- **`references/sound-programming.md`** — PRG Ch4: the programmer's walk-through of
  volume, multiple voices, waveforms, the envelope, filtering, and advanced
  sync/ring-mod technique with worked BASIC.
- **`references/sound-tutorial.md`** — User's Guide Ch7: gentle intro and sample
  sound-effect programs.
- **`references/music-note-values.md`** — PRG Appendix E: Note# → note → Fn → HI/LO
  bytes. The lookup table for playing tunes.
- **`references/sound-control-settings.md`** — User's Guide Appendix P: ready-made
  register-setting tables for instrument-like sounds and effects.

Paddle reading via `$D419/$D41A` is documented in **c64-game-ports**. For music
players driven off a raster or CIA-timer interrupt, see **c64-vic-ii** and
**c64-cia**. SID register addresses and banking live in **c64-memory-map**.
