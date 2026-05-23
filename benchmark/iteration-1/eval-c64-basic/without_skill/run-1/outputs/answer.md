Program:

```basic
10 INPUT "WHAT IS YOUR NAME";N$
20 FOR I=1 TO 5
30 PRINT "HELLO ";N$
40 NEXT I
```

Notes:
- `INPUT "...";N$` — prompt prints with trailing `?`. C64 adds `? ` auto.
- `N$` string var. `;` after prompt required.
- `FOR I=1 TO 5 ... NEXT I` loops 5 times.
- `PRINT "HELLO ";N$` — space inside quotes so output `HELLO MARKUS` not `HELLOMARKUS`.

Run: type `RUN`, Enter.