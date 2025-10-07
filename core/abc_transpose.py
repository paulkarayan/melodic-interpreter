"""
ABC Notation Transposition
Transposes ABC notation while maintaining octave register
"""
import re
from typing import Tuple

try:
    from music21 import converter, interval, note
    MUSIC21_AVAILABLE = True
except ImportError:
    MUSIC21_AVAILABLE = False


# Chromatic note mapping (C=0, C#=1, D=2, etc.)
NOTE_TO_SEMITONE = {
    'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11,
    'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11
}

SEMITONE_TO_NOTE_SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
SEMITONE_TO_NOTE_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

# Key signature to semitone offset from C
KEY_TO_SEMITONE = {
    'C': 0, 'Cmaj': 0, 'Amin': 0,
    'G': 7, 'Gmaj': 7, 'Emin': 4,
    'D': 2, 'Dmaj': 2, 'Bmin': 11,
    'A': 9, 'Amaj': 9, 'F#min': 6,
    'E': 4, 'Emaj': 4, 'C#min': 1,
    'B': 11, 'Bmaj': 11, 'G#min': 8,
    'F#': 6, 'F#maj': 6, 'D#min': 3,
    'F': 5, 'Fmaj': 5, 'Dmin': 2,
    'Bb': 10, 'Bbmaj': 10, 'Gmin': 7,
    'Eb': 3, 'Ebmaj': 3, 'Cmin': 0,
    'Ab': 8, 'Abmaj': 8, 'Fmin': 5,
    'Db': 1, 'Dbmaj': 1, 'Bbmin': 10,
}


def parse_key(key_str: str) -> Tuple[str, int]:
    """
    Parse a key string like 'Dmaj' or 'G' into (key_name, semitone_offset)
    """
    key_str = key_str.strip()

    # Try exact match first
    if key_str in KEY_TO_SEMITONE:
        return key_str, KEY_TO_SEMITONE[key_str]

    # Try without 'maj' suffix
    if key_str.endswith('maj'):
        base = key_str[:-3]
        if base in KEY_TO_SEMITONE:
            return base, KEY_TO_SEMITONE[base]

    # Default to C if not found
    return 'C', 0


def get_note_semitone(note: str, accidental: str, octave_markers: str) -> int:
    """
    Get absolute semitone value for a note

    Args:
        note: Base note (C, D, E, F, G, A, B, c, d, e, f, g, a, b)
        accidental: Sharp (^) or flat (_) or natural (=)
        octave_markers: Octave markers (' for up, , for down)

    Returns:
        Absolute semitone (middle C = 60 in MIDI)
    """
    # Base semitone from note name
    base_semitone = NOTE_TO_SEMITONE[note]

    # ABC uses lowercase for higher octave, uppercase for lower
    # Middle octave is C-B (uppercase), next octave is c-b (lowercase)
    if note.isupper():
        octave = 4  # C4-B4 range
    else:
        octave = 5  # c5-b5 range

    # Adjust for octave markers
    octave += octave_markers.count("'")  # ' raises by octave
    octave -= octave_markers.count(",")  # , lowers by octave

    # Apply accidental
    if accidental == '^':
        base_semitone += 1
    elif accidental == '_':
        base_semitone -= 1
    # '=' is natural, no adjustment

    # Calculate absolute semitone (C4 = 60 in MIDI)
    absolute_semitone = (octave * 12) + base_semitone

    return absolute_semitone


