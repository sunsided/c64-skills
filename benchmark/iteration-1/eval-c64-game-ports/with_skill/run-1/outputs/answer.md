Port 2 = location **56320** ($DC00, CIA1 Port A). Low 5 bits, active LOW (0 = pressed):

- bit 0 = up, bit 1 = down, bit 2 = left, bit 3 = right, bit 4 = fire.

```basic
10 JV=PEEK(56320)
20 FR=(JV AND 16)=0
30 D=15-(JV AND 15)
40 PRINT CHR$(147);
50 IF (D AND 1) THEN PRINT "UP ";
60 IF (D AND 2) THEN PRINT "DOWN ";
70 IF (D AND 4) THEN PRINT "LEFT ";
80 IF (D AND 8) THEN PRINT "RIGHT ";
90 IF D=0 THEN PRINT "CENTER ";
100 IF FR THEN PRINT "FIRE";
110 GOTO 10
```

How it works:
- `JV AND 16` isolates fire bit. =0 means pressed (active low).
- `15-(JV AND 15)` flips low 4 bits so 1=up,2=down,4=left,8=right. Diagonals combine (up+right = 1+8 = 9).
- Line 40 clears screen each loop so prints stay put.

Port 1 instead = **56321** ($DC01) — but port 1 has keyboard-scan crosstalk, so single-stick games use port 2.