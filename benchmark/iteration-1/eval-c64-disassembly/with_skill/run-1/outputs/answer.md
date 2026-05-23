**File = BASIC stub launcher (.prg).** Standard `10 SYS 2061` autostart.

Byte breakdown:

```
01 08            load address $0801 (2049) → BASIC start. Stripped, not data.
-- rest loads at $0801 in memory --
0B 08            link: next line @ $080B
0A 00            line number = 10
9E               SYS token
32 30 36 31      PETSCII "2061"   (digits, not binary)
00               end-of-line
00 00            next link = $0000 → end of program
```

Decodes to:

```basic
10 SYS 2061
```

**Machine code entry = 2061 = $080D.**

Why $080D: stub fills $0801–$080C (12 bytes). Code sits right after, $080D. 2061 is the classic "code immediately follows one-line stub" target (vs 2064/$0810 when 3 pad bytes used).

Next step: disassemble from $080D. First op is byte at file offset 14 (0-indexed: 2 header + 12 stub). Your dump stops at 14 bytes — `00 00 00` at end is the program terminator + start of whatever follows; need more bytes to read the actual code. Send bytes from offset 14 onward and I decode.