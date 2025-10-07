"""
Brenda Castles Melodic Variations
Generates variation ideas following Brenda Castles teaching methodology

Core Principles:
1. "Long notes, short notes" - fill in long notes or consolidate short notes
2. No technique required - pure mathematical manipulation
3. Find repeating phrases and vary them

All 8 Variation Techniques (from Brenda Castles transcript):

1. FILL LONG NOTES - Fill in long notes with neighbor/passing tones
   Example: D2 A → D E D, A G A
   "Take long notes and fill them in with shorter notes"

2. CONSOLIDATE TO LONG - Turn groups of short notes into sustained long notes
   Example: D E D A G A → D3 A3 (dotted quarters in 6/8)
   "Find groups of short notes and throw in a long note - needs attitude!"

3. CHORD SUBSTITUTION - Insert notes from the underlying chord
   Example: D2 A → D A D (using A from D chord: D-F#-A)
   "Substitute with harmony notes - what chord are we on?"

4. SLIDE APPROACH - Approach target note from below (like a slide/grace note)
   Example: D2 A → C D C A
   "Pick the note just below and land on it"

5. OCTAVE DISPLACEMENT - Move individual notes up/down an octave
   Example: D D D → D' D D or D C B → D' C B
   "Try going to high D instead - just shift one note"

6. MOVE ALONG - Extend one note to absorb the next note's duration
   Example: D' B C A → D'2 C A (extend D', eliminate B)
   "Make it move along - extend notes by eliminating others"

7. DOUBLE/TRIPLE NOTES - Repeat notes where there were long notes
   Example: D2 → D D D
   "Double up the notes - D D B, C C A"

8. STRATEGIC LENGTHENING - Extend certain notes by removing others
   Example: A B C D E F → A2 C D E2 (extend A & E, remove B & F)
   "Create space for ornaments by strategic lengthening - needs attitude!"

All techniques maintain the bar length and time signature.
"""
import random
import re
from typing import List, Dict, Tuple
from . import repetition_detector


def parse_abc_notes(abc_phrase: str) -> List[Tuple[str, int]]:
    """
    Parse ABC notation into (note, duration) pairs

    Examples:
        "DED" → [('D',1), ('E',1), ('D',1)]
        "D2A" → [('D',2), ('A',1)]
        "A-A" → [('A',1), ('A',1)]  # ties treated as separate

    Returns list of (note, duration) where duration 1 = eighth note
    """
    notes = []
    i = 0
    phrase = abc_phrase.replace('-', '').replace('|', '').strip()

    while i < len(phrase):
        # Get note (including octave markers ' or ,)
        note = phrase[i]
        i += 1

        # Handle octave markers
        while i < len(phrase) and phrase[i] in ["'", ","]:
            note += phrase[i]
            i += 1

        # Get duration (default 1)
        duration = 1
        if i < len(phrase) and phrase[i].isdigit():
            duration = int(phrase[i])
            i += 1

        notes.append((note, duration))

    return notes


def notes_to_abc(notes: List[Tuple[str, int]]) -> str:
    """Convert (note, duration) pairs back to ABC notation with proper beaming for 6/8"""
    result = []
    total_duration = 0

    for i, (note, duration) in enumerate(notes):
        # Add the note
        if duration == 1:
            result.append(note)
        else:
            result.append(f"{note}{duration}")

        total_duration += duration

        # Add space after every 3 eighth notes for 6/8 beaming
        # (but not at the end)
        if total_duration % 3 == 0 and i < len(notes) - 1:
            result.append(' ')

    return ''.join(result)


# ============================================================================
# BRENDA'S 8 VARIATION TECHNIQUES
# ============================================================================

def count_changes(original: str, variation: str) -> int:
    """Count how many notes are different between original and variation"""
    orig_notes = parse_abc_notes(original)
    var_notes = parse_abc_notes(variation)
    changes = 0
    for i in range(min(len(orig_notes), len(var_notes))):
        if i >= len(orig_notes) or i >= len(var_notes) or orig_notes[i] != var_notes[i]:
            changes += 1
    changes += abs(len(orig_notes) - len(var_notes))
    return changes


