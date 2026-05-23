> Source: c64ug.txt Chapter 7, "Creating Sound" (User's Guide). Lightly cleaned from the Project 64 etext.


7.1. Using Sound if You're Not a Computer Programmer

  Most programmers use computer sound for two purposes:  making music and
generating  sound  effects.  Before  getting  into  the  "intricacies" of
programming sound, let's take a quick look at how a typical sound program
is structured  ...  and give you a short sound program you can experiment
with.

7.2. Structure of a Sound Program

  To begin with,  there are five settings  which you should know in order
to generate sound on your COMMODORE 64:  VOLUME,  ATTACK/DECAY,  SUSTAIN/
RELEASE  (ADSR),  WAVEFORM CONTROL and HIGH FREQUENCY/LOW FREQUENCY.  The
first  three  settings  are  usually  set  ONCE  at the beginning of your
program.  The  high  and low frequency settings must be set for EACH NOTE
you play. The waveform control starts and stops each note.

7.3. Sample Sound Program

  Before you start you have to choose a VOICE.  There are 3 voices.  Each
voice requires different sound setting numbers for Waveform, etc. You can
play  1, 2 or 3  voices together but our sample uses only VOICE NUMBER 1.
Type  in  this program line by line  ...  be sure to hit the <RETURN> key
after each line:

  5 FORL=54272TO54296:POKEL,0:NEXT First clear sound chip.
 10 POKE 54296,15  <-------------- Set VOLUME at highest setting.
 20 POKE 54277,190 <-------------- Set  ATTACK/DECAY  rates to define how
                                   fast  a  note  rises to and falls from
                                   its peak volume level (0 to 255).
 30 POKE 54278,248 <-------------- Set SUSTAIN/RELEASE to define level to
                                   prolong note and rate to release it.
 40 POKE 54273,17 : POKE 54272,37  Find  the not/tone you want to play in
                                   the TABLE OF MUSICAL NOTES in Appendix
                                   M  and  enter  the  HIGH-FREQUENCY and
                                   LOW-FREQUENCY  values  for  that  note
                                   (each note requires 2 POKEs).
 50 POKE 54276,17  <-------------- Start  WAVEFORM with one of 4 standard
                                   settings (17, 33, 65 or 129).
 60 FOR T = 1 TO 250 : NEXT  <---- Enter a time loop  to set the DURATION
                                   of  the  note  to be played (a quarter
                                   note  is  approx. "250"  but  may vary
                                   since  a longer program can effect the
                                   timing).
 70 POKE 54276,16  <-------------- Turn off note.

  To hear the note you just created,  type the word RUN  and then hit the
<RETURN> key. To view the program type the word LIST and hit <RETURN>. To
change it, retype the lines you want to alter.

7.4. Making Music on Your Commodore 64

  You  don't  have to be a musician to make a music on your COMMODORE 64!
All  you  need  to know are a few simple numbers which tell your computer
how loud to set the volume,  which notes to play,  how long to play them,
etc. But first ... here's a program which gives you a quick demonstration
of  the  COMMODORE 64's incredible music capabilities,  using only ONE of
your computer's 3 separate voices.
  Type the word NEW and hit <RETURN> to erase your previous program, then
enter this program, type the word RUN and hit the <RETURN> key.

   5 REM MUSICAL SCALE  <---------- Title of program.
   7 FORL=54272TO54296:POKEL,0:NEXT Clear sound chip.
  10 POKE 54296,15  <-------------- Sets volume at highest setting (15).
  20 POKE 54277,9  <--------------- Sets Attack/Decay level (each note).
  30 POKE 54276,17  <-------------- Determines waveform (type of sound).
  40 FOR T = 1 TO 300 : NEXT  <---- Duration (how long) each note plays.
  50 READ A  <--------------------- Reads first number in line 110 DATA.
  60 READ B  <--------------------- Reads second number in line 110 DATA.
  70 IF B = -1 THEN END  <--------- ENDs when it READs -1 in line 900.
  80 POKE 54273, A : POKE 54272, B  POKEs  the  first number from DATA in
                                    line  110  (A=17)  as  HIGH FREQUENCY
                                    and  second  number   (B=37)  as  LOW
                                    FREQUENCY.  Next  time  program loops
                                    around it READs A as 19  and B as 63,
                                    and  so  on,  and POKEs these numbers
                                    into   the  HIGH  and  LOW  FREQUENCY
                                    locations.  The  number  54273 = HIGH
                                    FREQUENCY for VOICE 1 and 54272 = LOW
                                    FREQUENCY for VOICE 1.
  85 POKE 54276, 17  <------------- Start note.
  90 FORT=1TO250:NEXT:POKE54276,16  Let it play then stop note.
  95 FOR T = 1 TO 50 : NEXT  <----- Time for release.
 100 GOTO 20  <-------------------- Loops back to reset CONTROL  and play
                                    new note.
 110 DATA 17,37,19,63,21,154,22,227 Musical  note  values from note value
 120 DATA25,177,28,214,32,94,34,175 chart  in  Appendix M.  Each  pair of
                                    numbers  represents  one  note.   For
                                    example,  17 and 37  represent "C" of
                                    the 4th octave,  19 and 63  represent
                                    "D" and so on.
 900 DATA -1,-1  <----------------- When program reaches -1  it turns off
                                    HIGH/LOW FREQUENCY settings  and ENDs
                                    as instructed in line 70.

  To change the sound to a "harpsichord", change line 85 to read 54276,33
and line 90 to read FOR T=1 TO 250:NEXT:POKE 54276,32 and RUN the program
again.  (To change the line,  hit the <RUN/STOP> key to stop the program,
type word LIST and hit <RETURN>, then retype the program line you want to
change; the new line will automatically replace the old one). What we did
here  is change the "waveform" from a "triangular" shaped sound wave to a
"sawtooth"  wave.  Changing the WAVEFORM can drastically change the sound
produced by the COMMODORE 64  ... but ... waveform is only one of several
settings  you  can  change  to  make  different  musical  tones and sound
effects!  You can also change the ATTACK/DECAY rate of each note  ... for
example, to change from a "harpsichord" sound to a more "banjo" sound try
changing lines 20 and 30 to read:

  20 POKE 54277,3
  30 POKE 54278,0  <--------------- Sets no sustain for banjo effect.

  As  you've  just  seen,  you  can  make  your  COMMODORE 64  sound like
different musical instruments. Let's take a closer look at how each sound
setting works.

7.5. Important Sound Settings

  1. VOLUME.  --  To  turn on the volume and set it to the highest level,
type:  POKE 54296,15.  The  volume setting ranges from 0 to 15 but you'll
use 15 most of the time. To turn "off" the volume, type:

   POKE 54296,0

   You only have to set the volume ONCE at the beginning of your program,
since  the same setting activates all three of the Commodore 64's VOICES.
(Changing  the  volume  during a musical note or sound effect can produce
interesting results but is beyond the scope of this introduction.)

  2. ADSR  and  WAVEFORM  CONTROL  SETTINGS.  --  You've already seen how
changing  the  waveform  can  change the sound effect from "xylophone" to
"harpsichord". Each VOICE has its own WAVEFORM CONTROL SETTING which lets
you define four different types of waveforms:  Triangle,  Sawtooth, Pulse
(Square)  and  Noise.  The CONTROL also activates the COMMODORE 64's ADSR
feature, but we'll come back to this in a moment. A sample waveform start
setting looks like this:

  POKE 54276,17

where the first number (54276) represents the control setting for VOICE 1
and  the  second  number  (17)  represents  the  start  for  a triangular
waveform.  The settings for each VOICE and WAVEFORM combination are shown
in the table below.

                   ADSR AND WAVEFORM CONTROL SETTINGS

              CONTROL               Note Start/Stop Numbers
              REGISTER   TRIANGLE     SAWTOOTH     PULSE       NOISE
 +-----------+---------+-----------+-----------+-----------+-----------+
 |  VOICE 1  |  54276  |   17/16   |   33/32   |   65/64   |  129/128  |
 +-----------+---------+-----------+-----------+-----------+-----------+
 |  VOICE 2  |  54283  |   17/16   |   33/32   |   65/64   |  129/128  |
 +-----------+---------+-----------+-----------+-----------+-----------+
 |  VOICE 3  |  54290  |   17/16   |   33/32   |   65/64   |  129/128  |
 +-----------+---------+-----------+-----------+-----------+-----------+

  Although  the  control  registers  are  different  for  each  voice the
waveform settings are the same for each type of waveform. To see how this
works,  look  at  lines  85 and 90 in the musical scale program.  In this
program,  immediately after setting the frequency in line 80,  we set the
CONTROL SETTING for VOICE 1 in line 85  by POKEing 54276,17.  This turned
on  the  CONTROL  for  VOICE 1 and set it to a TRIANGLE WAVEFORM (17). In
line  70  we  POKE 54276,16,  stopping  the note.  Later,  we changed the
waveform  start  setting  from 17 to 33 to create a SAWTOOTH WAVEFORM and
this gave the scale a "harpsichord" effect.  See  how the CONTROL SETTING
and  WAVEFORM  interact?  Setting  the waveform is similar to setting the
volume,  except  each  voice  has its own stetting and instead of POKEing
volume  levels  we're  defining  waveforms.  Next,  we'll look at another
aspect of sound ... the ADSR feature.

  3. ATTACK/DECAY SETTING.  --  As we mentioned before,  the ADSR CONTROL
SETTING not only defines the waveform but it also activates the ADSR,  or
ATTACK/DECAY/SUSTAIN/RELEASE feature of the COMMODORE 64.  We'll begin by
looking  at  the  ATTACK/DECAY  setting.  The  following  chart shows the
various  ATTACK  and DECAY levels for each voice.  If you're not familiar
with the concepts of sound attack and decay,  you might think of "attack"
as the rate at which a note/sound arises to its MAXIMUM VOLUME. The DECAY
is  the  rate at which the note/sound falls from its highest volume level
back  to  the  SUSTAIN level.  The following chart shows the ATTACK/DECAY
setting  for  each  voice,  and  the  numbers  for  each attack and decay
setting.  Note  that YOU MUST COMBINE ATTACK AND DECAY SETTINGS BY ADDING
THEN UP AND ENTERING THE TOTAL.  For  example,  you can set a HIGH ATTACK
rate  and  a  LOW DECAY rate by adding the high attack number (64) to the
low  decay  number (1).  The total (65) will tell the computer to set the
high  attack  rate  and  low decay rate. You can also increase the attack
rates by adding them together (128+64+32+16=MAX. ATTACK RATE of 240).

                       ATTACK/DECAY RATE SETTINGS

    ATTACK/DECAY     HIGH  MEDIUM  LOW   LOWEST  HIGH MEDIUM LOW  LOWEST
   CONTROL  SETTING ATTACK ATTACK ATTACK ATTACK DECAY DECAY DECAY DECAY
 +---------+-------+------+------+------+------+-----+-----+-----+-----+
 | VOICE 1 | 54277 |  128 |  64  |  32  |  16  |  8  |  4  |  2  |  1  |
 +---------+-------+------+------+------+------+-----+-----+-----+-----+
 | VOICE 2 | 54284 |  128 |  64  |  32  |  16  |  8  |  4  |  2  |  1  |
 +---------+-------+------+------+------+------+-----+-----+-----+-----+
 | VOICE 3 | 54291 |  128 |  64  |  32  |  16  |  8  |  4  |  2  |  1  |
 +---------+-------+------+------+------+------+-----+-----+-----+-----+

  If  you  set  an attack rate with no decay,  the decay is automatically
zero, and vice-versa.  For example, if you POKE 54277,64 you set a medium
attack rate with zero decay for VOICE 1.  If you POKE 54277, 66 you set a
medium  attack  rate  and a low decay rate (because 66=64+2 and sets BOTH
settings).  You  can also add up several attack values,  or several decay
values.  For  example,  you can add a low attack (32) and a medium attack
(64)  for a combined attack rate of 96,  then add a medium decay of 4 and
... presto ... POKE 54277,100.
  At this point, a sample program will better illustrate the effect. Type
the word NEW, hit <RETURN> and type in this program and RUN it:

   5 FOR L=54272 TO 54296:POKE L,0:NEXT  Clear sound chip.
  10 PRINT "HIT ANY KEY"  <------------- Screen message
  20 POKE 54296,15  <------------------- Set VOLUME at highest level.
  30 POKE 54277,64  <------------------- Set Attack/Decay.
  50 POKE 54273,17 : POKE 54272,37  <--- POKE one note into VOICE 1.
  60 GET K$ : IF K$ = "" THEN 60  <----- Check the keyboard.
  70 POKE 54276,17: FOR T=1 TO 200: NEXT Set waveform control (triangle).
  80 POKE 54276,16: FOR T=1 TO 50: NEXT  Turn off settings.
  90 GOTO 20  <------------------------- Loop back and do it again.

  Here,  we're  using  VOICE 1  to create one note at a time  ...  with a
MEDIUM ATTACK RATE  and  ZERO DECAY.  The  key  is  line 30.  POKEing the
ATTACK/DECAY  setting  with the number 64 activates a MEDIUM attack rate.
The  result  sounds like someone bouncing a ball in an oil drum.  Now for
the fun part.  Hit the <RUN/STOP> key to stop the program,  then type the
word LIST and hit <RETURN>.  Now type this line and hit <RETURN> (the new
line 30 automatically replaces the old line 30):

  30 POKE 54277,190

  Type  word  RUN  and hit <RETURN> to see how it sounds. What we've done
here is combine several attack and decay settings. The settings are: HIGH
ATTACK  (128)  +  LOW ATTACK (32) + LOWEST ATTACK (16) + HIGH DECAY (8) +
MEDIUM DECAY (4) + LOW DECAY (2) = 190.  This  effect sounds like a sound
an  oboe  or  other  "reedy"  instrument  might  make.  If  you'd like to
experiment,  try  changing  the  waveform and attack/decay numbers in the
musical scale example to see how an "oboe" sounds.  Thus ...  you can see
that  changing  the  attack/decay  rates  can be used to create different
types of sound effects.

  4. SUSTAIN/RELEASE SETTING. --  Like Attack/Decay,  the SUSTAIN/RELEASE
setting is activated by the ADSR/WAVEFORM CONTROL.  SUSTAIN/RELEASE  lets
you "extend" (SUSTAIN) a portion of a particular sound, like the "sustain
pedal"  on  a  piano or organ which lets you prolong a note.  Any note or
sound  can  be  sustained  at  any one of 16 levels.  The SUSTAIN/RELEASE
setting  may  be  used with a FOR ... NEXT loop to determine how long the
note will be held at SUSTAIN volume before being released.  The following
chart  shows  the  numbers  you  have to POKE to reach different SUSTAIN/
RELEASE rates.

                      SUSTAIN/RELEASE RATE SETTINGS

   SUSTAIN/RELEASE   HIGH  MEDIUM  LOW   LOWEST  HIGH MEDIUM LOW  LOWEST
   CONTROL  SETTING           SUSTAIN          |        RELEASE
 +---------+-------+------+------+------+------+-----+-----+-----+-----+
 | VOICE 1 | 54278 |  128 |  64  |  32  |  16  |  8  |  4  |  2  |  1  |
 +---------+-------+------+------+------+------+-----+-----+-----+-----+
 | VOICE 2 | 54285 |  128 |  64  |  32  |  16  |  8  |  4  |  2  |  1  |
 +---------+-------+------+------+------+------+-----+-----+-----+-----+
 | VOICE 3 | 54292 |  128 |  64  |  32  |  16  |  8  |  4  |  2  |  1  |
 +---------+-------+------+------+------+------+-----+-----+-----+-----+

  As  an  example,  if  you're using VOICE 1,  you can set a HIGH SUSTAIN
level by typing: POKE 54278,128 or you could combine a HIGH SUSTAIN level
with a LOW RELEASE rate by adding 128 + 2 and then POKE 54278,130. Here's
the  same  sample  program  we used in the ATTACK/DECAY section above ...
with a SUSTAIN/RELEASE feature added. Notice the difference in sounds.

   5 FOR L=54272 TO 54296:POKE L,0:NEXT  Clear sound chip.
  10 PRINT "HIT ANY KEY"  <------------- Screen message
  20 POKE 54296,15  <------------------- Set VOLUME at highest level.
  30 POKE 54277,64  <------------------- Set Attack/Decay.
  40 POKE 54278,128 <------------------- Set Sustain/Release.
  50 POKE 54273,17 : POKE 54272,37  <--- POKE one note into VOICE 1.
  60 GET K$ : IF K$ = "" THEN 60  <----- Check the keyboard.
  70 POKE 54276,17: FOR T=1 TO 200: NEXT Set waveform control (triangle).
  80 POKE 54276,16: FOR T=1 TO 50: NEXT  Turn off settings.
  90 GOTO 20  <------------------------- Loop back and do it again.

  In line 30,  we tell the computer to SUSTAIN the note at a HIGH SUSTAIN
level (128 from chart above) ... after which the tone is released in line
80.  You  can vary the duration of a note by changing the "count" in line
70.  To see the effect of using the release function try changing line 30
to POKE 54278,89 (SUSTAIN = 80, RELEASE = 9).

  5. CHOOSING VOICES AND SETTING HIGH/LOW FREQUENCY SOUND VALUES. -- Each
individual  note  on the Commodore 64 requires TWO SEPARATE POKE COMMANDS
...  one  for  HIGH FREQUENCY and one for LOW FREQUENCY. The MUSICAL NOTE
VALUE  table  in Appendix M shows you the corresponding POKEs you need to
play any note in the Commodore 64's eight octave range.  The HIGH and LOW
FREQUENCY POKE COMMANDS  are  different  for each VOICE you use  --  this
allows  you to program all 3 voices independently to create 3-voice music
or exotic sound effects.
  The  HIGH  and  LOW FREQUENCY POKE COMMANDS for each voice are shown in
the  chart  below,  which  also  contains  the NOTE VALUES for the middle
(fifth) octave.

                              SAMPLE MUSICAL NOTES - FIFTH OCTAVE
VOICE NUMBER  POKE  +--+--+---+---+--+---+---+--+---+---+---+---+---+---+
& FREQUENCY   NUMBER| C|C#| D | D#| E| F | F#| G| G#| A | A#| B | C | C#|
+-------------------+--+--+---+---+--+---+---+--+---+---+---+---+---+---+
|VOICE 1/HIGH|54273 |34|36| 38| 40|43| 45| 48|51| 54| 57| 61| 64| 68| 72|
|VOICE 1/LOW |54272 |75|85|126|200|52|198|127|97|111|172|126|188|149|169|
+-------------------+--+--+---+---+--+---+---+--+---+---+---+---+---+---+
|VOICE 2/HIGH|54280 |34|36| 38| 40|43| 45| 48|51| 54| 57| 61| 64| 68| 72|
|VOICE 2/LOW |54279 |75|85|126|200|52|198|127|97|111|172|126|188|149|169|
+-------------------+--+--+---+---+--+---+---+--+---+---+---+---+---+---+
|VOICE 3/HIGH|54287 |34|36| 38| 40|43| 45| 48|51| 54| 57| 61| 64| 68| 72|
|VOICE 3/LOW |54286 |75|85|126|200|52|198|127|97|111|172|126|188|149|169|
+-------------------+--+--+---+---+--+---+---+--+---+---+---+---+---+---+

  As you can see,  there are 2 settings for each voice,  a HIGH FREQUENCY
setting  and  a LOW FREQUENCY setting.  To play a musical note,  you must
POKE  a  value  into  the HIGH FREQUENCY location and POKE another values
into  the  LOW FREQUENCY  location.  Using  the  settings  in  our VOICE/
FREQUENCY/NOTE VALUE  table,  here's the setting that plays a C note from
the 5th octave (VOICE 1):

  POKE 54273,34 : POKE 54272,75

The same note on VOICE 2 would be:

  POKE 54280,34 : POKE 54279,75

Used in a program, it looks like this:

   5 FORL=54272TO54296:POKEL,0:NEXT  Clear sound chip.
  10 V=54296:W=54276:A=54277:  <---- Set numbers equal to letters.
     S=54278:H=54273:L=54272
  20 POKE V,15:POKE A,190:POKE S,89  POKE volume, waveform, attack/decay.
  30 POKE H,34:POKE L,75  <--------- POKE hi/lo freq. notes.
  40 POKE W,33:FOR T=1 TO 200:NEXT   Start note, let it play.
  50 POKE W,32  <------------------- Stop note.

7.6. Playing a Song on the Commodore 64

  The  following  program  can  be  used to compose or play a song (using
VOICE 1).  There are two important lessons in this program:  first,  note
how  we  abbreviate all the long control numbers in the first line of the
program ... after that, we can use the letter W for "Waveform" instead of
the number 54276.
  The second lesson concerns the way we use the DATA. This program is set
up  to  let  you  enter 3 numbers for each note:  the HIGH FREQUENCY NOTE
VALUE,  the  LOW FREQUENCY NOTE VALUE,  and the DURATION THE NOTE will be
played.
  For  this  song,  we used a duration "count" of 125 for an eighth note,
250  for  a quarter note,  375 for a dotted quarter note,  500 for a half
note  and 1000 for a whole note.  These number values can be increased or
decreased to match a particular tempo, or your own musical taste.
  To see how a song gets entered, look at line 100.  We entered 34 and 75
as  our  HIGH  and  LOW FREQUENCY  settings  to play a "C" note (from the
sample  scale  shown  previously)  and  then the number 250 for a quarter
note.  So the first note in our song is a quarter note C. The second note
is also a quarter note,  this time the note is "E"  ...  and so on to the
end of our tune.  You can enter almost any song this way,  adding as many
DATA statement lines as you need.  You can continue the note and duration
numbers  from one line to the next but each line must begin with the word
DATA.  DATA -1,-1,-1  should be the last line in your program.  This line
"ends" the song.
  Type  the  word  NEW  to  erase  your  previous program and type in the
following program, then type RUN to hear the song.

  MICHAEL ROW  THE BOAT ASHORE-1 MEASURE

   2 FOR L = 54272 TO 54296 : POKE L,0 : NEXT
   5 V=54296:W=54276:A=54277:HF=54273:LF=54272:S=54278:PH=54275:PL=54274
  10 POKE V,15 : POKE A,88 : POKE PH,15 : POKE PL,15 : POKE S,89
  20 READ H : IF H = -1 THEN END
  30 READ L
  40 READ D
  60 POKE HF,H : POKE LF,L : POKE W,65
  80 FOR T = 1 TO D : NEXT : POKE W,64
  85 FOR T = 1 TO 50 : NEXT
  90 GOTO 10
 100 DATA 34,75,250,43,52,250,51,97,375,43,52,125,51,97
 105 DATA 250,57,172,250
 110 DATA 51,97,500,0,0,125,43,52,250,51,97,250,57,172
 115 DATA 1000,51,97,500
 120 DATA -1,-1,-1

7.7. Creating Sound Effects

  Unlike  music,  sound  effects  are  more  often  tied  to  a  specific
programming "action" such as the explosion made by an astro-fighter as it
crashes through a barrier in a space game  ... or the warning buzzer in a
business  program  that  tells  the  user he's about to erase his disk by
mistake.
  You  have  a  wide  range  of  options available  if you want to create
different sound effects.  Here are 10 programming ideas  which might help
you get started experimenting with sound effects:

  1. Change the volume while a note is playing,  for example to create an
     "echo" effect.
  2. Vary between two notes rapidly to create a sound "tremor."
  3. Waveform ... try different settings for each voice.
  4. Attack/Decay  ...  to alter the rate a sound rises toward its "peak"
     volume and rate it diminishes from that peak.
  5. Sustain/Release  ...  to change sustain to volume of a sound effect,
     and rate it diminishes from that volume.
  6. Multivoice effects ... playing more than one voice at the same time,
     each voice independently controlled,  or one voice playing longer or
     shorter then another, or serving as an "echo" or response to a first
     note.
  7. Changing notes on the scale,  or changing octaves,  using the values
     in the MUSICAL NOTE VALUE table.
  8. Use  the  Square Waveform  and  different  Pulse Settings  to create
     different effects.
  9. Use the Noise Waveform to generate "white noise" for accenting tonal
     sound effects or creating explosions,  gunshots  or  footsteps.  The
     same musical notes that create music can also be used with the Noise
     Waveform to create different types of white noise.
 10. Combine  several  HIGH/LOW  frequencies  in  rapid succession across
     different octaves.
 11. Filter ... try the extra POKE setting in Appendix M.

7.8. Sample Sound Effects To Try

  The  following  programs may be added to almost any BASIC program. They
are  included  to  give  you  some  programming ideas and demonstrate the
Commodore 64's sound effect range.
  Notice  the  programming  shortcut  we're  using  in  line  10.  We can
abbreviate  those  long cumbersome sound setting numbers by defining them
as  easy-to-use  letters  (numeric variables).  Line 10 simply means that
these easy to remember LETTERS can be used instead of those long numbers.
Here,  V=Volume, W=Waveform,  A=Attack/Decay, H=High Frequency (VOICE 1),
and  L=Low Frequency  (VOICE 1).  We  then  use  these letters instead of
numbers in our program ... making our program shorter, typing faster, and
the sound settings easier to remember and spot.

DOLL CRYING

  10 V=54296 : W=54276 : A=54277 : H=54273 : L=54272
  20 POKE V,15 : POKE W,65 : POKE A,15
  30 FOR X = 200 TO 5 STEP -2 : POKE H,40 : POKE L,X : NEXT
  40 FOR X = 150 TO 5 STEP -2 : POKE H,40 : POKE L,X : NEXT
  50 POKE W,0

SHOOTING SOUND ... USING VOICE 1, NOISE WAVEFORM, FADING VOLUME

  10 V=54296 : W=54276 : A=54277 : H=54273 : L=54272
  20 FOR X = 15 TO 0 STEP -1 : POKE V,X : POKE W,129:
     POKE A,15 : POKE H,40 : POKE L,200 : NEXT
  30 POKE W,0 : POKE A,0

