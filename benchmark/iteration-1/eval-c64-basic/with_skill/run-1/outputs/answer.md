Program:

```basic
10 INPUT "WHAT IS YOUR NAME";N$
20 FOR I=1 TO 5
30 PRINT "HELLO ";N$
40 NEXT I
```

Notes:
- `INPUT "...";N$` print prompt + `?`, wait RETURN. `N$` hold name.
- `FOR I=1 TO 5 ... NEXT I` loop 5 times. `STEP` default 1.
- `;` in PRINT join "HELLO " and `N$` no gap. Trailing space inside quotes give space before name.
- Type `NEW` first if old program in memory. `RUN` to start.