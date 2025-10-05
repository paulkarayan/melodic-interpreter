"""
Harmony generation for Irish tunes
All functions take ABC string and return modified ABC string
"""
import re
from .abc_utils import parse_abc, rebuild_abc, get_bars


def apply_quartal_sparse(abc: str) -> str:
    """
    Add quartal harmony on beats 1 and 5
    Fourth intervals for modern sound

    Args:
        abc: Input ABC notation

    Returns:
        Modified ABC with sparse quartal harmony
    """
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    # Add fourths on e and B
    varied = re.sub(r'^e', '[EA]', bars[0])
    varied = re.sub(r'B', '[BE]', varied)

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_quartal_two(abc: str) -> str:
    """
    Two-note quartal fourths throughout
    Most anglo-friendly approach

    Args:
        abc: Input ABC notation

    Returns:
        Modified ABC with two-note quartal harmony
    """
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    varied = re.sub(r'e', '[EA]', bars[0])
    varied = re.sub(r'A', '[AD]', varied)

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_modal_drone(abc: str) -> str:
    """
    Static A-D drone underneath
    Emphasizes Dorian mode

    Args:
        abc: Input ABC notation

    Returns:
        Modified ABC with modal drone
    """
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    varied = '[AD]3 ' + bars[0]

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_diatonic_thirds(abc: str) -> str:
    """
    Diatonic thirds harmony
    Traditional approach

    Args:
        abc: Input ABC notation

    Returns:
        Modified ABC with diatonic thirds
    """
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    varied = re.sub(r'e([^a])', r'[ec]\1', bars[0])
    varied = re.sub(r'A', '[Ac]', varied)
    varied = re.sub(r'B', '[Bd]', varied)

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_open_fifths(abc: str) -> str:
    """
    Open fifths harmony
    Powerful, traditional sound

    Args:
        abc: Input ABC notation

    Returns:
        Modified ABC with open fifths
    """
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    varied = re.sub(r'A', '[AE]', bars[0])
    varied = re.sub(r'd', '[da]', varied)

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_beat_emphasis(abc: str) -> str:
    """
    Beat emphasis - harmony on strong beats only
    Works for any meter

    Args:
        abc: Input ABC notation

    Returns:
        Modified ABC with beat emphasis
    """
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    # In 6/8 jigs, emphasize beats 1 and 4 (strong beats)
    # Add fifths or fourths on first note and 4th note
    varied = re.sub(r'^([A-Ga-g])', r'[\1\1]', bars[0])  # Double first note for emphasis

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_jig_rhythm(abc: str) -> str:
    """
    Jig rhythm emphasis - beats 1, 3+4, 5+1
    Specific to 6/8 time signature

    Args:
        abc: Input ABC notation

    Returns:
        Modified ABC with jig rhythm emphasis
    """
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    # For jig: emphasize beat 1, beats 3+4 together, beats 5+1 together
    # eAA Bcd -> [EA]e AA [Bc]B cd
    varied = re.sub(r'^e', '[EA]', bars[0])  # Beat 1
    varied = re.sub(r'Bc', '[Bc]B', varied)  # Beats 3+4

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_chord_changes(abc: str) -> str:
    """
    Chord changes - I-III-IV progression
    Modal harmony with chord progressions

    Args:
        abc: Input ABC notation

    Returns:
        Modified ABC with chord changes
    """
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    # For A Dorian: I=Am [ACE], III=C [CEG], IV=Dm [DFA]
    # Apply I-III-IV progression
    varied = re.sub(r'^e', '[ACE]', bars[0])  # I: Am chord
    varied = re.sub(r'A', '[CEG]', varied)    # III: C chord
    varied = re.sub(r'B', '[DFA]', varied)    # IV: Dm chord

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_drone_pedal(abc: str) -> str:
    """
    Drone pedal - sustained root note underneath
    Most traditional Irish approach
    """
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    varied = 'A4 ' + bars[0]  # Sustained A underneath

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_parallel_thirds(abc: str) -> str:
    """
    Parallel thirds - traditional harmony
    """
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    # Add thirds above: e->g, A->c, B->d
    varied = re.sub(r'e([^a])', r'[eg]\1', bars[0])
    varied = re.sub(r'A', '[Ac]', varied)
    varied = re.sub(r'B', '[Bd]', varied)

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_parallel_sixths(abc: str) -> str:
    """
    Parallel sixths - traditional harmony
    """
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    # Add sixths above: e->c, A->f, B->g
    varied = re.sub(r'e([^a])', r'[ec]\1', bars[0])
    varied = re.sub(r'A', '[Af]', varied)
    varied = re.sub(r'B', '[Bg]', varied)

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_double_stops(abc: str) -> str:
    """
    Double stops - fiddle-style two-note harmonies
    """
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    # Fiddle double stops: mix thirds and fifths
    varied = re.sub(r'e([^a])', r'[eA]\1', bars[0])
    varied = re.sub(r'A', '[Ac]', varied)
    varied = re.sub(r'B', '[Bd]', varied)
    varied = re.sub(r'd', '[da]', varied)

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_bass_line(abc: str) -> str:
    """
    Walking bass line - I-III-IV progression
    """
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    # I-III-IV bass line: A, C, D,
    varied = 'A, ' + bars[0][:len(bars[0])//3] + ' C, ' + bars[0][len(bars[0])//3:2*len(bars[0])//3] + ' D, ' + bars[0][2*len(bars[0])//3:]

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_quartal_moving(abc: str) -> str:
    """
    Moving quartal harmony - parallel fourths following melody
    """
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    # Parallel fourths throughout
    varied = re.sub(r'e', '[eA]', bars[0])
    varied = re.sub(r'A', '[Ad]', varied)
    varied = re.sub(r'B', '[Be]', varied)
    varied = re.sub(r'c', '[cf]', varied)
    varied = re.sub(r'd', '[dg]', varied)

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_suspended_chords(abc: str) -> str:
    """
    Suspended chords - add 2nds and 4ths, avoid 3rds
    """
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    # Suspended voicings: root + 4th or root + 2nd
    varied = re.sub(r'^e', '[eAd]', bars[0])  # Asus4
    varied = re.sub(r'B', '[BeA]', varied)    # Asus2
    varied = re.sub(r'd', '[dAe]', varied)    # Dsus4

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_modal_mixture(abc: str) -> str:
    """
    Modal mixture - borrow from parallel modes
    """
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    # Mix Dorian with Aeolian (lower 7th occasionally)
    varied = re.sub(r'g', '_g', bars[0])  # Borrowed ♭7 from Aeolian

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_countermelody(abc: str) -> str:
    """
    Countermelody - independent melodic line
    """
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    # Simple contrary motion countermelody
    # When melody goes up, counter goes down
    varied = 'c2B2A2G2 | ' + bars[0]

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_simple_chord_changes(abc: str) -> str:
    """
    Simple chord changes - analyze melody to identify chords and add chord notes
    on chord changes with chord names above

    Returns ABC with:
    1. Chord notes (2-3 notes) replacing melody notes at chord changes
    2. Chord names as annotations above each change
    """
    headers, body = parse_abc(abc)

    # Extract key from headers
    key_match = re.search(r'K:([A-G][#b]?)(maj|min|m|dor|mix|lyd|phr|loc)?', headers)
    if not key_match:
        return abc  # Can't proceed without key

    key_root = key_match.group(1)
    mode = key_match.group(2) or ''

    # Define chord tones for common keys (simplified for anglo concertina)
    # Format: {note: (chord_name, [chord_notes])}
    chord_map = {
        'A': {
            'dor': {  # A Dorian (like Sliabh Russell)
                'A': ('Am', ['A', 'c', 'e']),
                'e': ('Am', ['A', 'c', 'e']),
                'c': ('C', ['C', 'E', 'G']),
                'E': ('C', ['C', 'E', 'G']),
                'G': ('C', ['C', 'E', 'G']),
                'd': ('Dm', ['D', 'F', 'A']),
                'D': ('Dm', ['D', 'F', 'A']),
                'F': ('Dm', ['D', 'F', 'A']),
                'B': ('G', ['G', 'B', 'd']),
                'g': ('G', ['G', 'B', 'd']),
            }
        },
        'D': {
            '': {  # D Major
                'D': ('D', ['D', '^F', 'A']),
                'd': ('D', ['D', '^F', 'A']),
                'A': ('A', ['A', '^C', 'E']),
                'a': ('A', ['A', '^C', 'E']),
                'G': ('G', ['G', 'B', 'D']),
                'g': ('G', ['G', 'B', 'D']),
                '^F': ('D', ['D', '^F', 'A']),
                '^f': ('D', ['D', '^F', 'A']),
            },
            'mix': {  # D Mixolydian
                'D': ('D', ['D', '^F', 'A']),
                'd': ('D', ['D', '^F', 'A']),
                'A': ('A', ['A', '^C', 'E']),
                'a': ('A', ['A', '^C', 'E']),
                'G': ('G', ['G', 'B', 'D']),
                'g': ('G', ['G', 'B', 'D']),
                'C': ('C', ['C', 'E', 'G']),
                'c': ('C', ['C', 'E', 'G']),
            }
        },
        'G': {
            '': {  # G Major
                'G': ('G', ['G', 'B', 'D']),
                'g': ('G', ['G', 'B', 'D']),
                'D': ('D', ['D', '^F', 'A']),
                'd': ('D', ['D', '^F', 'A']),
                'C': ('C', ['C', 'E', 'G']),
                'c': ('C', ['C', 'E', 'G']),
                'E': ('Em', ['E', 'G', 'B']),
                'e': ('Em', ['E', 'G', 'B']),
            }
        }
    }

    # Get chord map for this key
    chords = chord_map.get(key_root, {}).get(mode, chord_map.get(key_root, {}).get('', {}))
    if not chords:
        return abc  # Unsupported key

    # Process the body note by note
    result = []
    current_chord = None
    i = 0

    while i < len(body):
        char = body[i]

        # Check if this is a note (A-G or a-g, possibly with accidentals)
        note_match = re.match(r'([_=\^]*)([A-Ga-g])', body[i:])
        if note_match:
            accidental = note_match.group(1)
            note = note_match.group(2)
            full_note = accidental + note

            # Look up chord for this note
            chord_info = chords.get(full_note) or chords.get(note)

            if chord_info:
                chord_name, chord_notes = chord_info

                # Is this a chord change?
                if chord_name != current_chord:
                    # Add chord annotation and notes
                    result.append(f'"^{chord_name}"')
                    # Use 2-3 chord notes (anglo-friendly)
                    if len(chord_notes) >= 3:
                        result.append(f'[{chord_notes[0]}{chord_notes[1]}{chord_notes[2]}]')
                    elif len(chord_notes) == 2:
                        result.append(f'[{chord_notes[0]}{chord_notes[1]}]')
                    else:
                        result.append(f'{chord_notes[0]}')

                    current_chord = chord_name
                    i += len(note_match.group(0))
                    continue

            # Not a chord change, keep the note as-is
            result.append(full_note)
            i += len(note_match.group(0))
        else:
            # Not a note (bar line, rhythm, etc.)
            result.append(char)
            i += 1

    result_body = ''.join(result)
    return rebuild_abc(headers, result_body)


# Harmony function registry
HARMONY_FUNCTIONS = {
    # Traditional
    'drone_pedal': apply_drone_pedal,
    'parallel_thirds': apply_parallel_thirds,
    'parallel_sixths': apply_parallel_sixths,
    'diatonic_thirds': apply_diatonic_thirds,
    'open_fifths': apply_open_fifths,
    # Extended Traditional
    'double_stops': apply_double_stops,
    'bass_line': apply_bass_line,
    'modal_drone': apply_modal_drone,
    # Contemporary
    'quartal_sparse': apply_quartal_sparse,
    'quartal_two': apply_quartal_two,
    'quartal_moving': apply_quartal_moving,
    'suspended_chords': apply_suspended_chords,
    'modal_mixture': apply_modal_mixture,
    'countermelody': apply_countermelody,
    'beat_emphasis': apply_beat_emphasis,
    'jig_rhythm': apply_jig_rhythm,
    'chord_changes': apply_chord_changes,
    'simple_chord_changes': apply_simple_chord_changes,
}

HARMONY_DESCRIPTIONS = {
    # Traditional
    'drone_pedal': "Drone pedal - sustained root note underneath (most traditional)",
    'parallel_thirds': "Parallel thirds - traditional harmony a 3rd above",
    'parallel_sixths': "Parallel sixths - traditional harmony a 6th above",
    'diatonic_thirds': "Diatonic thirds - traditional approach with diatonic intervals",
    'open_fifths': "Open fifths - powerful, traditional sound",
    # Extended Traditional
    'double_stops': "Double stops - fiddle-style two-note harmonies",
    'bass_line': "Walking bass line - I-III-IV progression",
    'modal_drone': "Modal drone - static A-D pedal emphasizing Dorian mode",
    # Contemporary
    'quartal_sparse': "Quartal harmony on beats 1 and 5 - fourth intervals for modern sound",
    'quartal_two': "Two-note quartal fourths throughout - anglo-friendly approach",
    'quartal_moving': "Moving quartal - parallel fourths following melody",
    'suspended_chords': "Suspended chords - add 2nds and 4ths, avoid 3rds",
    'modal_mixture': "Modal mixture - borrow chords from parallel modes",
    'countermelody': "Countermelody - independent melodic line in contrary motion",
    'beat_emphasis': "Beat emphasis - harmony on strong beats only",
    'jig_rhythm': "Jig rhythm - emphasize beats 1, 3+4, 5+1 (6/8 specific)",
    'chord_changes': "Chord changes - modal chord progressions (Am, Dm, G)",
    'simple_chord_changes': "Simple chord changes - analyze melody and add concertina chord voicings (2-3 notes) with chord names when harmony changes",
}