def variation_fill_long_notes(phrase: str) -> Dict:
    """
    Technique 1: Fill in long notes with passing/neighbor tones
    Example: D2A → DED AGA (D-E-D, A-G-A)
    """
    notes = parse_abc_notes(phrase)

    # Generate multiple variations and pick the simplest that's different
    candidates = []
    for attempt in range(5):  # Try 5 times
        result = []
        for note, duration in notes:
            if duration >= 2 and random.random() < 0.7:  # Fill 70% of long notes
                # Fill long note with neighbor tone
                base_note = note.replace("'", "").replace(",", "")
                octave = note[len(base_note):]

                # Randomly choose note below or above
                if random.random() < 0.5:
                    note_neighbor = chr(ord(base_note) - 1) if base_note > 'A' else 'G'
                else:
                    note_neighbor = chr(ord(base_note) + 1) if base_note < 'G' else 'A'

                result.append((note, 1))
                result.append((note_neighbor + octave, 1))

                # Add remaining duration
                for _ in range(duration - 2):
                    result.append((note, 1))
            else:
                result.append((note, duration))

        abc = notes_to_abc(result)
        if abc != notes_to_abc(notes):  # Only keep if different
            candidates.append((abc, count_changes(phrase, abc)))

    # Pick the simplest (fewest changes)
    if candidates:
        candidates.sort(key=lambda x: x[1])
        return {
            'abc': candidates[0][0],
            'description': 'Fill long notes with neighbor tones'
        }
    else:
        return {
            'abc': notes_to_abc(notes),
            'description': 'Fill long notes with neighbor tones'
        }


def variation_consolidate_to_long(phrase: str) -> Dict:
    """
    Technique 2: Consolidate short notes into longer sustained notes
    Example: DED AGA → D3 A3 (dotted quarter notes in 6/8)

    Generate multiple candidates and pick the simplest that differs from original.
    """
    notes = parse_abc_notes(phrase)

    # Generate multiple variations and pick simplest
    candidates = []
    for attempt in range(5):
        result = []
        i = 0
        consolidations = 0
        max_consolidations = 1  # Only consolidate 1 group for subtlety

        while i < len(notes):
            if i + 2 < len(notes) and consolidations < max_consolidations and random.random() < 0.5:
                # Group of 3 → keep first with duration 3
                result.append((notes[i][0], 3))
                i += 3
                consolidations += 1
            else:
                result.append(notes[i])
                i += 1

        abc = notes_to_abc(result)
        if abc != notes_to_abc(notes):  # Only keep if different
            candidates.append((abc, count_changes(phrase, abc)))

    # Pick simplest (fewest changes)
    if candidates:
        candidates.sort(key=lambda x: x[1])
        return {
            'abc': candidates[0][0],
            'description': 'Consolidate to long notes (needs attitude!)'
        }

    # Fallback if no different variations
    return {
        'abc': notes_to_abc(notes),
        'description': 'Consolidate to long notes (original)'
    }


def variation_double_notes(phrase: str) -> Dict:
    """
    Technique 7: Double/triple notes where there were long notes
    Example: D2 → DDD

    Generate multiple candidates and pick the simplest that differs from original.
    """
    notes = parse_abc_notes(phrase)

    # Generate multiple variations and pick simplest
    candidates = []
    for attempt in range(5):
        result = []
        doubled_count = 0
        max_doubled = 1  # Only double 1 note for subtlety

        for note, duration in notes:
            if duration >= 2 and doubled_count < max_doubled and random.random() < 0.5:
                # Replace with repeated notes
                for _ in range(duration):
                    result.append((note, 1))
                doubled_count += 1
            else:
                result.append((note, duration))

        abc = notes_to_abc(result)
        if abc != notes_to_abc(notes):
            candidates.append((abc, count_changes(phrase, abc)))

    # Pick simplest
    if candidates:
        candidates.sort(key=lambda x: x[1])
        return {
            'abc': candidates[0][0],
            'description': 'Double/triple notes'
        }

    return {
        'abc': notes_to_abc(notes),
        'description': 'Double/triple notes (original)'
    }


def variation_octave_displacement(phrase: str) -> Dict:
    """
    Technique 5: Move one note up OR down by exactly one octave
    Example: DDD → D'DD (up) or d'cd' → dcd' (down)
    ALWAYS moves by exactly 1 octave (12 semitones), never more
    """
    notes = parse_abc_notes(phrase)

    # Generate multiple candidates and pick simplest
    candidates = []
    for attempt in range(5):
        result = []
        if len(notes) > 0 and random.random() > 0.3:
            displace_idx = random.randint(0, len(notes) - 1)
            # Randomly choose up or down
            go_up = random.random() < 0.5

            for i, (note, duration) in enumerate(notes):
                if i == displace_idx:
                    # Move this note exactly one octave
                    if go_up:
                        # Add one apostrophe for up
                        result.append((note + "'", duration))
                    else:
                        # Add one comma for down (or remove one apostrophe if present)
                        if "'" in note:
                            # Remove one apostrophe
                            result.append((note.replace("'", "", 1), duration))
                        else:
                            # Add comma to go down
                            result.append((note + ",", duration))
                else:
                    result.append((note, duration))
        else:
            result = list(notes)

        abc = notes_to_abc(result)
        if abc != notes_to_abc(notes):
            candidates.append((abc, count_changes(phrase, abc)))

    # Pick simplest
    if candidates:
        candidates.sort(key=lambda x: x[1])
        return {
            'abc': candidates[0][0],
            'description': 'Octave displacement'
        }

    return {
        'abc': notes_to_abc(notes),
        'description': 'Octave displacement (original)'
    }


