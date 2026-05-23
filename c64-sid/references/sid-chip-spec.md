> Source: c64prg.txt Appendix O, "6581 Sound Interface Device (SID) Chip Specifications". Lightly cleaned from the Project 64 etext.


  6581 SOUND INTERFACE DEVICE (SID)
  CHIP SPECIFICATIONS

  CONCEPT

    The 6581 Sound Interface Device (SID) is a single-chip, 3-voice elec-
  tronic music synthesizer/sound effects generator compatible with the 65XX
  and similar microprocessor families. SID provides wide-range, high-
  resolution control of pitch (frequency), tone color (harmonic content),
  and dynamics (volume). Specialized control circuitry minimizes software
  overhead, facilitating use in arcade/home video games and low-cost
  musical instruments.

  FEATURES

  o 3 TONE OSCILLATORS
        Range: 0-4 kHz
  o 4 WAVEFORMS PER OSCILLATOR
        Triangle, Sawtooth,
        Variable Pulse, Noise
  o 3 AMPLITUDE MODULATORS
        Range: 48 dB
  o 3 ENVELOPE GENERATORS
        Exponential response
        Attack Rate: 2 ms-8 s
        Decay Rate: 6 ms-24 s
        Sustain Level: 0-peak volume
        Release Rate: 6 ms-24 s
  o OSCILLATOR SYNCHRONIZATION
  o RING MODULATION
  o PROGRAMMABLE FILTER
        Cutoff range: 30 Hz-12 kHz
        12 dB/octave Rolloff
        Low pass, Bandpass,
        High pass, Notch outputs
        Variable Resonance

  o MASTER VOLUME CONTROL
  o 2 A/D POT INTERFACES
  o RANDOM NUMBER/MODULATION GENERATOR
  o EXTERNAL AUDIO INPUT

                             PIN CONFIGURATION

                                +----+ +----+
                     CAP1A   1 @|    +-+    |@ 28  Vdd
                                |           |
                     CAP1B   2 @|           |@ 27  AUDIO OUT
                                |           |
                     CAP2A   3 @|           |@ 26  EXT IN
                                |           |
                     CAP2B   4 @|           |@ 25  Vcc
                                |           |
                      /RES   5 @|           |@ 24  POT X
                                |           |
                        02   6 @|           |@ 23  POT Y
                                |           |
                       R/W   7 @|           |@ 22  D7
                                |    6581   |
                       /CS   8 @|    SID    |@ 21  D6
                                |           |
                        A0   9 @|           |@ 20  D5
                                |           |
                        A1  10 @|           |@ 19  D4
                                |           |
                        A2  11 @|           |@ 18  D3
                                |           |
                        A3  12 @|           |@ 17  D2
                                |           |
                        A4  13 @|           |@ 16  D1
                                |           |
                       GND  14 @|           |@ 15  D0
                                +-----------+

                          [THE PICTURE IS MISSING!]

                             6581 BLOCK DIAGRAM

  DESCRIPTION

    The 6581 consists of three synthesizer "voices" which can be used
  independently or in conjunction with each other (or external audio
  sources) to create complex sounds. Each voice consists of a Tone
  Oscillator/Waveform Generator, an Envelope Generator and an Amplitude
  Modulator. The Tone Oscillator controls the pitch of the voice over a
  wide range. The Oscillator produces four waveforms at the selected
  frequency, with the unique harmonic content of each waveform providing
  simple control of tone color. The volume dynamics of the oscillator are
  controlled by the Amplitude Modulator under the direction of the Envelope
  Generator. When triggered, the Envelope Generator creates an amplitude
  envelope with programmable rates of increasing and decreasing volume. In
  addition to the three voices, a programmable Filter is provided for
  generating complex, dynamic tone colors via subtractive synthesis.
    SID allows the microprocessor to read the changing output of the third
  Oscillator and third Envelope Generator. These outputs can be used as a
  source of modulation information for creating vibrato, frequency/filter
  sweeps and similar effects. The third oscillator can also act as a random
  number generator for games. Two A/D converters are provided for inter-
  facing SID with potentiometers. These can be used for "paddles" in a
  game environment or as front panel controls in a music synthesizer. SID
  can process external audio signals, allowing multiple SID chips to be
  daisy-chained or mixed in complex polyphonic systems.

  SID CONTROL REGISTERS

    There are 29 eight-bit registers in SID which control the generation of
  sound. These registers are either WRITE-only or READ-only and are listed
  below in Table 1.

                         Table 1. SID Register Map            WO=WRITE-ONLY
                                                              RO=READ-ONLY
    REG#                      DATA
    (HEX) D7    D6    D5    D4    D3    D2    D1    D0   REG NAME       REG
                                                         Voice 1       TYPE
   0 00   F7    F6    F5    F4    F3    F2    F1    F0   FREQ LO         WO
   1 01   F15   F14   F13   F12   F11   F10   F9    F8   FREQ HI         WO
   2 02   PW7   PW6   PW5   PW4   PW3   PW2   PW1   PW0  PW LO           WO
   3 03    -     -     -     -   PW11  PW10   PW9   PW8  PW HI           WO
   4 04  NOISE PULSE  SAW TRIANG TEST  RING  SYNC  GATE  CONTROL REG     WO
   5 05  ATK3  ATK2  ATK1  ATK0  DCY3  DCY2  DCY1  DCY0  ATTACK/DECAY    WO
   6 06  STN3  STN2  STN1  STN0  RLS3  RLS2  RLS1  RLS0  SUSTAIN/RELEASE WO

                                                         Voice 2
   7 07   F7    F6    F5    F4    F3    F2    F1    F0   FREQ LO         WO
   8 08   F15   F14   F13   F12   F11   F10   F9    F8   FREQ HI         WO
   9 09   PW7   PW6   PW5   PW4   PW3   PW2   PW1   PW0  PW LO           WO
  10 0A    -     -     -     -   PW11  PW10   PW9   PW8  PW HI           WO
  11 0B  NOISE PULSE  SAW TRIANG TEST  RING  SYNC  GATE  CONTROL REG     WO
  12 0C  ATK3  ATK2  ATK1  ATK0  DCY3  DCY2  DCY1  DCY0  ATTACK/DECAY    WO
  13 0D  STN3  STN2  STN1  STN0  RLS3  RLS2  RLS1  RLS0  SUSTAIN/RELEASE WO

                                                         Voice 3
  14 0E   F7    F6    F5    F4    F3    F2    F2    F1   FREQ LO         WO
  15 0F   F15   F14   F13   F12   F11   F10   F9    F8   FREQ HI         WO
  16 10   PW7   PW6   PW5   PW4   PW3   PW2   PW1   PW0  PW LO           WO
  17 11    -     -     -     -   PW11  PW10   PW9   PW8  PW HI           WO
  18 12  NOISE PULSE  SAW TRIANG TEST  RING  SYNC  GATE  CONTROL REG     WO
  19 13  ATK3  ATK2  ATK1  ATK0  DCY3  DCY2  DCY1  DCY0  ATTACK/DECAY    WO
  20 14  STN3  STN2  STN1  STN0  RLS3  RLS2  RLS1  RLS0  SUSTAIN/RELEASE WO

                                                         Filter
  21 15    -     -     -     -     -    FC2   FC1   FC0  FC LO           WO
  22 16  FC10   FC9   FC8   FC7   FC6   FC5   FC4   FC3  FC HI           WO
  23 17  RES3  RES2  RES1  RES0 FILTEX FILT3 FILT2 FILT1 RES/FILT        WO
  24 18  3OFF   HP    BP    LP   VOL3  VOL2  VOL1  VOL0  MODE/VOL        WO

                                                         Misc.
  25 19   PX7   PX6   PX5   PX4   PX3   PX2   PX1   PX0  POT X           RO
  26 1A   PY7   PY6   PY5   PY4   PY3   PY2   PY1   PY0  POT Y           RO
  27 1B   O7    O6    O5    O4    O3    O2    O1    O0   OSC3/RANDOM     RO
  28 1C   E7    E6    E5    E4    E3    E2    E1    E0   ENV3            RO

  SID REGISTER DESCRIPTION

  VOICE 1

  FREQ LO/FREQ HI (Registers 00,01)

    Together these registers form a 16-bit number which linearly controls
  the frequency of Oscillator 1 . The frequency is determined by the
  following equation:

                       Fout = (Fn*Fclk/16777216) Hz

    Where Fn is the 16-bit number in the Frequency registers and Fclk is
  the system clock applied to the 02 input (pin 6). For a standard 1.0-MHz
  clock, the frequency is given by:

                       Fout = (Fn*0.059604645) Hz

    A complete table of values for generating 8 octaves of the equally
  tempered musical scale with concert A (440 Hz) tuning is provided in
  Appendix E. It should be noted that the frequency resolution of SID is
  sufficient for any tuning scale and allows sweeping from note to note
  (portamento) with no discernable frequency steps.

  PW LO/PW HI (Registers 02,03)

    Together these registers form a 12-bit number (bits 4-7 of PW HI are
  not used) which linearly controls the Pulse Width (duty cycle) of the
  Pulse waveform on Oscillator 1. The pulse width is determined by the
  following equation:

                            PWout = (PWn/40.95) %

  Where PWn is the 12-bit number in the Pulse Width registers.
    The pulse width resolution allows the width to be smoothly swept with
  no discernable stepping. Note that the Pulse waveform on Oscillator 1
  must be selected in order for the Pulse Width registers to have any au-
  dible effect. A value of 0 or 4095 ($FF) in the Pulse Width registers
  will produce a constant DC output, while a value of 2048 ($800) will
  produce a square wave.

  CONTROL REGISTER (Register 04)

    This register contains eight control bits which select various options
  on Oscillator 1.
    GATE (Bit 0): The GATE bit controls the Envelope Generator for Voice 1.
  When this bit is set to a one, the Envelope Generator is Gated
  (triggered) and the ATTACK/DECAY/SUSTAIN cycle is initiated. When the bit
  is reset to a zero, the RELEASE cycle begins. The Envelope Generator
  controls the amplitude of Oscillator I appearing at the audio output,
  therefore, the GATE bit must be set (along with suitable envelope pa-
  rameters) for the selected output of Oscillator 1 to be audible. A de-
  tailed discussion of the Envelope Generator can be found at the end of
  this Appendix.
    SYNC (Bit 1): The SYNC bit, when set to a one, synchronizes the
  fundamental frequency of Oscillator 1 with the fundamental frequency of
  Oscillator 3, producing "Hard Sync" effects.
    Varying the frequency of Oscillator 1 with respect to Oscillator 3 pro-
  duces a wide range of complex harmonic structures from Voice I at the
  frequency of Oscillator 3. In order for sync to occur, Oscillator 3 must
  be set to some frequency other than zero but preferably lower than the
  frequency of Oscillator 1. No other parameters of Voice 3 have any effect
  on sync.
    RING MOD (Bit 2): The RING MOD bit, when set to a one, replaces the
  Triangle waveform output of Oscillator 1 with a "Ring Modulated"
  combination of Oscillators 1 and 3. Varying the frequency of Oscillator 1
  with respect to Oscillator 3 produces a wide range of non-harmonic
  overtone structures for creating bell or gong sounds and for special ef-
  fects. In order for ring modulation to be audible, the Triangle waveform
  of Oscillator 1 must be selected and Oscillator 3 must be set to some
  frequency other than zero. No other parameters of Voice 3 have any effect
  on ring modulation.
    TEST (Bit 3): The TEST bit, when set to a one, resets and locks Oscil-
  lator 1 at zero until the TEST bit is cleared. The Noise waveform output
  of Oscillator 1 is also reset and the Pulse waveform output is held at a
  DC level. Normally this bit is used for testing purposes, however, it can
  be used to synchronize Oscillator 1 to external events, allowing the
  generation of highly complex waveforms under real-time software control.

    (Bit 4): When set to a one, the Triangle waveform output of Oscillator
  1 is selected. The Triangle waveform is low in harmonics and has a
  mellow, flute-like quality.
    (Bit 5): When set to a one, the Sawtooth waveform output of Oscillator
  1 is selected. The Sawtooth waveform is rich in even and odd harmonics
  and has a bright, brassy quality.
    (Bit 6): When set to a one, the Pulse waveform output of Oscillator 1
  is selected. The harmonic content of this waveform can be adjusted by the
  Pulse Width registers, producing tone qualities ranging from a bright,
  hollow square wave to a nasal, reedy pulse. Sweeping the pulse width in
  real-time produces a dynamic "phasing" effect which adds a sense of
  motion to the sound. Rapidly jumping between different pulse widths can
  produce interesting harmonic sequences.
    NOISE (Bit 7): When set to a one, the Noise output waveform of
  Oscillator 1 is selected. This output is a random signal which changes at
  the frequency of Oscillator 1. The sound quality can be varied from a low
  rumbling to hissing white noise via the Oscillator 1 Frequency registers.
  Noise is useful in creating explosions, gunshots, jet engines, wind, surf
  and other unpitched sounds, as well as snore drums and cymbals. Sweeping
  the oscillator frequency with Noise selected produces a dramatic rushing
  effect.
    One of the output waveforms must be selected for Oscillator 1 to be
  audible, however, it is NOT necessary to de-select waveforms to silence
  the output of Voice 1. The amplitude of Voice 1 at the final output is a
  function of the Envelope Generator only.

  +-----------------------------------------------------------------------+
  | NOTE: The oscillator output waveforms are NOT additive. If more than  |
  | one output waveform is selected simultaneously, the result will be a  |
  | logical ANDing of the waveforms. Although this technique can be used  |
  | to generate additional waveforms beyond the four listed above, it must|
  | be used with care. If any other waveform is selected while Noise is   |
  | on, the Noise output can "lock up " If this occurs, the Noise output  |
  | will remain silent until reset by the TEST bit or by bringing RES     |
  | (pin 5) low.                                                          |
  +-----------------------------------------------------------------------+

  ATTACK/DECAY (Register 05)

    Bits 4-7 of this register (ATK0-ATK3) select 1 of 16 ATTACK rates for
  the Voice 1 Envelope Generator. The ATTACK rate determines how rapidly
  the output of Voice 1 rises from zero to peak amplitude when the Envelope
  Generator is Gated. The 16 ATTACK rates are listed in Table 2.
    Bits 0-3 (DCY0-DCY3) select 1 of 16 DECAY rates for the Envelope
  Generator. The DECAY cycle follows the ATTACK cycle and the DECAY rate
  determines how rapidly the output fails from the peak amplitude to the
  selected SUSTAIN level. The 16 DECAY rates are listed in Table 2.

  SUSTAIN/RELEASE (Register 06)

    Bits 4-7 of this register (STN0-STN3) select 1 of 16 SUSTAIN levels for
  the Envelope Generator. The SUSTAIN cycle follows the DECAY cycle and the
  output of Voice 1 will remain at the selected SUSTAIN amplitude as long
  as the Gate bit remains set. The SUSTAIN levels range from zero to peak
  amplitude in 16 linear steps, with a SUSTAIN value of 0 selecting zero
  amplitude and a SUSTAIN value of 15 ($F) selecting the peak amplitude. A
  SUSTAIN value of 8 would cause Voice I to SUSTAIN at an amplitude one-
  half the peak amplitude reached by the ATTACK cycle.
    Bits 0-3 (RLS0-RLS3) select 1 of 16 RELEASE rates for the Envelope
  Generator. The RELEASE cycle follows the SUSTAIN cycle when the Gate bit
  is reset to zero. At this time, the output of Voice 1 will fall from the
  SUSTAIN amplitude to zero amplitude at the selected RELEASE rate. The 16
  RELEASE rates are identical to the DECAY rates.

  +-----------------------------------------------------------------------+
  | NOTE: The cycling of the Envelope Generator can be altered at any     |
  | point via the Gate bit. The Envelope Generator can be Gated and       |
  | Released without restriction. For example, if the Gate bit is reset   |
  | before the envelope has finished the ATTACK cycle, the RELEASE cycle  |
  | will immediately begin, starting from whatever amplitude had been     |
  | reached. if the envelope is then Gated again (before the RELEASE cycle|
  | has reached zero amplitude), another ATTACK cycle will begin, starting|
  | from whatever amplitude had been reached. This technique can be used  |
  | to generate complex amplitude envelopes via real-time software        |
  | control.                                                              |
  +-----------------------------------------------------------------------+

                           Table 2. Envelope Rates
  +-----------------+--------------------------+--------------------------+
  |      VALUE      |        ATTACK RATE       |    DECAY/RELEASE RATE    |
  +-----------------+--------------------------+--------------------------+
  |   DEC   (HEX)   |       (Time/Cycle)       |       (Time/Cycle)       |
  +-----------------+--------------------------+--------------------------+
  |     0    (0)    |            2 ms          |            6 ms          |
  |     1    (1)    |            8 ms          |           24 ms          |
  |     2    (2)    |           16 ms          |           48 ms          |
  |     3    (3)    |           24 ms          |           72 ms          |
  |     4    (4)    |           38 ms          |          114 ms          |
  |     5    (5)    |           56 ms          |          168 ms          |
  |     6    (6)    |           68 ms          |          204 ms          |
  |     7    (7)    |           80 ms          |          240 ms          |
  |     8    (8)    |          100 ms          |          300 ms          |
  |     9    (9)    |          250 ms          |          750 ms          |
  |    10    (A)    |          500 ms          |          1.5 s           |
  |    11    (B)    |          800 ms          |          2.4 s           |
  |    12    (C)    |            1 s           |            3 s           |
  |    13    (D)    |            3 s           |            9 s           |
  |    14    (E)    |            5 s           |           15 s           |
  |    15    (F)    |            8 s           |           24 s           |
  +-----------------+--------------------------+--------------------------+

  +-----------------------------------------------------------------------+
  | NOTE: Envelope rates are based on a 1.0-MHz 02 clock. For other 02    |
  | frequencies, multiply the given rate by 1 MHz/02. The rates refer to  |
  | the amount of time per cycle. For example, given an ATTACK value of 2,|
  | the ATTACK cycle would take 16 ms to rise from zero to peak amplitude.|
  | The DECAY/RELEASE rates refer to the amount of time these cycles would|
  | take to fall from peak amplitude to zero.                             |
  +-----------------------------------------------------------------------+

  VOICE 2

    Registers 07-$0D control Voice 2 and are functionally identical to reg-
  isters 00-06 with these exceptions:

    1) When selected, SYNC synchronizes Oscillator 2 with Oscillator 1.
    2) When selected, RING MOD replaces the Triangle output of Oscillator 2
       with the ring modulated combination of Oscillators 2 and 1.

  VOICE 3

    Registers $0E-$14 control Voice 3 and are functionally identical to
  registers 00-06 with these exceptions:

    1) When selected, SYNC synchronizes Oscillator 3 with Oscillator 2.
    2) When selected, RING MOD replaces the Triangle output of Oscillator 3
       with the ring modulated combination of Oscillators 3 and 2.

    Typical operation of a voice consists of selecting the desired parame-
  ters: frequency, waveform, effects (SYNC, RING MOD) and envelope rates,
  then gating the voice whenever the sound is desired. The sound can be
  sustained for any length of time and terminated by clearing the Gate bit.
  Each voice can be used separately, with independent parameters and
  gating, or in unison to create a single, powerful voice. When used in
  unison, a slight detuning of each oscillator or tuning to musical
  intervals creates a rich, animated sound.

  FILTER

  FC LO/FC HI (Registers $15,$16)

    Together these registers form an 11-bit number (bits 3-7 of FC LO are
  not used) which linearly controls the Cutoff (or Center) Frequency of the
  programmable Filter. The approximate Cutoff Frequency ranges from 30
  Hz to 12 KHz.

  RES/FILT (Register $17)

    Bits 4-7 of this register (RES0-RES3) control the resonance of the
  filter. Resonance is a peaking effect which emphasizes frequency com-
  ponents at the Cutoff Frequency of the Filter, causing a sharper sound.
  There are 16 resonance settings ranging linearly from no resonance (0) to
  maximum resonance (15 or $F). Bits 0-3 determine which signals will be
  routed through the Filter:
    FILT 1 (Bit 0): When set to a zero, Voice 1 appears directly at the
  audio output and the Filter has no effect on it. When set to a one, Voice
  1 will be processed through the Filter and the harmonic content of Voice
  1 will be altered according to the selected Filter parameters.
    FILT 2 (Bit 1): Same as bit 0 for Voice 2.
    FILT 3 (Bit 2): Same as bit 0 for Voice 3.
    FILTEX (Bit 3): Same as bit 0 for External audio input (pin 26).

  MODE/VOL (Register $18)

    Bits 4-7 of this register select various Filter mode and output
  options:
    LP (Bit 4): When set to a one, the Low-Pass output of the Filter is
  selected and sent to the audio output. For a given Filter input signal,
  all frequency components below the Filter Cutoff Frequency are passed
  unaltered, while all frequency components above the Cutoff are attenuated
  at a rate of 12 dB/Octave. The Low-Pass mode produces fullbodied sounds.
    BP (Bit 5): Same as bit 4 for the Bandpass output. All frequency
  components above and below the Cutoff are attenuated at a rate of 6
  dB/Octave. The Bandpass mode produces thin, open sounds.
    HP (Bit 6): Same as bit 4 for the High-Pass output. All frequency
  components above the Cutoff are passed unaltered, while all frequency
  components below the Cutoff are attenuated at a rate of 12 dB/Octave.
  The High-Pass mode produces tinny, buzzy sounds.
    3 OFF (Bit 7): When set to a one, the output of Voice 3 is disconnected
  from the direct audio path. Setting Voice 3 to bypass the Filter
  (FILT 3 = 0) and setting 3 OFF to a one prevents Voice 3 from reaching
  the audio output. This allows Voice 3 to be used for modulation purposes
  without any undesirable output.

  +-----------------------------------------------------------------------+
  | NOTE: The Filter output modes ARE additive and multiple Filter modes  |
  | may be selected simultaneously. For example, both LP and HP modes can |
  | be selected to produce a Notch (or Band Reject) Filter response. In   |
  | order for the Filter to have any audible effect, at least one Filter  |
  | output must be selected and at least one Voice must be routed through |
  | the Filter. The Filter is, perhaps, the most important element in SID |
  | as it allows the generation of complex tone colors via subtractive    |
  | synthesis (the Filter is used to eliminate specific frequency         |
  | components from a harmonically rich input signal). The best results   |
  | are achieved by varying the Cutoff Frequency in real-time.            |
  +-----------------------------------------------------------------------+

    Bits 0-3 (VOL0-VOL3) select 1 of 16 overall Volume levels for the final
  composite audio output. The output volume levels range from no output (0)
  to maximum volume (15 or $F) in 16 linear steps. This control can be used
  as a static volume control for balancing levels in multi-chip systems or
  for creating dynamic volume effects, such as Tremolo. Some Volume level
  other than zero must be selected in order for SID to produce any sound.

  MISCELLANEOUS

  POTX (Register $19)

    This register allows the microprocessor to read the position of the
  potentiometer tied to POTX (pin 24), with values ranging from 0 at
  minimum resistance, to 255 ($FF) at maximum resistance. The value is
  always valid and is updated every 512 (02 clock cycles. See the Pin
  Description section for information on pot and capacitor values.

  POTY (Register $1A)

    Same as POTX for the pot tied to POTY (pin 23).

  OSC 3/RANDOM (Register $1B)

    This register allows the microprocessor to read the upper 8 output bits
  of Oscillator 3. The character of the numbers generated is directly re-
  lated to the waveform selected. If the Sawtooth waveform of Oscillator 3
  is selected, this register will present a series of numbers incrementing
  from 0 to 255 ($FF) at a rate determined by the frequency of Oscillator
  3. If the Triangle waveform is selected, the output will increment from 0
  up to 255, then decrement down to 0. If the Pulse waveform is selected,
  the output will jump between 0 and 255. Selecting the Noise waveform
  will produce a series of random numbers, therefore, this register can be
  used as a random number generator for games. There are numerous timing
  and sequencing applications for the OSC 3 register, however, the chief
  function is probably that of a modulation generator. The numbers
  generated by this register can be added, via software, to the Oscillator
  or Filter Frequency registers or the Pulse Width registers in real-time.
  Many dynamic effects can be generated in this manner. Siren-like sounds
  can be created by adding the OSC 3 Sawtooth output to the frequency
  control of another oscillator. Synthesizer "Sample and Hold" effects can
  be produced by adding the OSC 3 Noise output to the Filter Frequency
  control registers. Vibrato can be produced by setting Oscillator 3 to a
  frequency around 7 Hz and adding the OSC 3 Triangle output (with proper
  scaling) to the Frequency control of another oscillator. An unlimited
  range of effects are available by altering the frequency of Oscillator 3
  and scaling the OSC 3 output. Normally, when Oscillator 3 is used for
  modulation, the audio output of Voice 3 should be eliminated (3 OFF = 1).

  ENV 3 (Register $1C)

    Same as OSC 3, but this register allows the microprocessor to read the
  output of the Voice 3 Envelope Generator. This output can be added to the
  Filter Frequency to produce harmonic envelopes, WAH-WAH, and similar
  effects. "Phaser" sounds can be created by adding this output to the
  frequency control registers of an oscillator. The Voice 3 Envelope
  Generator must be Gated in order to produce any output from this regis-
  ter. The OSC 3 register, however, always reflects the changing output of
  the oscillator and is not affected in any way by the Envelope Generator.

  SID PIN DESCRIPTION

  CAP1A,CAP1B, (Pins 1,2)/ CAP2A,CAP2B (Pins 3,4)

    These pins are used to connect the two integrating capacitors required
  by the programmable Filter. C1 connects between pins 1 and 2, C2 between
  pins 3 and 4. Both capacitors should be the some value. Normal operation
  of the Filter over the audio range (approximately 30 Hz-12 kHz) is
  accomplished with a value of 2200 pF for C1 and C2. Polystyrene
  capacitors are preferred and in complex polyphonic systems, where many
  SID chips must track each other, matched capacitors are recommended.
    The frequency range of the Filter can be tailored to specific applica-
  tions by the choice of capacitor values. For example, a low-cost game may
  not require full high-frequency response. In this case, larger values
  for C1 and C2 could be chosen to provide more control over the bass
  frequencies of the Filter. The maximum Cutoff Frequency of the Filter is
  given by:

                             FCmax = 2.6E-5/C

  Where C is the capacitor value. The range of the Filter extends 9 octaves
  below the maximum Cutoff Frequency.

  RES (Pin 5)

    This TTL-level input is the reset control for SID. When brought low for
  at least ten 02 cycles, all internal registers are reset to zero and the
  audio output is silenced. This pin is normally connected to the reset
  line of the microprocessor or a power-on-clear circuit.

  02 (Pin 6)

    This TTL-Level input is the master clock for SID. All oscillator
  frequencies and envelope rates are referenced to this clock. 02 also
  controls data transfers between SID and the microprocessor. Data can only
  be transferred when (02 is high. Essentially, (02 acts as a high-active
  chip select as far as data transfers are concerned. This pin is normally
  connected to the system clock, with a nominal operating frequency of 1.0
  MHz.

  R/W  (Pin 7)

    This TTL-level input controls the direction of data transfers between
  SID and the microprocessor. If the chip select conditions have been met,
  a high on this line allows the microprocessor to Read data from the
  selected SID register and a low allows the microprocessor to Write data
  into the selected SID register. This pin is normally connected to the
  system Read/Write line.

  CS (Pin 8)

    This TTL-Level input is a low active chip select which controls data
  transfers between SID and the microprocessor. CS must be low for any
  transfer. A Read from the selected SID register can only occur if CS is
  low, 02 is high and R/W is high. A Write to the selected SID register can
  only occur if CS is low, (02 is high and R/W is low. This pin is normally
  connected to address decoding circuitry, allowing SID to reside in the
  memory map of a system.

  A0-A4 (Pins 9-13)

    These TTL-Level inputs are used to select one of the 29 SID registers.
  Although enough addresses are provided to select 1 of 32 registers, the
  remaining three register locations are not used. A Write to any of these
  three locations is ignored and a Read returns invalid data. These pins
  are normally connected to the corresponding address lines of the micro-
  processor so that SID may be addressed in the same manner as memory.

  GND (Pin 14)

    For best results, the ground line between SID and the power supply
  should be separate from ground lines to other digital circuitry. This
  will minimize digital noise at the audio output.

  D0-D7 (Pins 15-22)

    These bidirectional lines are used to transfer data between SID and the
  microprocessor. They are TTL compatible in the input mode and capable of
  driving 2 TTL loads in the output mode. The data buffers are usually in
  the high-impedance off state. During a Write operation, the data buffers
  remain in the off (input) state and the microprocessor supplies data to
  SID over these lines. During a Read operation, the data buffers turn on
  and SID supplies data to the microprocessor over these lines. The pins
  are normally connected to the corresponding data lines of the micro-
  processor.

  POTX,POTY (Pins 24,23)

    These pins are inputs to the A/D converters used to digitize the posi-
  tion of potentiometers. The conversion process is based on the time con-
  stant of a capacitor tied from the POT pin to ground, charged by a
  potentiometer tied from the POT pin to +5 volts. The component values are
  determined by:

                                RC = 4.7E-4

  Where R is the maximum resistance of the pot and C is the capacitor.
    The larger the capacitor, the smaller the POT value jitter. The recom-
  mended values for R and C are 470 komhs and 1000 pF. Note that a separate
  pot and cap are required for each POT pin.

  VCC (Pin 25)

    As with the GND line, a separate +5 VDC line should be run between SID
  Vcc and the power supply in order to minimize noise. A bypass capacitor
  should be located close to the pin.

  EXT IN (Pin 26)

    This analog input allows external audio signals to be mixed with the
  audio output of SID or processed through the Filter. Typical sources in-
  clude voice, guitar, and organ. The input impedance of this pin is on the
  order of 100 kohms. Any signal applied directly to the pin should ride at
  a DC level of 6 volts and should not exceed 3 volts p-p. In order to pre-

  vent any interference caused by DC level differences, external signals
  should be AC-coupled to EXT IN by an electrolytic capacitor in the 1-10
  uF range. As the direct audio path (FILTEX=0) has unity gain, EXT IN can
  be used to mix outputs of many SID chips by daisy-chaining. The number of
  chips that can be chained in this manner is determined by the amount of
  noise and distortion allowable at the final output. Note that the output
  Volume control will affect not only the three SID voices, but also any
  external inputs.

  AUDIO OUT (Pin 27)

    This open-source buffer is the final audio output of SID, comprised of
  the three SID voices, the Filter and any external input. The output level
  is set by the output Volume control and reaches a maximum of 2 volts p-p
  at a DC level of 6 volts. A source resistor from AUDIO OUT to ground is
  required for proper operation. The recommended resistance is 1 kohm for
  a standard output impedance.
    As the output of SID rides at a 6-volt DC level, it should be AC-
  coupled to any audio amplifier with an electrolytic capacitor in the 1-10
  uF range.

  VDD (Pin 28)

    As with Vcc, a separate +12 VDC line should be run to SID VDD and a
  bypass capacitor should be used.

  6581 SID CHARACTERISTICS

  ABSOLUTE MAXIMUM RATINGS

  +--------------------------+------------+-----------------+-------------+
  |          RATING          |   SYMBOL   |      VALUE      |    UNITS    |
  +--------------------------+------------+-----------------+-------------+
  |  Supply Voltage          |    VDD     |   -0.3 to +17   |     VDC     |
  |  Supply Voltage          |    VCC     |   -0.3 to +7    |     VDC     |
  |  Input Voltage (analog)  |    Vina    |   -0.3 to +17   |     VDC     |
  |  Input Voltage (digital) |    Vind    |   -0.3 to +7    |     VDC     |
  |  Operating Temperature   |    Ta      |      0 to +70   |   Celsius   |
  |  Storage Temperature     |    Tstg    |   -55 to +150   |   Celsius   |
  +--------------------------+------------+-----------------+-------------+

   ELECTRICAL CHARACTERISTICS (Vdd=12 VDC+-5%, Vcc=5 VDC+-5%,
     Ta=0 to 70 Celsius)

  +------------------------------------------+----+-----+---+-------+-----+
  |             CHARACTERISTIC               SYMBOL MIN |TYP|  MAX  |UNITS|
  +------------------------------------------+----+-----+---+-------+-----+
  | Input High Voltage (RES, 02, RIN, CS,    | Vih|  2  | - |  Vcc  | VDC |
  | Input Low Voltage  A0-A4, D0-D7)         | Vil|-0.3 | - |  0.8  | VDC |
  +------------------------------------------+----+-----+---+-------+-----+
  | Input Leakage Current (RES, 02, R/W, CS, | Iin|  -  | - |  2.5  |  uA |
  |                       A0-A4; Vin=0-5 VDC)|    |     |   |       |     |
  | Three-State (Off)     (D0-D7; Vcc=max)   |Itsi|  -  | - |  10   |  uA |
  +------------------------------------------+----+-----+---+-------+-----+
  | Input Leakage Current Vin=0.4-2.4 VDC    |    |     |   |       |     |
  +------------------------------------------+----+-----+---+-------+-----+
  | Output High Voltage   (D0-D7; Vcc=min,   | Voh| 2.4 | - |Vcc-0.7| VDC |
  |                       I load=200 uA)     |    |     |   |       |     |
  +------------------------------------------+----+-----+---+-------+-----+
  | Output Low Voltage    (D0-D7; Vcc=max,   | Vol| GND | - |  0.4  | VDC |
  |                       I load=3.2 mA)     |    |     |   |       |     |
  +------------------------------------------+----+-----+---+-------+-----+
  | Output High Current   (D0-D7; Sourcing,  | Ioh| 200 | - |   -   |  uA |
  |                       Voh=2.4 VDC)       |    |     |   |       |     |
  +------------------------------------------+----+-----+---+-------+-----+
  | Output Low Current    (D0-D7; Sinking,   | Iol| 3.2 | - |   -   |  mA |
  |                       Vol=0.4 VDC)       |    |     |   |       |     |
  +------------------------------------------+----+-----+---+-------+-----+
  | Input Capacitance     (RES, 02, R/W, CS, | Cin|  -  | - |  10   |  pF |
  |                       A0-A4, D0-D7)      |    |     |   |       |     |
  +------------------------------------------+----+-----+---+-------+-----+
  | Pot Trigger Voltage   (POTX, POTY)       |Vpot|  -  Vcc/2   -   | VDC |
  +------------------------------------------+----+-----+---+-------+-----+
  | Pot Sink Current      (POTX, POTY)       |Ipot| 500 | - |   -   |  uA |
  +------------------------------------------+----+-----+---+-------+-----+
  | Input Impedance       (EXT IN)           | Rin| 100 |150|   -   |kohms|
  +------------------------------------------+----+-----+---+-------+-----+
  | Audio Input Voltage   (EXT IN)           | Vin| 5.7 | 6 |  6.3  | VDC |
  |                                          |    |  -  |0.5|   3   | VAC |

  +------------------------------------------+----+-----+---+-------+-----+
  | Audio Output Voltage  (AUDIO OUT; 1 kohm |    |     |   |       |     |
  |                       load, volume=max)  |Vout| 5.7 | 6 |  6.3  | VDC |
  |                       One Voice on:      |    | 0.4 |0.5|  0.6  | VAC |
  |                       All Voices on:     |    | 1.0 |1.5|  2.0  | VAC |
  +------------------------------------------+----+-----+---+-------+-----+
  | Power Supply Current  (VDD)              | Idd|  -  | 20|   25  |  mA |
  +------------------------------------------+----+-----+---+-------+-----+
  | Power Supply Current  (VCC)              | Icc|  -  | 70|  100  |  mA |
  +------------------------------------------+----+-----+---+-------+-----+
  | Power Dissipation     (Total)            | Pd |  -  |600| 1000  |  mW |
  +------------------------------------------+----+-----+---+-------+-----+

  6581 SID TIMING

                          [THE PICTURE IS MISSING!]

  READ CYCLE

  +----------+----------------------------+-------+-------+-------+-------+
  |  SYMBOL  |           NAME             |  MIN  |  TYP  |  MAX  | UNITS |
  +----------+----------------------------+-------+-------+-------+-------+
  |   Tcyc   |   Clock Cycle Time         |    1  |   -   |    20 |   uA  |
  |   Tc     |   Clock High Pulse Width   |  450  |  500  |10,000 |   ns  |
  |   Tr,Tf  |   Clock Rise/Fall Time     |   -   |   -   |    25 |   ns  |
  |   Trs    |   Read Set-Up Time         |    0  |   -   |   -   |   ns  |
  |   Trh    |   Read Hold Time           |    0  |   -   |   -   |   ns  |
  |   Tacc   |   Access Time              |   -   |   -   |   300 |   ns  |
  |   Tah    |   Address Hold Time        |   10  |   -   |   -   |   ns  |
  |   Tch    |   Chip Select Hold Time    |    0  |   -   |   -   |   ns  |
  |   Tdh    |   Data Hold Time           |   20  |   -   |   -   |   ns  |
  +----------+----------------------------+-------+-------+-------+-------+

                          [THE PICTURE IS MISSING!]

  WRITE CYCLE

  +----------+----------------------------+-------+-------+-------+-------+
  |  SYMBOL  |           NAME             |  MIN  |  TYP  |  MAX  | UNITS |
  +----------+----------------------------+-------+-------+-------+-------+
  |   Tw     |   Write Pulse Width        |  300  |   -   |   -   |   ns  |
  |   Twh    |   Write Hold Time          |    0  |   -   |   -   |   ns  |
  |   Taws   |   Address Set-up Time      |    0  |   -   |   -   |   ns  |
  |   Tah    |   Address Hold Time        |   10  |   -   |   -   |   ns  |
  |   Tch    |   Chip Select Hold Time    |    0  |   -   |   -   |   ns  |
  |   Tvd    |   Valid Data               |   80  |   -   |   -   |   ns  |
  |   Tdh    |   Data Hold Time           |   10  |   -   |   -   |   ns  |
  +----------+----------------------------+-------+-------+-------+-------+

  EQUAL-TEMPERED MUSICAL SCALE VALUES

    The table in Appendix E lists the numerical values which must be stored
  in the SID Oscillator frequency control registers to produce the notes of
  the equal-tempered musical scale. The equal-tempered scale consists of an
  octave containing 12 semitones (notes): C,D,E,F,G,A,B and C#,D#,F#,G#,A#.
  The frequency of each semitone is exactly the 12th root of 2 times the
  frequency of the previous semitone. The table is based on a (02 clock of
  1.02 MHz. Refer to the equation given in the Register Description for use
  of other master clock frequencies. The scale selected is concert pitch,
  in which A-4 = 440 Hz. Transpositions of this scale and scales other than
  the equal-tempered scale are also possible.
    Although the table in Appendix E provides a simple and quick method for
  generating the equal-tempered scale, it is very memory inefficient as it
  requires 192 bytes for the table alone. Memory efficiency can be improved
  by determining the note value algorithmically. Using the fact that each
  note in an octave is exactly half the frequency of that note in the next
  octave, the note look-up table can be reduced from 96 entries to 12
  entries, as there are 12 notes per octave. If the 12 entries (24 bytes)
  consist of the 16-bit values for the eighth octave (C-7 through B-7),
  then notes in lower octaves can be derived by choosing the appropriate
  note in the eighth octave and dividing the 16-bit value by two for each
  octave of difference. As division by two is nothing more than a right-
  shift of the value, the calculation can easily be accomplished by a
  simple software routine. Although note B-7 is beyond the range of the
  oscillators, this value should still be included in the table for
  calculation purposes (the MSB of B-7 would require a special software
  case, such as generating this bit in the CARRY before shifting). Each
  note must be specified in a form which indicates which of the 12
  semitones is desired, and which of the eight octaves the semitone is in.
  Since four bits are necessary to select 1 of 12 semitones and three bits
  are necessary to select 1 of 8 octaves, the information can fit in one
  byte, with the lower nybble selecting the semitone (by addressing the
  look-up table) and the upper nybble being used by the division routine to
  determine how many times the table value must be right-shifted.

  SID ENVELOPE GENERATORS

    The four-part ADSR (ATTACK, DECAY, SUSTAIN, RELEASE) envelope generator
  has been proven in electronic music to provide the optimum trade-off
  between flexibility and ease of amplitude control. Appropriate selection
  of envelope parameters allows the simulation of a wide range 2: of
  percussion and sustained instruments. The violin is a good example of a
  sustained instrument. The violinist controls the volume by bowing the
  instrument. Typically, the volume builds slowly, reaches a peak, then
  drops to an intermediate level. The violinist can maintain this level for
  as long as desired, then the volume is allowed to slowly die away. A
  "snapshot" of this envelope is shown below:

      PEAK AMPLITUDE ---      +  <- SUSTAIN  ->
                             / \     PERIOD
                           A/  D\      S         R
                           /     +------------+
                          /       INTERMEDIATE +
                         /            LEVEL      +
      ZERO AMPLITUDE ---+                           +--

    This volume envelope can be easily reproduced by the ADSR as shown
  below, with typical envelope rates:
                                                +
                                               / \
                                              /   +--------+
  ATTACK:  10 ($A)     500 ms                /              +
  DECAY:    8          300 ms             --+ A  D     S     R +-
  SUSTAIN: 10 ($A)
  RELEASE:  9          750 ms
                                        GATE+--------------+
                                          --+              +-----

    Note that the tone can be held at the intermediate SUSTAIN level for
  as long as desired. The tone will not begin to die away until GATE is
  cleared. With minor alterations, this basic envelope can be used for
  brass and woodwinds as well as strings.
    An entirely different form of envelope is produced by percussion in-
  struments such as drums, cymbals and gongs, as well as certain
  keyboards such as pianos and harpsichords. The percussion envelope is
  characterized by a nearly instantaneous attack, immediately followed by
  a decay to zero volume. Percussion instruments cannot be sustained at

  a constant amplitude. For example, the instant a drum is struck, the
  sound reaches full volume and decays rapidly regardless of how it was
  struck. A typical cymbal envelope is shown below:

  ATTACK:   0       2 ms                        +
  DECAY:    9     750 ms                        |+
  SUSTAIN:  0                                   |  +
  RELEASE:  9     750 ms                    ----+     +--
                                               A    D
    Note that the tone immediately begins to decay to zero amplitude after
  the peak is reached, regardless of when GATE is cleared. The amplitude
  envelope of pianos and harpsichords is somewhat more complicated, but can
  be generated quite easily with the ADSR. These instruments reach full
  volume when a key is first struck. The amplitude immediately begins to
  die away slowly as long as the key remains depressed. If the key is
  released before the sound has fully died away, the amplitude will
  immediately drop to zero. This envelope is shown below:

  ATTACK:   0       2 ms                        +
  DECAY:    9     750 ms                        |+
  SUSTAIN:  0                                   |  +
  RELEASE:  0       6 ms                    ----+  +-----
                                               A  D R
    Note that the tone decays slowly until GATE is cleared, at which point
  the amplitude drops rapidly to zero.
    The most simple envelope is that of the organ, When a key is pressed,
  the tone immediately reaches full volume and remains there. When the key
  is released, the tone drops immediately to zero volume. This envelope is
  shown below:
                                                +----+
  ATTACK:   0       2 ms                        |    |
  DECAY:    0       6 ms                        |    |
  SUSTAIN: 15 ($F)                              |    |
  RELEASE:  0       6 ms                    ----+    +---
                                               A   S  R
    The real power of SID lies in the ability to create original sounds
  rather than simulations of acoustic instruments. The ADSR is capable of
  creating envelopes which do not correspond to any "real" instruments. A
  good example would be the "backwards" envelope. This envelope is
  characterized by a slow attack and rapid decay which sounds very much

  like an instrument that has been recorded on tape then played backwards.
  This envelope is shown below:                        S
                                                  +----------+
  ATTACK: 10 ($A) 500 ms                       A /           | R
  DECAY:   0        6 ms                        /            +
  SUSTAIN: 15 ($F)                             /              +
  RELEASE:  3      72 ms                    --+                 +--

    Many unique sounds can be created by applying the amplitude envelope of
  one instrument to the harmonic structure of another. This produces sounds
  similar to familiar acoustic instruments, yet notably different. In
  general, sound is quite subjective and experimentation with various
  envelope rates and harmonic contents will be necessary in order to
  achieve the desired sound.

                          [THE PICTURE IS MISSING!]

                        TYPICAL 6581/SID APPLICATION

