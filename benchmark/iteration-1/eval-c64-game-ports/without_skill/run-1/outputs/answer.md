Port 2 = `56320` ($DC00), CIA#1 Data Port A. Bits **active LOW** (0 = pushed):

| Bit | Value | Direction |
|-----|-------|-----------|
| 0 | 1 | Up |
| 1 | 2 | Down |
| 2 | 4 | Left |
| 3 | 8 | Right |
| 4 | 16 | Fire |

Read with `PEEK(56320)`. Test each bit: `(J AND value)=0` means pushed.

```basic
10 J=PEEK(56320)
20 IF (J AND 1)=0 THEN PRINT "UP"
30 IF (J AND 2)=0 THEN PRINT "DOWN"
40 IF (J AND 4)=0 THEN PRINT "LEFT"
50 IF (J AND 8)=0 THEN PRINT "RIGHT"
60 IF (J AND 16)=0 THEN PRINT "FIRE"
70 GOTO 10
```

Notes:
- Port 1 = `56321` ($DC01), same bit layout. Port 1 shares lines with keyboard scan — port 2 cleaner.
- Diagonals = two bits low together (up+left etc).
- Idle (nothing pushed) = `PEEK` returns 127 (`$7F`), all direction/fire bits high.