def variation_move_along(phrase: str) -> Dict:
    """
    Technique 6: Extend a note to absorb the next note's space
    Example: D'BCA → D'2CA (C absorbs B)
    """
    notes = parse_abc_notes(phrase)

    if len(notes) < 3 or random.random() < 0.3:  # Only skip 30% of the time
        return {'abc': notes_to_abc(notes), 'description': 'Move along (original)'}

    result = []
    # Randomly pick a note to extend
    extend_idx = random.randint(0, min(2, len(notes) - 2))

    for i, (note, duration) in enumerate(notes):
        if i == extend_idx and i + 1 < len(notes):
            # Extend this note and skip the next one
            result.append((note, duration + 1))
        elif i == extend_idx + 1:
            # Skip this note (it was absorbed)
            pass
        else:
            result.append((note, duration))

    return {
        'abc': notes_to_abc(result),
        'description': 'Move along - extend and eliminate'
    }


def variation_slide_approach(phrase: str) -> Dict:
    """
    Technique 4: Approach first note from below (like a slide)
    Example: D2A → CDC A (slide up to D from C)
    """
    notes = parse_abc_notes(phrase)

    if len(notes) == 0 or random.random() < 0.5:  # Only apply 50% of the time
        return {'abc': notes_to_abc(notes), 'description': 'Slide approach (original)'}

    result = []

    # Pick a random long note to add a slide to
    long_note_indices = [i for i, (n, d) in enumerate(notes) if d >= 2]

    if long_note_indices and random.random() > 0.3:
        slide_idx = random.choice(long_note_indices)

        for i, (note, duration) in enumerate(notes):
            if i == slide_idx:
                base_note = note.replace("'", "").replace(",", "")
                octave = note[len(base_note):]
                note_below = chr(ord(base_note) - 1) if base_note > 'A' else 'G'

                result.append((note_below + octave, 1))
                result.append((note, 1))
                if duration > 2:
                    result.append((note, duration - 2))
            else:
                result.append((note, duration))
    else:
        result = list(notes)

    return {
        'abc': notes_to_abc(result),
        'description': 'Slide approach from below'
    }


def variation_chord_substitution(phrase: str, key: str = 'D') -> Dict:
    """
    Technique 3: Substitute with chord tones
    Example in D: D2A → DAD ABA (use A from D chord: D-F#-A)
    """
    # Simplified chord tones for common keys
    chord_tones = {
        'D': ['D', 'F', 'A'],  # Simplified - ignoring sharps for ABC
        'G': ['G', 'B', 'D'],
        'A': ['A', 'C', 'E']
    }

    tones = chord_tones.get(key, ['D', 'F', 'A'])
    notes = parse_abc_notes(phrase)
    result = []

    for note, duration in notes:
        if duration >= 2:
            base_note = note.replace("'", "").replace(",", "")
            octave = note[len(base_note):]

            # Find a chord tone different from current note
            available = [t for t in tones if t != base_note]
            if available:
                chord_note = random.choice(available)
                result.append((note, 1))
                result.append((chord_note + octave, 1))

                # Add remaining duration
                for _ in range(duration - 2):
                    result.append((note, 1))
            else:
                result.append((note, duration))
        else:
            result.append((note, duration))

    return {
        'abc': notes_to_abc(result),
        'description': 'Chord tone substitution'
    }


def variation_strategic_rests(phrase: str) -> Dict:
    """
    Technique 8: Strategic lengthening - extend notes by removing others
    Example: ABCDEF → A2CD E2 (extend A and E, remove B and F)
    """
    notes = parse_abc_notes(phrase)

    if len(notes) < 4 or random.random() < 0.6:  # Only apply 40% of the time
        return {'abc': notes_to_abc(notes), 'description': 'Strategic lengthening (original)'}

    # Extend some notes by eliminating others (but not all pairs)
    result = []
    i = 0
    while i < len(notes):
        if i + 1 < len(notes) and random.random() < 0.5:  # Only extend 50% of pairs
            # Take this note, extend it, skip next
            result.append((notes[i][0], notes[i][1] + notes[i+1][1]))
            i += 2
        else:
            # Keep as is
            result.append(notes[i])
            i += 1

    return {
        'abc': notes_to_abc(result),
        'description': 'Strategic lengthening (needs attitude!)'
    }


