**Bad Line condition** (from Bauer's VIC-II doc):

A Bad Line Condition exists at the negative edge of ø0 at start of a cycle when **all three** hold:

1. `RASTER >= $30` AND `RASTER <= $F7` (raster in 48–247)
2. `(RASTER & 7) == YSCROLL` (low 3 bits of raster equal YSCROLL)
3. DEN bit was set at some point during raster line `$30` (48)

**Registers:**
- RASTER = `$D012` (53266), bit 8 in `$D011` bit 7
- YSCROLL = `$D011` low 3 bits (`$D011 & 7`)
- DEN (Display Enable) = `$D011` bit 4 (`%00010000`), value $10

`$D011` (53265) bit layout:
```
bit 7: RASTER bit 8
bit 6: ECM
bit 5: BMM
bit 4: DEN
bit 3: RSEL
bit 2-0: YSCROLL
```

Default `$D011` after boot = `$1B` = `%00011011` → DEN=1, YSCROLL=3. So default first bad line = raster `$33` (51), then every 8 lines while DEN held during line $30.

**Why DEN-at-line-$30 matters:** if DEN=0 during entire line $30, NO bad lines occur that whole frame (screen blank, but sprites/border still work). DEN must be set during line $30 to "arm" bad lines for the frame.

**Effect:** On a Bad Line, VIC asserts BA low, steals cycles 12–54 from CPU (~40+ cycles) to fetch video matrix + color data (c-access). CPU halted those cycles.

Use case — open top/bottom border or stable raster: write YSCROLL via `$D011` to shift when bad line hits, or clear DEN to suppress bad lines.