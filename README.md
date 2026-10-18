# Pussy

**Status ~2026.10.17:  Pussy can run the Minsky two-counter machine (and a bit more) and is considered a complete experiment in a Turing-complete cat language.**

<img width="106" height="114" alt="image" src="https://github.com/user-attachments/assets/f3a88510-34d7-47f2-8a20-470ef0d316e2" />

A tiny programming language built into a cat.  Pussy is Turing-complete as it can
implement a two-counter Minsky machine (it has three counters).

Pussy is an esolang whose canonical rendering is not monospace.  The program isn’t a grid of cells
but a line of prose that happens to be a cat.  Layout is purely semantic, whitespace is cosmetic,
and the parser only cares about the face glyphs and the counts of `～`, `🐾`, and `~`.  You can
paste a program into a tweet and it will still run.

&nbsp;&nbsp;&nbsp;&nbsp;／l、<br>
（ﾟ､ ｡ ﾟ７<br>
&nbsp;&nbsp;&nbsp;l、ﾞ ~ヽ<br>
&nbsp;&nbsp;&nbsp;じし_,)～～～ノ ...🐾🐾
 
## How it works
 
Pussy is a three-counter machine. One live cat holds the state; its body parts are the counters and they grow as the numbers do:
 
| Counter  | Where it lives                        |
|----------|---------------------------------------|
| tail     | `～` wags inside the tail: `)～～～ノ`   |
| tracks   | `🐾` paw prints trailing behind       |
| whiskers | `~` on the cheek line                 |
 
The program is a sequence of cats separated by blank lines. Each frame's **eyes** are the opcode, its **mouth** picks the counter, and its **tracks** are a jump target:
 
| Eyes       | Face   | Does                                       |
|------------|--------|--------------------------------------------|
| `(ﾟ ﾟ)`    | awake  | `INC` — the counter grows by one           |
| `(ー ﾟ)`   | blink  | `DEC` — shrink by one; if already 0, skip the next frame |
| `(ﾟ ー)`   | wink   | `JMP` — go to the frame numbered by this frame's paw prints |
| `(ー ー)`  | asleep | `HALT`                                     |
 
| Mouth | Counter  |
|-------|----------|
| `｡`   | tail     |
| `ω`   | tracks   |
| `､`   | whiskers |
 
So a cat blinking its left eye at its tail means "take one off the tail". A winking cat with three paw prints means "go to frame 3".
 
Input is the starting cat. Output is the cat when it falls asleep (or when you stop watching). Nothing else is needed: three unbounded counters make this a Minsky machine, so it is Turing-complete.
 
## Running it
 
```
python3 pussy.py 1200
```
 
prints the cat each time it finishes a Fibonacci step. The number alternates between the tail and the tracks, so you watch it grow a long tail, then leave a lot of tracks, then a longer tail.
 
## Notes

- Pussy is meant to be read in a **proportional font**. The original kaomoji was drawn for one, and the parser only looks at the face glyphs and counts of `～`, `🐾` and `~`, so whitespace and alignment are cosmetic. A program pasted into a tweet still runs.
- The face bracket `（` is fullwidth (U+FF08), as are `／` and `７`. Swap for ASCII `(` if your target context can't cope.
