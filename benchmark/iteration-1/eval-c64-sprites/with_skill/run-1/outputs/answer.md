Sprite 0. Red = color code **2**. X=160 < 256 so no $D010 MSB needed.

```basic
10 V=53248                     : REM VIC BASE $D000
20 POKE 2040,13                : REM SPRITE 0 POINTER -> 13*64 = 832
30 FOR I=0 TO 62:READ A:POKE 832+I,A:NEXT : REM 63 SHAPE BYTES
40 POKE V+21,1                 : REM $D015 ENABLE SPRITE 0 (BIT 0)
50 POKE V+39,2                 : REM $D027 SPRITE 0 COLOR = RED (2)
60 POKE V,160:POKE V+1,100     : REM X=160 ($D000), Y=100 ($D001)
70 POKE V+16,0                 : REM $D010 CLEAR X MSB (X<256)
80 DATA 255,255,255,255,255,255,255,255,255
90 DATA 255,255,255,255,255,255,255,255,255
100 DATA 255,255,255,255,255,255,255,255,255
110 DATA 255,255,255,255,255,255,255,255,255
120 DATA 255,255,255,255,255,255,255,255,255
130 DATA 255,255,255,255,255,255,255,255,255
140 DATA 255,255,255,255,255,255,255,255,255
```

Key points:
- **Pointer 2040** ($07F8) = sprite 0 pointer, end of default $0400 screen. Value 13 → data at 13×64 = **832** ($0340, cassette buffer, safe in bank 0).
- **Enable** $D015 (V+21), bit 0.
- **Color** $D027 (V+39) = 2 (red).
- **Position** $D000/$D001 (V/V+1). X=160 fits in one byte.

63 DATA bytes here = solid block. Swap for own shape.