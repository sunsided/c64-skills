C64 blank screen, power LED on. Dead reset/init. Most common culprits, check order:

## Most likely (ranked)

1. **PLA (906114-01, U17)** — #1 killer. Generates all chip-select logic. Dead PLA = no ROM/RAM access = blank screen, no border. Runs hot, fails often. Socketed usually. Swap test first.
2. **RAM (4164 DRAM, U9–U24)** — bad RAM in first bank corrupts zero page/stack → CPU can't init. Often **blank screen with NO border** (vs. garbage screen = different fault).
3. **CPU 6510 (U7)** — dead CPU = no bus activity. Blank.
4. **VIC-II (6567/6569, U19)** — no video gen. But VIC dead often gives black screen too.
5. **ROMs** — KERNAL (901227, U4) / BASIC (901226, U3) bad → no boot. Char ROM (901225, U5) bad gives garbage chars not blank.
6. **PLA-adjacent**: 7406/7407 logic, clock (8701 oscillator), bad reset (555 timer / cap C? on reset line).

## Check first (no scope needed)

- **Reseat all socketed chips** — PLA, CPU, VIC, ROMs, SID. Oxidized pins common. Free fix.
- **Reset line** — pin holds low =永 reset. Check pin 40 (RES) on 6510 = should be HIGH (~5V) after power-up.
- **Power rails** — measure +5V and +12V at board. Cassette port: pin C/3 = +5V, no +12V there (that's elsewhere). Bad 5V regulator (7805) → dim/dead.

## Check with multimeter / scope

| Signal | Where | Expect |
|---|---|---|
| +5V | many | 4.9–5.1V steady |
| ø2 clock (1MHz) | 6510 pin 39 | square wave ~1MHz |
| ø0 dot clock (8MHz) | VIC | oscillator running |
| RES | 6510 pin 40 | HIGH after boot |
| AEC/BA | bus | toggling = activity |

## Fast triage

No scope? **Dead Test cartridge** (diagnostic ROM) or known-good chip swaps. Order to swap: **PLA → RAM → CPU → VIC → KERNAL ROM**.

Border present but no text = different class (RAM/char). **Truly black, no border = VIC, PLA, CPU, or clock dead** — points hard at PLA or CPU.

Start: reseat chips + check reset line HIGH + verify +5V. Cheapest, catches majority.