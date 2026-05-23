Bad Line condition. Three parts must all hold, tested at negative edge of Φ0 starting a cycle:

1. **Raster in range:** `$30 ≤ RASTER ≤ $F7` (line 48–247)
2. **YSCROLL match:** `(RASTER & 7) == YSCROLL` — low 3 bits of raster equal `$D011` bits 2–0
3. **DEN was set:** display-enable bit (`$D011` bit 4) set at some point during raster line `$30` (48)

All three true → Bad Line. VIC pulls BA low, stalls 6510 ~40–43 cycles to fetch 40 char pointers.

Notes:
- YSCROLL=0 (default) → first Bad Line = line `$30`, then every 8th line.
- Clear DEN (`$D011` bit 4 = 0) before/at line $30 → suppresses **all** Bad Lines for frame.
- Writing YSCROLL mid-line moves/suppresses next Bad Line → basis of FLD/FLI.