def semitone_to_abc_note(semitone: int, prefer_sharps: bool = True) -> str:
    """
    Convert absolute semitone to ABC notation

    Args:
        semitone: Absolute semitone (C4 = 60 in MIDI)
        prefer_sharps: Use sharps vs flats for accidentals

    Returns:
        ABC notation string (e.g., "d", "^f", "_B,")
    """
    octave = semitone // 12
    pitch_class = semitone % 12

    # Get note name
    if prefer_sharps:
        note_name = SEMITONE_TO_NOTE_SHARP[pitch_class]
    else:
        note_name = SEMITONE_TO_NOTE_FLAT[pitch_class]

    # Determine if we need accidental
    accidental = ''
    base_note = note_name[0]
    if len(note_name) > 1:
        if note_name[1] == '#':
            accidental = '^'
        elif note_name[1] == 'b':
            accidental = '_'

    # Determine case and octave markers
    # Octave 4 (C4-B4) = uppercase
    # Octave 5 (c5-b5) = lowercase
    # Higher/lower = add markers

    if octave == 4:
        note = base_note.upper()
        octave_markers = ''
    elif octave == 5:
        note = base_note.lower()
        octave_markers = ''
    elif octave > 5:
        note = base_note.lower()
        octave_markers = "'" * (octave - 5)
    elif octave == 3:
        note = base_note.upper()
        octave_markers = ','
    elif octave < 3:
        note = base_note.upper()
        octave_markers = ',' * (4 - octave)
    else:
        note = base_note.upper()
        octave_markers = ''

    return accidental + note + octave_markers


def transpose_abc_music(abc: str, from_key: str, to_key: str) -> str:
    """
    Transpose ABC notation from one key to another while maintaining octave register

    Args:
        abc: ABC notation string (just the music body, not headers)
        from_key: Source key (e.g., 'Gmaj', 'D', 'Amin')
        to_key: Target key (e.g., 'Dmaj', 'A', 'Emin')

    Returns:
        Transposed ABC notation
    """
    _, from_semitone = parse_key(from_key)
    _, to_semitone = parse_key(to_key)

    interval = to_semitone - from_semitone

    # Use sharps if target key has sharps
    prefer_sharps = '#' in to_key or to_key in ['G', 'D', 'A', 'E', 'B', 'F#', 'Gmaj', 'Dmaj', 'Amaj', 'Emaj', 'Bmaj', 'F#maj']

    # Pattern to match ABC notes
    # Matches: [accidental][note][octave_markers][duration]
    note_pattern = r'([_=\^]*)([A-Ga-g])([,\']*)(\d*/?\d*)'

    def transpose_match(match):
        accidental = match.group(1) or ''
        note = match.group(2)
        octave_markers = match.group(3) or ''
        duration = match.group(4) or ''

        # Get current semitone
        current_semitone = get_note_semitone(note, accidental[:1] if accidental else '', octave_markers)

        # Transpose
        new_semitone = current_semitone + interval

        # Convert back to ABC
        new_note = semitone_to_abc_note(new_semitone, prefer_sharps)

        return new_note + duration

    # Transpose all notes
    transposed = re.sub(note_pattern, transpose_match, abc)

    return transposed


def transpose_abc_tune_music21(abc_full: str, from_key: str, to_key: str) -> str:
    """
    Transpose using music21 library (maintains octave register properly)

    Args:
        abc_full: Full ABC notation
        from_key: Source key (e.g., 'Gmaj', 'G')
        to_key: Target key (e.g., 'Dmaj', 'D')

    Returns:
        Transposed ABC notation in correct octave
    """
    if not MUSIC21_AVAILABLE:
        raise ImportError("music21 not available")

    try:
        # Parse ABC with music21
        score = converter.parse(abc_full, format='abc')

        # Determine transposition interval
        from_key_clean = from_key.replace('maj', '').replace('min', '')
        to_key_clean = to_key.replace('maj', '').replace('min', '')

        # Create interval for transposition
        note_from = note.Note(f'{from_key_clean}4')
        note_to = note.Note(f'{to_key_clean}4')
        trans_interval = interval.Interval(noteStart=note_from, noteEnd=note_to)

        # Transpose the score
        transposed_score = score.transpose(trans_interval)

        # Convert back to ABC
        # music21's ABC export
        abc_handler = converter.subConverters.ConverterABC()
        transposed_abc = abc_handler.write(transposed_score, fmt='abc')

        return transposed_abc
    except Exception as e:
        print(f"[TRANSPOSE] music21 failed: {e}")
        raise


