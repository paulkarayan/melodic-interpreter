"""
Anglo concertina playability validation
Checks for impossible note combinations on C/G 30-button Anglo
"""
from typing import List, Set, Tuple


# Impossible note pairs from ANGLO_CONSTRAINTS.md
IMPOSSIBLE_PAIRS = {
    ('F#', 'C'), ('F#', 'F'),
    ('Bb', 'B'), ('Bb', 'D'), ('Bb', 'G'), ('Bb', 'E'), ('Bb', 'A'),
    ('Eb', 'E'), ('Eb', 'G'), ('Eb', 'B'), ('Eb', 'D'), ('Eb', 'A'),
    ('C#', 'C'), ('C#', 'F'), ('C#', 'Bb'), ('C#', 'Eb'),
    ('G#', 'G'), ('Ab', 'A'), ('Db', 'D'),
}

# Normalize sharp/flat equivalents
NOTE_EQUIVALENTS = {
    'F#': 'F#', 'Gb': 'F#',
    'C#': 'C#', 'Db': 'C#',
    'G#': 'G#', 'Ab': 'G#',
    'A#': 'Bb', 'Bb': 'Bb',
    'D#': 'Eb', 'Eb': 'Eb',
}


def normalize_note(note: str) -> str:
    """
    Normalize note names (handle sharps/flats)

    Args:
        note: Note name (e.g., 'F#', 'Gb', 'A')

    Returns:
        Normalized note name
    """
    # Remove octave markers
    clean = note.replace("'", "").replace(",", "")

    # Normalize to uppercase
    if len(clean) > 0:
        clean = clean[0].upper() + clean[1:]

    # Apply equivalents
    return NOTE_EQUIVALENTS.get(clean, clean)


def extract_notes_from_chord(chord_notation: str) -> List[str]:
    """
    Extract individual notes from ABC chord notation [ABC]

    Args:
        chord_notation: ABC chord like "[EA]" or "[Adf]"

    Returns:
        List of note names
    """
    # Remove brackets
    clean = chord_notation.strip('[]')

    # Extract note letters (with sharps/flats)
    notes = []
    i = 0
    while i < len(clean):
        note = clean[i]
        # Check for sharp/flat
        if i + 1 < len(clean) and clean[i + 1] in ['^', '_', '=']:
            note += '#' if clean[i + 1] == '^' else 'b'
            i += 2
        else:
            i += 1
        notes.append(note)

    return notes


def validate_chord(notes: List[str]) -> Tuple[bool, List[Tuple[str, str]]]:
    """
    Check if a chord is playable on Anglo concertina

    Args:
        notes: List of note names

    Returns:
        (is_playable, list_of_impossible_pairs)
    """
    normalized = [normalize_note(n) for n in notes]
    impossible = []

    # Check all pairs
    for i in range(len(normalized)):
        for j in range(i + 1, len(normalized)):
            pair = tuple(sorted([normalized[i], normalized[j]]))
            reverse_pair = tuple(sorted([normalized[j], normalized[i]]))

            if pair in IMPOSSIBLE_PAIRS or reverse_pair in IMPOSSIBLE_PAIRS:
                impossible.append((notes[i], notes[j]))

    return len(impossible) == 0, impossible


def validate_abc_playability(abc_string: str) -> dict:
    """
    Validate entire ABC notation for Anglo playability

    Args:
        abc_string: Full ABC notation

    Returns:
        Dict with validation results
    """
    import re

    # Find all chords [...]
    chords = re.findall(r'\[[A-Ga-g^_=,\'\d]+\]', abc_string)

    results = {
        'is_playable': True,
        'total_chords': len(chords),
        'unplayable_chords': [],
        'warnings': []
    }

    for chord in chords:
        notes = extract_notes_from_chord(chord)
        is_playable, impossible_pairs = validate_chord(notes)

        if not is_playable:
            results['is_playable'] = False
            results['unplayable_chords'].append({
                'chord': chord,
                'notes': notes,
                'impossible_pairs': impossible_pairs
            })

    return results


# TODO: Implement suggest_playable_alternative()
# TODO: Implement full button layout simulation
