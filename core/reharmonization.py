"""
Programmatic Reharmonization using Music Theory
Analyzes ABC notation and suggests chord substitutions
"""

import re
from typing import List, Dict, Tuple, Set
from collections import defaultdict


# Note to MIDI number mapping
NOTE_TO_MIDI = {
    'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11,
    'c': 12, 'd': 14, 'e': 16, 'f': 17, 'g': 19, 'a': 21, 'b': 23,
}

# Chord formulas (intervals from root)
CHORD_FORMULAS = {
    'maj': [0, 4, 7],           # Major triad
    'min': [0, 3, 7],           # Minor triad
    'dim': [0, 3, 6],           # Diminished
    'aug': [0, 4, 8],           # Augmented
    'maj7': [0, 4, 7, 11],      # Major 7th
    'min7': [0, 3, 7, 10],      # Minor 7th
    '7': [0, 4, 7, 10],         # Dominant 7th
    'min7b5': [0, 3, 6, 10],    # Half-diminished
    'dim7': [0, 3, 6, 9],       # Diminished 7th
    '6': [0, 4, 7, 9],          # Major 6th
    'min6': [0, 3, 7, 9],       # Minor 6th
    'sus4': [0, 5, 7],          # Suspended 4th
    'sus2': [0, 2, 7],          # Suspended 2nd
}

# Common key signatures
KEY_SIGNATURES = {
    'C': [], 'G': ['F#'], 'D': ['F#', 'C#'], 'A': ['F#', 'C#', 'G#'],
    'E': ['F#', 'C#', 'G#', 'D#'], 'B': ['F#', 'C#', 'G#', 'D#', 'A#'],
    'F': ['Bb'], 'Bb': ['Bb', 'Eb'], 'Eb': ['Bb', 'Eb', 'Ab'],
    'Ab': ['Bb', 'Eb', 'Ab', 'Db'],
    'Am': [], 'Em': ['F#'], 'Bm': ['F#', 'C#'], 'F#m': ['F#', 'C#', 'G#'],
    'C#m': ['F#', 'C#', 'G#', 'D#'], 'Dm': ['Bb'], 'Gm': ['Bb', 'Eb'],
    'Cm': ['Bb', 'Eb', 'Ab'], 'Ador': ['F#'],  # A Dorian = G major key sig
}


def parse_abc_note(note_str: str) -> Tuple[int, int]:
    """Parse ABC note and return (midi_pitch_class, duration_eighths)"""
    # Remove accidentals and ornaments for now
    clean = re.sub(r'[~HLMOPSTuv\^_=]', '', note_str)

    # Extract base note
    base_match = re.match(r"([A-Ga-g])", clean)
    if not base_match:
        return None, 0

    base_note = base_match.group(1)

    # Get MIDI pitch class (0-11)
    if base_note in NOTE_TO_MIDI:
        pitch_class = NOTE_TO_MIDI[base_note] % 12
    else:
        return None, 0

    # Parse duration (simplified)
    duration = 1  # default eighth note
    if '/' in clean:
        duration = 0.5
    elif '2' in clean:
        duration = 2
    elif '3' in clean:
        duration = 3
    elif '4' in clean:
        duration = 4

    return pitch_class, duration


def extract_notes_from_bar(bar: str) -> List[int]:
    """Extract note pitch classes from a bar"""
    notes = []
    # Match notes (letter + optional accidental + optional duration)
    note_pattern = r'[\^_=]?[A-Ga-g][,\']?[0-9\/]*'
    matches = re.findall(note_pattern, bar)

    for match in matches:
        pitch_class, _ = parse_abc_note(match)
        if pitch_class is not None:
            notes.append(pitch_class)

    return notes


def find_chords_for_notes(notes: List[int], key_root: int) -> List[Dict]:
    """Find all chords that contain the given notes"""
    if not notes:
        return []

    note_set = set(notes)
    matching_chords = []

    # Try each root note (all 12 chromatic notes)
    for root in range(12):
        for chord_type, intervals in CHORD_FORMULAS.items():
            chord_tones = set((root + interval) % 12 for interval in intervals)

            # Check if all melody notes are in this chord
            if note_set.issubset(chord_tones):
                root_name = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'][root]
                chord_name = f"{root_name}{chord_type}" if chord_type != 'maj' else root_name

                # Calculate how well this chord fits the key
                distance_from_key = min(abs(root - key_root), 12 - abs(root - key_root))

                # Prefer chords in key (I, IV, V, vi, ii, iii)
                diatonic_scale = [key_root, (key_root + 2) % 12, (key_root + 4) % 12,
                                  (key_root + 5) % 12, (key_root + 7) % 12, (key_root + 9) % 12,
                                  (key_root + 11) % 12]
                in_key = root in diatonic_scale

                matching_chords.append({
                    'name': chord_name,
                    'root': root,
                    'type': chord_type,
                    'tones': sorted(chord_tones),
                    'distance_from_key': distance_from_key,
                    'in_key': in_key,
                    'coverage': len(note_set & chord_tones) / len(note_set),
                })

    # Sort by: in_key first, then coverage, then distance from key
    matching_chords.sort(key=lambda x: (not x['in_key'], -x['coverage'], x['distance_from_key']))

    return matching_chords


