---
name: c64-keyboard
description: >-
  The Commodore 64 keyboard and screen editor: every special key and exactly
  what it does — the Commodore (C=) key, CTRL, RUN/STOP, RESTORE, SHIFT /
  SHIFT-LOCK, CLR/HOME, INST/DEL, the cursor (CRSR) keys, function keys f1–f8,
  RETURN — plus screen-editor behavior (quote mode, insert mode, full-screen
  line editing, the 10-key keyboard buffer). Use this skill WHEN asked "what
  does the C= key do", "how do I switch to lower case", "what is RUN/STOP +
  RESTORE", "how do I clear the screen", "what's quote mode", "how do I type a
  cursor-down into a string", "reset the C64", or about the f-keys. Pairs with
  c64-petscii (the codes these keys emit) and c64-cia (the NMI/RESTORE mechanism).
---

# The Commodore 64 Keyboard & Screen Editor

The C64 keyboard is an 8×8 switch matrix scanned by the KERNAL via CIA #1
($DC00 columns / $DC01 rows). Keystrokes queue in a **10-character buffer**
(type-ahead) and are decoded into a PETSCII value placed at location **197
($C5)** — `PEEK(197)` returns the matrix code of the key held now (64 = none).
The buffer itself is at 631–640 with its count at 198; you can stuff keys there.

## Special keys — what each does

| Key | Effect |
|-----|--------|
| **RETURN** | Enters the current logical (up to 80-char) line; the editor reads & tokenizes it. |
| **SHIFT** | Upper case in lower/upper mode; the right-front graphic in upper/graphics mode; the shifted function (f2/f4/f6/f8) on the function keys. |
| **SHIFT LOCK** | Mechanical latch holding SHIFT down. |
| **`C=` (Commodore)** | See below — charset toggle (with SHIFT) and second color set (with number keys), and the left-front graphic (with a graphic key). |
| **CTRL** | Held with a number key 1–8 sets text color; with 9/0 turns ReVerSe on/off; held during LIST slows the listing. Emits the PETSCII color/RVS control codes. |
| **RUN/STOP** | Interrupts (breaks) a running BASIC program → `BREAK`. With **SHIFT**+RUN/STOP: LOAD+RUN first program from tape. |
| **RUN/STOP + RESTORE** | Warm reset: clears screen, restores default I/O & screen state, **leaves the BASIC program intact**. (RESTORE drives the CPU NMI line.) |
| **RESTORE** | On its own does little; held-down RUN/STOP makes the NMI restore the machine to its normal state. |
| **CLR/HOME** | HOME = cursor to top-left (no erase). **SHIFT**+CLR/HOME = clear screen + home. |
| **INST/DEL** | DEL = backspace, delete char to the left, close the gap. **SHIFT**+INST/DEL = INSerT a space at the cursor. |
| **CRSR ↑↓** / **CRSR ←→** | Two cursor keys: unshifted move down / right, **SHIFT**ed move up / left. Auto-repeat while held. |
| **f1–f8** | Four physical keys; f1/f3/f5/f7 unshifted, f2/f4/f6/f8 shifted. Not bound by default — read them via GET/CHR$(133..140) and act on them. |

### "What does the `C=` key do?" (the common question)
The Commodore key has three jobs:
1. **`C=` + `SHIFT`** toggles the two character sets — upper-case/graphics ↔
   upper/lower case. (Same as `POKE 53272,21` / `POKE 53272,23` from BASIC.)
2. **`C=` + a number key (1–8)** selects the *second* set of 8 text colors
   (CTRL + number gives the first 8).
3. **`C=` + a graphics key** prints the graphic on the **left** front of that
   key (SHIFT prints the right-front graphic).

### Resetting the machine
- **Warm reset, keep program:** hold RUN/STOP, press RESTORE.
- **Cold reset (wipes program/data):** `SYS 64759`.

## Charset / color quick recipes
```basic
POKE 53272,23 : REM switch to lower/upper case set (set 2)
POKE 53272,21 : REM switch back to upper case/graphics (set 1)
PRINT CHR$(28) : REM red text (CTRL+3 equivalent)   -- color CHR$ codes -> c64-petscii
```

## The screen editor

Full-screen, line-oriented editor over an 80-char logical line (two 40-col
physical rows). LIST a line, move the cursor anywhere on it, change it, press
RETURN — the **whole logical line is re-read**, so you don't retype it. Change
just the line number and RETURN to duplicate a line. Editing a line longer than
80 chars loses the overflow (the editor reads only two physical rows) — the same
reason INPUT is capped near 80 chars.

### Quote mode
Entered automatically when the cursor is to the right of an **odd number of `"`**.
In quote mode the cursor/color control keys no longer move the cursor; instead
they insert a **reversed glyph** standing for that control code, so you can embed
cursor-positioning and color changes inside a string literal. Those codes then
*execute* when the string is PRINTed.
- `DEL` is the only control NOT trapped by quote mode.
- Cancel quote mode with RETURN, or RUN/STOP + RESTORE.

```basic
10 PRINT"A{CRSR R}{CRSR R}B"   : REM the {CRSR R} are reversed glyphs typed in quote mode
```

### Insert mode
`SHIFT`+`INST/DEL` opens space and enters INSERT mode until the opened space is
filled. In insert mode, control keys also show as reversed glyphs — but here
`INST` inserts real spaces and `DEL` makes a reversed `T`, which lets you put DEL
characters into a PRINT string (impossible in quote mode). Cancel with RETURN,
SHIFT+RETURN, RUN/STOP+RESTORE, or by filling the inserted spaces.

## The keyboard buffer (type-ahead)
Up to 10 keystrokes queue while the machine is busy; an 11th+ is dropped. Because
a queued RETURN commits everything before it, flush stray input before a prompt:
```basic
10 GET JUNK$: IF JUNK$<>"" THEN 10 : REM empty the keyboard buffer
```

## How to read the references
- **`references/keyboard-and-editor.md`** — PRG Ch2 verbatim: the keyboard
  buffer, the 8×8 matrix and how the KERNAL scans it (CIA #1 $DC00/$DC01,
  location 197), POKEing the buffer (631–640 / 198), and the full Screen Editor
  section — quote mode, insert mode, the Table 2-2 cursor-control glyphs, and the
  printable special characters. Read for the authoritative editor behavior.
- **`references/keyboard-tutorial.md`** — User's Guide verbatim: a friendly
  walk-through of each key (RETURN, SHIFT, CRSR, INST/DEL, CLR/HOME, RESTORE,
  CTRL, RUN/STOP, the `C=` key, function keys), the CTRL-for-color intro, and the
  "back to normal" reset tips (RUN/STOP+RESTORE, `SYS 64759`). Read for plain
  per-key explanations.

## Cross-links
- The actual PETSCII codes these keys emit (cursor, color, RVS, f-key CHR$
  values) and the screen/POKE codes → **c64-petscii**.
- The NMI line that RESTORE pulls, and CIA #1's role in scanning the matrix →
  **c64-cia**.