def transpose_abc_tune(abc_full: str, to_key: str) -> str:
    """
    Transpose a full ABC tune (with headers) to a new key

    Args:
        abc_full: Full ABC notation including headers
        to_key: Target key (e.g., 'Dmaj', 'G')

    Returns:
        Fully transposed ABC notation with updated K: header
    """
    lines = abc_full.split('\n')

    # Find the K: header to determine source key
    from_key = 'C'
    key_line_idx = None
    music_start_idx = 0

    for i, line in enumerate(lines):
        if line.startswith('K:'):
            from_key = line[2:].strip()
            key_line_idx = i
            music_start_idx = i + 1
            break

    if key_line_idx is None:
        # No K: header found, can't transpose
        return abc_full

    # Split into header and music
    header_lines = lines[:music_start_idx]
    music_lines = lines[music_start_idx:]

    # Update K: header
    header_lines[key_line_idx] = f'K: {to_key}'

    # Transpose music
    music_body = '\n'.join(music_lines)
    transposed_music = transpose_abc_music(music_body, from_key, to_key)

    # Recombine
    result = '\n'.join(header_lines) + '\n' + transposed_music

    return result


def get_average_pitch(abc_music: str) -> float:
    """
    Calculate the average pitch (in semitones) of notes in ABC notation

    Args:
        abc_music: ABC music notation (without headers)

    Returns:
        Average absolute semitone value
    """
    note_pattern = r'([_=\^]*)([A-Ga-g])([,\']*)(\d*/?\d*)'
    matches = re.findall(note_pattern, abc_music)

    if not matches:
        return 60.0  # Default to middle C if no notes found

    semitones = []
    for accidental, note, octave_markers, _ in matches:
        try:
            semitone = get_note_semitone(note, accidental[:1] if accidental else '', octave_markers)
            semitones.append(semitone)
        except:
            continue

    if not semitones:
        return 60.0

    return sum(semitones) / len(semitones)


def shift_octave(abc_music: str, octaves: int) -> str:
    """
    Shift all notes in ABC notation up or down by octaves

    Args:
        abc_music: ABC music notation
        octaves: Number of octaves to shift (positive = up, negative = down)

    Returns:
        Shifted ABC notation
    """
    if octaves == 0:
        return abc_music

    note_pattern = r'([_=\^]*)([A-Ga-g])([,\']*)(\d*/?\d*)'

    def shift_match(match):
        accidental = match.group(1) or ''
        note = match.group(2)
        octave_markers = match.group(3) or ''
        duration = match.group(4) or ''

        # Get current semitone
        current_semitone = get_note_semitone(note, accidental[:1] if accidental else '', octave_markers)

        # Shift by octaves
        new_semitone = current_semitone + (octaves * 12)

        # Convert back to ABC (preserve sharps/flats preference from accidental)
        prefer_sharps = '^' in accidental or accidental == ''
        new_note = semitone_to_abc_note(new_semitone, prefer_sharps)

        return new_note + duration

    return re.sub(note_pattern, shift_match, abc_music)


def smart_octave_correction(original_music: str, transposed_music: str, expected_interval: int) -> str:
    """
    Fix notes that are in the wrong octave by checking each note individually

    Args:
        original_music: Original ABC music
        transposed_music: Transposed ABC music (may have octave errors)
        expected_interval: Expected transposition interval in semitones

    Returns:
        Corrected ABC music
    """
    note_pattern = r'([_=\^]*)([A-Ga-g])([,\']*)(\d*/?\d*)'
    orig_matches = re.findall(note_pattern, original_music)
    trans_matches = re.findall(note_pattern, transposed_music)

    if len(orig_matches) != len(trans_matches):
        # Can't do note-by-note correction if counts don't match
        return transposed_music

    # Build corrected string by replacing notes
    def replace_notes(match):
        # This will be called for each note match in order
        replace_notes.counter = getattr(replace_notes, 'counter', -1) + 1
        i = replace_notes.counter

        if i >= len(orig_matches):
            return match.group(0)

        t_acc, t_note, t_oct, t_dur = trans_matches[i]
        o_acc, o_note, o_oct_orig, o_dur = orig_matches[i]

        o_pitch = get_note_semitone(o_note, o_acc[:1] if o_acc else '', o_oct_orig)
        t_pitch = get_note_semitone(t_note, t_acc[:1] if t_acc else '', t_oct)
        actual_diff = t_pitch - o_pitch

        # Check if this note is off by an octave from expected
        octave_error = round((actual_diff - expected_interval) / 12.0)

        if octave_error != 0:
            # This note needs octave correction
            corrected_pitch = t_pitch - (octave_error * 12)

            # Determine if we should use sharps
            prefer_sharps = '^' in t_acc or t_acc == ''
            corrected_note = semitone_to_abc_note(corrected_pitch, prefer_sharps)

            return corrected_note + t_dur
        else:
            # Note is correct, keep as is
            return match.group(0)

    # Reset counter
    replace_notes.counter = -1
    corrected = re.sub(note_pattern, replace_notes, transposed_music)

    return corrected


