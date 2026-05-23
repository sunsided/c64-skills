> Source: C64ServiceManual.txt, "64 TROUBLESHOOTING GUIDE". Lightly cleaned from the Project 64 etext (page-break tildes and running footers removed; the SYMPTOM / POSSIBLE SOLUTION table is verbatim). Chip designators (U1, U7, etc.) refer to board positions — see `board-identification.md` for the parts lists that map each Un to its part.

# 64 TROUBLESHOOTING GUIDE

| SYMPTOM | POSSIBLE SOLUTION |
|---------|-------------------|
| Blank screen on power up. | Check External Power Supply; U4 (KERNAL ROM), U17 (PLA); U7 (6510 MPU), U3 (ROM); U8 (7406 IC), U19 (VIC II); U9-U12 (4164 RAM), U21-U24 (4164 RAM); BT2, CR4, VR1 |
| Out of memory error on power up. | Check U9-U12 (4164 RAM); U21-U24 (4164 RAM); **** USE DIAGNOSTIC TEST - DISK |
| No cursor displayed. | Check U1, U15, U7 |
| Intermittent blank screen. | Check U2, U7 |
| Powers up with graphics display and blinking cursor. | Check U14 (74LS258 IC) |
| Powers up with all the characters displayed as blocks. | Check U26 (74LS373 IC) |
| Intermittent display. | Check C88 (Possible Bad Connection) |
| Powers up with the 'PRESS PLAY ON TAPE' message and the display blanks. | Check U7 (6510 MPU); R1 (Possible Bad Connection) |
| On power up the cursor lock up. | Check U7 (6510 MPU); U20 (556 IC) |
| When 'RETURN' is pressed after a run command, the cursor goes back to home position. | Check U3 (ROM) |
| Poke command does not work. | Check U3 (ROM) |
| Joystick does not operate correctly. | Check U1, U28 (6526 CIA) |
| Wrong frequency. | Check C70 |
| No character lettering is displayed on the screen. | Check U3 (ROM); U2 (CIA) |
| Graphic characters instead of letters displayed. | Check U19 (VIC II) |
| Power up message appears but no cursor | Check U1, U15, U7 and U4 |
| Cursor jumps to back to home position. | Check U7 (6510 MPU) |
| Abnormal colors appear in the letters. | Check U6 (2114 RAM); U16 (4066 IC) |
| Different characters are displayed and cursor is locked when turned on and off. | Check RAM |
| System does not reset and the 'RESTORE' key does not work. | Check U20 (556 IC) |
| White band scrolls down the screen. (60 HZ HUM) | Check External Power Supply; VR2 (5V Regulator) |
| Cursor disappears after the system warms up. | Check U1 (6526 CIA) |
| SYNTAX ERROR displayed after system warms up. | Check RAM, U3 (ROM) |
| Wavy screen after the system warms up. | Check External power supply; U31 (74LS629 IC); U30 (74LS193 IC) |
| The system resets when it warms up. | Check U7 (6510 MPU); U3 (ROM) |
| Keyboard does not operate correctly when the system warms up. | Check U1 (6526 CIA); U3 (ROM) |
| Black band scrolls through screen when the system warms up. | Check External Power Supply; C90, C88, CR4; VR2 (5V Regulator) |
| Cassette motor keeps running. | Check U7 (6510 MPU) |
| Cassette motor keeps running even after a program is done loading. The TIP 29 transistor gets extremely hot and the fuse may possibly blow. | Check Cassette Port for Shorts; R4 (Possibly Open) |
| The cursor disappears when the cassette is plugged in. | Check U7 (6510 MPU) |
| Cassette runs extremely slow. The program seems to load but will not run | Check U7 (6510 MPU) |
| When loading from cassette, the 'SYNTAX ERROR' message is displayed. | Check U20 (556 IC) |
| DEVICE NOT PRESENT ERROR is displayed when disk is used. | Check U1 (6526 CIA); U7 (6510 MPU); R28, R29, R30 |
| Disk drives continue to search when trying to load. | Check U2 (6526 CIA) |
| When loading from disk and any key of the 4th row of the keyboard is pressed, the cursor goes to home position. | Check U20 (556 IC); R35 (Possible Bad Connection) |
| When loading from disk, a 'FILE NOT FOUND' message is displayed. | Check U4 (ROM); U2 (6526 CIA) |
| OUT OF MEMORY is displayed when disk is used. | Check U20 (556 IC) |