def get_key_root(key_str: str) -> int:
    """Get MIDI pitch class for key root"""
    # Handle keys like "Ador", "Gmaj", "Emin", "D", etc.
    key_match = re.match(r'([A-G][#b]?)', key_str)
    if not key_match:
        return 0  # Default to C

    key_letter = key_match.group(1)
    note_map = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

    root = note_map.get(key_letter[0], 0)
    if len(key_letter) > 1:
        if key_letter[1] == '#':
            root = (root + 1) % 12
        elif key_letter[1] == 'b':
            root = (root - 1) % 12

    return root


def reharmonize_abc(abc: str, num_alternatives: int = 5) -> Dict:
    """
    Analyze ABC and suggest chord substitutions
    Returns melody with chord annotations and alternative suggestions
    """
    # Extract key
    key_match = re.search(r'K:\s*([^\n]+)', abc)
    key = key_match.group(1).strip() if key_match else 'C'
    key_root = get_key_root(key)

    # Split into header and body
    lines = abc.split('\n')
    header_end = next((i for i, line in enumerate(lines) if line.startswith('K:')), -1)
    headers = '\n'.join(lines[:header_end + 1])
    body = '\n'.join(lines[header_end + 1:])

    # Split body into bars
    bars = re.split(r'[\|:\]]', body)
    bars = [b.strip() for b in bars if b.strip() and not b.strip().startswith('%')]

    # Analyze each bar
    bar_analyses = []
    for i, bar in enumerate(bars[:16]):  # Limit to first 16 bars
        notes = extract_notes_from_bar(bar)
        if not notes:
            continue

        # Find all possible chords
        all_chords = find_chords_for_notes(notes, key_root)

        # Get top alternatives (diverse set)
        alternatives = []
        seen_roots = set()

        for chord in all_chords[:num_alternatives * 3]:
            # Prefer diversity in root notes
            if len(alternatives) >= num_alternatives:
                break
            if chord['root'] not in seen_roots or len(alternatives) < 2:
                alternatives.append(chord)
                seen_roots.add(chord['root'])

        # Generate explanations
        for chord in alternatives:
            if chord['in_key']:
                chord['explanation'] = f"Diatonic to {key}"
            elif chord['type'] == '7':
                chord['explanation'] = "Secondary dominant"
            elif chord['type'] in ['maj7', 'min7']:
                chord['explanation'] = "Modal/jazz color"
            elif 'dim' in chord['type']:
                chord['explanation'] = "Passing/diminished"
            else:
                chord['explanation'] = "Modal substitution"

        bar_analyses.append({
            'bar_number': i + 1,
            'bar_content': bar,
            'notes': notes,
            'primary_chord': alternatives[0] if alternatives else None,
            'alternatives': alternatives[1:] if len(alternatives) > 1 else [],
        })

    # Create annotated ABC with primary chords
    annotated_body_lines = []
    current_bar_idx = 0

    for line in body.split('\n'):
        if not line.strip() or line.strip().startswith('%'):
            annotated_body_lines.append(line)
            continue

        # Add chord annotations to line
        annotated_line = line
        for analysis in bar_analyses:
            if current_bar_idx < len(bars) and analysis['bar_content'] in line:
                if analysis['primary_chord']:
                    chord_name = analysis['primary_chord']['name']
                    # Add chord annotation before the bar
                    annotated_line = annotated_line.replace(
                        analysis['bar_content'],
                        f'"{chord_name}"{analysis["bar_content"]}',
                        1
                    )
                current_bar_idx += 1

        annotated_body_lines.append(annotated_line)

    annotated_abc = headers + '\n' + '\n'.join(annotated_body_lines)

    return {
        'original_abc': abc,
        'annotated_abc': annotated_abc,
        'key': key,
        'bar_analyses': bar_analyses,
    }
