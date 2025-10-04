# Anglo Concertina Physical Constraints
## C/G 30-button Jeffries Layout

This document outlines the **impossible note combinations** on a C/G 30-button Anglo concertina. These constraints must be respected when generating harmony and chord voicings.

---

## Why These Constraints Matter

The Anglo concertina is a **bisonoric** instrument - each button produces different notes on push vs pull. This means:

- You **cannot play a push note and a pull note simultaneously**
- Certain note combinations require impossible bellows directions
- Some intervals/chords are physically unplayable

---

## Basic Impossible Pairs

These note pairs **cannot sound together**:

- **F# + C**
- **F# + F natural**
- **Bb + B natural**
- **Bb + D**
- **Bb + G**
- **Eb + E natural**
- **Eb + G**
- **Eb + B natural**

---

## Chromatic Conflicts

Any chromatic pair (sharp/flat + its natural) is impossible:

- **Bb + B**
- **Eb + E**
- **Ab + A**
- **Db + D**
- **F# + F**
- **C# + C**
- **G# + G**

---

## Extended Impossible Combinations

### F# cannot combine with:
- C
- F
- Bb
- Eb

### Bb cannot combine with:
- B natural
- D
- G
- E
- A

### Eb cannot combine with:
- E natural
- G
- B natural
- D
- A

### C# cannot combine with:
- C
- F
- Bb
- Eb
- **(C# is extremely limited - avoid in harmonies)**

---

## Three-Note Impossible Combinations

Any chord containing these combinations is unplayable:

- **F# + C** (in any chord)
- **Bb + G** (in any chord)
- **Eb + E natural** (in any chord)
- **F + B + D together**
- **C + D + F# together**

---

## Generally Limited Notes

These notes have **very restricted harmonic possibilities**:

| Note | Limitation |
|------|------------|
| **C#** | Almost no harmonic combinations available |
| **G# / Ab** | Very limited combinations |
| **F#** | Cannot combine with most push-direction notes |
| **Bb** | Cannot combine with most pull-direction notes |
| **Eb** | Cannot combine with most pull-direction notes |

---

## Simple Validation Rule

**If a combination contains ANY pair from the "Basic Impossible Pairs" list above, the entire chord/harmony cannot be played.**

---

## Playable Intervals (Safe Choices)

These intervals are **generally safe** on C/G Anglo:

### Major/Minor Thirds
- C-E
- D-F
- E-G
- G-B
- A-C

### Perfect Fourths
- E-A (very common in modal tunes)
- A-D (drone-friendly)
- D-G
- G-C

### Perfect Fifths
- A-E
- D-A
- G-D
- C-G

### Octaves
- All octaves are playable (same note, different register)

---

## Recommended Harmony Approaches for Anglo

1. **Quartal Harmony (Fourths)**
   - E-A, A-D are highly playable
   - Modern sound, safe on anglo

2. **Diatonic Thirds**
   - Traditional Irish approach
   - Validate each third individually

3. **Open Fifths**
   - Very safe, traditional sound
   - A-E, D-A work well for Dorian tunes

4. **Modal Drones**
   - A-D pedal works perfectly
   - Low register, sustained

5. **Sparse Harmony**
   - Add harmony on strong beats only (beats 1 & 5 in 6/8)
   - Reduces complexity, ensures playability

---

## Validation Workflow

When generating harmony:

1. **Parse the chord** into individual notes
2. **Check all pairs** against the Impossible Pairs list
3. **If any impossible pair exists**, reject the chord
4. **Suggest alternative** (drop one note, substitute with safe interval)

---

## Example: Validating a Chord

```
Chord: [E, A, C#]

Check pairs:
- E + A: ✅ Safe (perfect fourth)
- E + C#: ❌ UNSAFE (C# is very limited)
- A + C#: ❌ UNSAFE (C# conflicts with many notes)

Result: ❌ UNPLAYABLE

Alternative: [E, A] (drop C#)
- E + A: ✅ Safe (perfect fourth)

Result: ✅ PLAYABLE
```

---

## Notes for Developers

- **Always validate** before presenting a harmony to the user
- **Filter out** impossible combinations automatically
- **Suggest alternatives** when validation fails
- **Test with real Anglo layout** if possible (simulator coming soon)

---

## Future Enhancements

- Button layout simulator
- Fingering pattern analysis
- Stretch distance validation (some intervals are theoretically playable but physically difficult)
- Cross-rowing complexity scoring

---

## References

- Based on C/G 30-button Jeffries layout
- Tested against common Irish session tunes in A Dorian, G Major, D Major
- Constraints apply to **simultaneous notes only** (melody notes played sequentially are always fine)
