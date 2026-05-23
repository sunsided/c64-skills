---
name: c64-basic
description: >-
  Commodore 64 BASIC V2: programming rules, the three data types (integer,
  floating-point, string) and their constants/variables/arrays, expressions,
  arithmetic/relational/logical operators and precedence, string handling,
  INPUT/GET, program crunching, and the full alphabetical reference of every
  BASIC keyword (commands, statements, functions, operators) with abbreviations.
  Use this skill WHEN reading, writing, or debugging C64 BASIC, or asked things
  like "what does FOR/NEXT do", "how do I DIM an array", "what's the abbreviation
  for PRINT", "why do I get ?REDIM'D ARRAY", "operator precedence in BASIC", or
  "is GET blocking". Pairs with c64-petscii (CHR$/screen codes), c64-keyboard
  (keys & editor), c64-memory-map (POKE/PEEK targets), and c64-assembly (SYS/USR).
---

# Commodore 64 BASIC V2

C64 BASIC V2 (Microsoft-derived, in the $A000–$BFFF ROM) has a compact keyword
set — commands, statements, and functions (plus a few operators). Lines
are tokenized on entry; abbreviations and spaces vanish at tokenize time. The
logical screen line is 80 characters (2 physical 40-column rows) — that's the
hard limit on an editable program line. Two modes: **DIRECT** (no line number,
runs on RETURN) and **PROGRAM** (numbered lines). Always `NEW` before keying a
fresh program.

## Data types

Three constant/variable/array types. Type is declared by a suffix on the name:

| Type | Suffix | Range / form | Stored as |
|------|--------|--------------|-----------|
| Floating-point | *(none)* | ±2.93873588E-39 … ±1.70141183E+38, 9 digits shown | 5 bytes |
| Integer | `%` | -32768 … +32767, whole numbers only | 2 bytes |
| String | `$` | 0–255 chars; `""` is the null string | 3 bytes + 1/char |

- Arithmetic is always done in floating point; integers are converted in and the
  result converted back if assigned to a `%` name.
- Numeric constants take **no commas** (`32000`, never `32,000`) — a comma gives
  `?SYNTAX ERROR`. Scientific notation: `3E3` = 3·10³ = 3000.
- A string can hold anything except `"` — use `CHR$(34)` to embed a quote.

### Variable names — the 2-character trap
Names may be any length but **only the first two characters are significant**.
`COUNT` and `COUNTER` are the *same* variable. The first char must be a letter;
`%`/`$` may only be the last char. A name must not be, or contain, a keyword
(e.g. `FORK` contains `FOR`) → `?SYNTAX ERROR`.

### Arrays
`DIM A(n)` makes elements `0..n` (so `n+1` elements). Referencing an
undimensioned array auto-DIMs it to 10 (subscripts 0–10); a later explicit `DIM`
then gives `?REDIM'D ARRAY`. Out-of-range subscript → `?BAD SUBSCRIPT`. Max 255
dimensions, ≤32767 per dimension (memory-limited in practice). Element bytes:
2 (int), 5 (float), 3 + chars (string).

## Operators and precedence

Highest to lowest (Table 1-3). Equal precedence evaluates left→right; relational
operators have no precedence among themselves.

| Prec | Operators | Notes |
|------|-----------|-------|
| 1 | `^` | exponentiation (`3^-2` = 1/9) |
| 2 | `-` (unary) | negation |
| 3 | `*` `/` | |
| 4 | `+` `-` | `+` also concatenates strings |
| 5 | `>` `=` `<` `<=` `>=` `<>` | relational; true = **-1**, false = **0** |
| 6 | `NOT` | bitwise/logical complement (one operand, on its right) |
| 7 | `AND` | |
| 8 | `OR` | |

- Relational/logical results are integers: **true is -1, false is 0**. So
  `A = (X>5)` sets A to -1 or 0, and conditions can be done arithmetically.
