**.prg with standard BASIC autostart stub.** Decode:

**Bytes 0-1: load address** `01 08` → little-endian `$0801`. KERNAL LOAD puts rest of file starting there. $0801 = default BASIC program start on C64.

**Remaining 12 bytes load into $0801–$080C:**

| Addr | Byte(s) | Meaning |
|------|---------|---------|
| $0801 | `0B 08` | link ptr → next line @ `$080B` |
| $0803 | `0A 00` | line number = `$000A` = **10** |
| $0805 | `9E` | BASIC token **SYS** |
| $0806 | `32 30 36 31` | ASCII `"2061"` |
| $080A | `00` | end-of-line |
| $080B | `00 00` | null link = end-of-program |

Detokenized: `10 SYS 2061`

**Machine code starts at $080D.** 2061 decimal = `$080D` = 2048+13. That's byte immediately after the stub ($080C last stub byte). ML code lives there in file (bytes not in your dump — your 14 bytes are just the stub).

**Flow:** RUN → BASIC interpreter hits line 10 → SYS does `JSR $080D` (after pushing regs from $030C-$030F). Execution lands first opcode at $080D.

Why 2061 not lower: stub occupies $0801-$080C, so $080D is first free byte. Compiler/cruncher packs ML right behind stub for tightest layout.

Check it yourself in VICE monitor:
```
d 080d    ; disassemble from entry point
```
Or in BASIC after LOAD: `PRINT PEEK(2061)` shows first ML opcode byte.