def correct_octave_register(original_abc: str, transposed_abc: str) -> str:
    """
    Correct the octave register of a transposed tune to match the original

    Compares note-by-note pitch differences to detect octave errors.
    The transposition interval should be consistent, but if there's an extra ~12 semitone
    offset across all notes, that indicates an octave error.

    Args:
        original_abc: Original ABC notation (full tune with headers)
        transposed_abc: Transposed ABC notation that may be in wrong octave

    Returns:
        Corrected ABC notation in the same register as original
    """
    # Extract music bodies (after K: header)
    def get_music_body(abc: str) -> str:
        lines = abc.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('K:'):
                return '\n'.join(lines[i+1:])
        return abc

    original_music = get_music_body(original_abc)
    transposed_music = get_music_body(transposed_abc)

    # Extract all notes from both
    note_pattern = r'([_=\^]*)([A-Ga-g])([,\']*)(\d*/?\d*)'
    orig_matches = re.findall(note_pattern, original_music)
    trans_matches = re.findall(note_pattern, transposed_music)

    if not orig_matches or not trans_matches:
        return transposed_abc

    # Calculate pitch differences for each corresponding note pair
    diffs = []
    for i in range(min(len(orig_matches), len(trans_matches))):
        orig_acc, orig_note, orig_oct, _ = orig_matches[i]
        trans_acc, trans_note, trans_oct, _ = trans_matches[i]

        try:
            orig_pitch = get_note_semitone(orig_note, orig_acc[:1] if orig_acc else '', orig_oct)
            trans_pitch = get_note_semitone(trans_note, trans_acc[:1] if trans_acc else '', trans_oct)
            diff = trans_pitch - orig_pitch
            diffs.append(diff)
        except:
            continue

    if not diffs:
        return transposed_abc

    # Calculate median difference (most common transposition interval)
    diffs.sort()
    median_diff = diffs[len(diffs) // 2]

    # Normalize all diffs to same octave as median (modulo 12)
    # This detects notes that are off by octaves
    normalized_diffs = []
    for d in diffs:
        # Find which multiple of 12 to add/subtract to get closest to median
        octave_offset = round((d - median_diff) / 12.0)
        normalized_diffs.append(d - (octave_offset * 12))

    # Check if there are significant deviations (notes in wrong octaves)
    # If most notes match median ±1 semitone, but some are off by ~12, those need fixing
    deviations = [abs(nd - median_diff) for nd in normalized_diffs]
    avg_deviation = sum(deviations) / len(deviations)

    if avg_deviation < 0.5:
        # All notes transposed consistently
        return transposed_abc

    print(f"[TRANSPOSE] Median transposition: {median_diff} semitones")
    print(f"[TRANSPOSE] Average deviation: {avg_deviation:.2f} semitones")
    print(f"[TRANSPOSE] Detected inconsistent octaves - attempting smart correction")

    # Fix notes that are off by octaves
    # Go through each note and check if it's ~12 semitones off from expected
    corrected_music = smart_octave_correction(original_music, transposed_music, median_diff)

    # Reconstruct full ABC
    lines = transposed_abc.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('K:'):
            header_lines = lines[:i+1]
            return '\n'.join(header_lines) + '\n' + corrected_music

    return transposed_abc