def generate_variation_ideas(original_lick: str, num_ideas: int = 5, key: str = 'D') -> List[Dict]:
    """
    Generate variation ideas for a repeated lick using Brenda Castles methods

    Args:
        original_lick: ABC notation of the original repeated section (e.g., "DED A2A" or "BAGABc|d2BcBA")
        num_ideas: Number of variation ideas to generate
        key: Musical key for chord substitutions

    Returns:
        List of variation ideas, each with 'abc' and 'description'
    """

    # Split by bars if multi-bar phrase
    bars = [b.strip() for b in original_lick.split('|') if b.strip()]

    # Apply all 8 techniques to each bar separately, then recombine
    all_variations = []
    technique_funcs = [
        variation_fill_long_notes,
        variation_consolidate_to_long,
        variation_double_notes,
        variation_octave_displacement,
        variation_move_along,
        variation_slide_approach,
        lambda x: variation_chord_substitution(x, key),
        variation_strategic_rests,
    ]

    for func in technique_funcs:
        varied_bars = []
        descriptions = []

        for bar in bars:
            result = func(bar)
            varied_bars.append(result['abc'])
            descriptions.append(result['description'])

        # Combine bars back with |
        combined_abc = '|'.join(varied_bars)
        # Use first description (they should all be the same technique)
        combined_desc = descriptions[0]

        all_variations.append({
            'abc': combined_abc,
            'description': combined_desc
        })

    # Filter out any that are identical to original
    original_normalized = original_lick.replace('|', '').replace('-', '').replace(' ', '')
    unique_variations = [
        v for v in all_variations
        if v['abc'].replace('|', '').replace(' ', '') != original_normalized
    ]

    # Return requested number (or all if fewer)
    return unique_variations[:num_ideas] if num_ideas < len(unique_variations) else unique_variations


def apply_variations_to_tune(
    abc: str,
    repeated_phrases: List[Dict],
    variation_ideas: List[Dict]
) -> Dict:
    """
    Apply random variation ideas to repeated sections of the tune

    Args:
        abc: Original ABC notation
        repeated_phrases: List of repeated phrase info from repetition_detector
        variation_ideas: List of variation idea groups

    Returns:
        Dict with 'applied_abc' and 'variation_mapping'

    This randomly selects variations to apply to each occurrence of repeated phrases
    """

    # Use measure extraction that preserves durations
    measures = repetition_detector.extract_measures_with_durations(abc)
    modified_bars = set()  # Track which bars were modified (0-indexed)

    variation_mapping = {}

    # Apply variations to each variation group
    for var_group in variation_ideas:
        if not var_group.get('ideas'):
            continue

        original = var_group['original']

        # For each repeated phrase occurrence, pick a random variation
        for phrase_info in repeated_phrases:
            if phrase_info.get('original_text', '').replace('|', '').replace(' ', '') == original.replace('|', '').replace(' ', ''):
                occurrences = phrase_info.get('occurrences', [])
                phrase_length = phrase_info.get('length', 1)

                for start_bar in occurrences:
                    # Randomly choose: keep original or use a variation
                    if random.random() < 0.7:  # 70% chance to use variation
                        variation = random.choice(var_group['ideas'])

                        # The variation ABC is the entire phrase - we need to split it by bars if it's multi-bar
                        variation_bars = variation['abc'].split('|')
                        variation_bars = [b.strip() for b in variation_bars if b.strip()]

                        # Replace the measures in this phrase
                        for offset in range(min(phrase_length, len(variation_bars))):
                            bar_idx = start_bar + offset
                            if bar_idx < len(measures):
                                # Replace this measure with the corresponding variation bar
                                if offset < len(variation_bars):
                                    measures[bar_idx] = variation_bars[offset]
                                    modified_bars.add(bar_idx)
                                    variation_mapping[f"Bar {bar_idx + 1}"] = variation_bars[offset]

    # Reconstruct ABC with annotations
    # Extract header
    lines = abc.split('\n')
    music_start = 0
    for i, line in enumerate(lines):
        if line.startswith('K:'):
            music_start = i + 1
            break
    headers = '\n'.join(lines[:music_start])

    # Reconstruct music with VARIED annotations
    music_lines = []
    current_line = []
    bar_count = 0

    for i, measure in enumerate(measures):
        # Add VARIED annotation if this measure was modified
        if i in modified_bars:
            measure_annotated = f'"^VARIED"{measure}'
        else:
            measure_annotated = measure

        current_line.append(measure_annotated)
        bar_count += 1

        # Start new line every 4 bars or at the end
        if bar_count % 4 == 0 or i == len(measures) - 1:
            music_lines.append('|' + '|'.join(current_line) + '|')
            current_line = []

    applied_abc = headers + '\n' + '\n'.join(music_lines)

    return {
        'applied_abc': applied_abc,
        'variation_mapping': variation_mapping
    }