- `AND`/`OR`/`NOT` operate bit-by-bit on integers (−32768…32767). `A=96 AND 32`
  → 32; `A=64 OR 32` → 96; `NOT 96` → -97 (two's complement).
- **XOR has no operator** — it only exists inside the `WAIT` statement.
- Strings compare by PETSCII code, left to right; shorter string sorts lower
  when all else equal; leading/trailing blanks count.

## Keyword categories

Abbreviation = type enough letters to be unambiguous, last one **SHIFTed**.
`PRINT` abbreviates to `?`.

**Commands (mostly direct mode):** `CONT` `LIST` `LOAD` `NEW` `RUN` `SAVE`
`VERIFY` `CLR`.
**Statements:** `CLOSE` `CMD` `DATA` `DEF` `DIM` `END` `FOR`…`TO`…`STEP`…`NEXT`
`GET` `GET#` `GOSUB` `GOTO` `IF`…`THEN` `INPUT` `INPUT#` `LET` `ON` `OPEN` `POKE`
`PRINT` `PRINT#` `READ` `REM` `RESTORE` `RETURN` `STOP` `SYS` `WAIT`.
**Numeric functions:** `ABS` `ATN` `COS` `EXP` `FRE` `INT` `LEN` `LOG` `PEEK`
`POS` `RND` `SGN` `SIN` `SQR` `TAN` `USR` `VAL` `ASC` `STATUS`(`ST`) `TIME`(`TI`).
**String functions:** `CHR$` `LEFT$` `MID$` `RIGHT$` `STR$` `TIME$`(`TI$`).
**Special:** `SPC(` `TAB(` `FN`.
**Operators:** `AND` `OR` `NOT`.

Common abbreviations: `?`=PRINT, `G`+SHIFT`O`=GOTO, `GO`+SHIFT`S`=GOSUB,
`P`+SHIFT`O`=POKE, `P`+SHIFT`E`=PEEK, `N`+SHIFT`E`=NEXT, `F`+SHIFT`O`=FOR. Full
list in `references/abbreviations.md`. Abbreviations save **no memory** (all
keywords tokenize to one byte) and LIST back in full form.

## INPUT vs GET

- `INPUT A$` / `INPUT A` prompts and waits for RETURN; only works in PROGRAM
  mode (direct use → `?ILLEGAL DIRECT`). Numeric `INPUT` fed text → `?REDO FROM
  START`; extra commas → `?EXTRA IGNORED`. Limited to ~80 chars (one logical line).
- `GET A$` reads one key from the 10-char keyboard buffer and returns
  *immediately* — empty string if no key. It does **not** block. Idiomatic wait:
  ```basic
  10 GET A$: IF A$="" THEN 10
  ```
- Read the raw key matrix value with `PEEK(197)` (64 = no key). Stuff the buffer
  via locations 631–640 + count at 198.

## Crunching (making programs smaller/faster)
- Renumber to low line numbers — `GOTO 1` is cheaper than `GOTO 100` (line refs
  store digits as bytes).
- Pack statements with `:` up to 80 chars; drop all spaces; remove `REM`s.
- Replace repeated literals with a 1–2 char variable (`V=54296:POKEV,15`).
- Use `?` and other abbreviations to fit a line during entry (re-LIST inflates
  them; don't edit an over-80-char line afterward — excess is lost).

## Gotchas
- Two-char variable significance silently aliases names — pick distinct first 2.
- **String garbage collection** can freeze the machine for seconds when free
  string space fills (BASIC V2's GC is O(n²)); `FRE(0)` triggers it. Reuse string
  vars and minimize churn in tight loops.
- Integer **arrays** save space (2 bytes vs 5) but integer *scalars* are slower
  (converted to float for every operation) — use `%` for big arrays, not loop vars.
- `DEF FN` must be executed before the function is used → `?UNDEF'D FUNCTION`.
- An undimensioned array first touched in a loop auto-DIMs to 10 → later `DIM`
  errors with `?REDIM'D ARRAY`.
- Largest result before `?OVERFLOW` is 1.70141183E+38; underflow silently → 0.

## Worked one-liners
- "Wait for any key": `10 GET K$:IF K$="" THEN 10`
- "Random integer 1–6": `R=INT(RND(1)*6)+1`
- "Is it numeric?": `?VAL("12A")` → 12 (stops at first non-numeric).
- "Embed a quote in a string": `?CHR$(34)"HI"CHR$(34)`
- "Call machine code at $C000": `SYS 49152`

## How to read the references
- **`references/basic-rules.md`** — PRG Ch1 verbatim: constants/variables/arrays,
  expressions, all operators with truth tables, the precedence table, string
  ops, data conversion, INPUT/GET tutorials, and the full crunching section.
  Read for the authoritative wording and worked examples.
- **`references/keyword-reference.md`** — PRG Ch2 verbatim: Table 2-1 (keyword /
  abbreviation / function type) plus the alphabetical "Description of BASIC
  Keywords" with TYPE, FORMAT, Action, and EXAMPLES for every keyword A–WAIT.
  This is the file to open for the exact syntax/behavior of any one keyword.
- **`references/abbreviations.md`** — PRG App A: the complete keyword→keystroke
  abbreviation table (and on-screen appearance). Read when typing fast or
  decoding an abbreviated listing.
- **`references/converting-basic.md`** — PRG App J: porting other-dialect BASIC
  (string DIM, `A$(I,J)` substrings, `B=C=0`, backslash separators, MAT).
- **`references/error-messages.md`** — PRG App K: every BASIC error message and
  its cause. Read this to diagnose a runtime/syntax error.

## Cross-links
- Character codes used by `CHR$`/`ASC`/`PRINT`, and POKE-to-screen codes →
  **c64-petscii**.
- The physical keys and the screen editor's quote/insert modes → **c64-keyboard**.
- What addresses `POKE`/`PEEK` actually hit (VIC/SID/CIA, RAM banking) →
  **c64-memory-map**.
- Writing the machine code that `SYS`/`USR` calls → **c64-assembly**.
