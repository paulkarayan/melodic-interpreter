"""
Repetition Detection for ABC Notation
Identifies repeated measures and phrases in Irish traditional music
"""
import re
from typing import List, Dict, Tuple


def extract_measures(abc: str) -> List[str]:
    """Extract individual measures from ABC notation (normalized for comparison)"""
    # Get music body (after K: header)
    lines = abc.split('\n')
    music_start = 0
    for i, line in enumerate(lines):
        if line.startswith('K:'):
            music_start = i + 1
            break

    music_body = '\n'.join(lines[music_start:])

    # Split by bar lines, clean up
    measures = []
    for bar in music_body.split('|'):
        # Remove repeat markers, endings, whitespace
        clean_bar = re.sub(r'[:|12\s]', '', bar.strip())
        if clean_bar and not re.match(r'^[\s:12]*$', clean_bar):
            measures.append(clean_bar)

    return measures


def extract_measures_with_durations(abc: str) -> List[str]:
    """Extract individual measures preserving durations and note content"""
    # Get music body (after K: header)
    lines = abc.split('\n')
    music_start = 0
    for i, line in enumerate(lines):
        if line.startswith('K:'):
            music_start = i + 1
            break

    music_body = '\n'.join(lines[music_start:])

    # Split by bar lines, preserve content but remove repeat markers and endings
    measures = []
    for bar in music_body.split('|'):
        # Remove only repeat markers (:), endings (1, 2 at start), and extra whitespace
        # But preserve duration numbers that come after notes
        clean_bar = bar.strip()
        # Remove leading : and endings like "1" or "2" at the start
        clean_bar = re.sub(r'^[:\d]+', '', clean_bar)
        # Remove trailing :
        clean_bar = re.sub(r':+$', '', clean_bar)
        # Remove internal whitespace
        clean_bar = clean_bar.replace(' ', '')

        if clean_bar:
            measures.append(clean_bar)

    return measures


def normalize_measure(measure: str) -> str:
    """Normalize a measure for comparison (remove octave markers, etc.)"""
    # Remove octave markers (commas and apostrophes)
    normalized = measure.replace(',', '').replace("'", '')
    # Lowercase for comparison
    normalized = normalized.lower()
    return normalized


def find_repeated_measures(abc: str, min_occurrences: int = 2) -> Dict[str, List[int]]:
    """
    Find measures that repeat in the tune

    Returns:
        Dict mapping normalized measure content to list of bar indices where it appears
    """
    measures = extract_measures(abc)

    # Track occurrences
    measure_map = {}
    for i, measure in enumerate(measures):
        normalized = normalize_measure(measure)
        if normalized not in measure_map:
            measure_map[normalized] = []
        measure_map[normalized].append(i)

    # Filter to only repeated measures
    repeated = {
        measure: indices
        for measure, indices in measure_map.items()
        if len(indices) >= min_occurrences
    }

    return repeated


def find_repeated_phrases(abc: str, phrase_length: int = 2, min_occurrences: int = 2) -> List[Dict]:
    """
    Find repeated phrases (sequences of measures)

    Args:
        abc: ABC notation string
        phrase_length: Number of measures in a phrase (default 2)
        min_occurrences: Minimum times phrase must repeat (default 2)

    Returns:
        List of dicts with 'phrase', 'length', 'occurrences' (list of starting indices)
    """
    # Get normalized measures for comparison
    measures = extract_measures(abc)
    # Get measures with durations for display
    measures_with_durations = extract_measures_with_durations(abc)

    # Generate all phrases of given length
    phrase_map = {}
    for i in range(len(measures) - phrase_length + 1):
        phrase = tuple(normalize_measure(m) for m in measures[i:i+phrase_length])
        if phrase not in phrase_map:
            phrase_map[phrase] = []
        phrase_map[phrase].append(i)

    # Filter to repeated phrases
    repeated_phrases = []
    for phrase, indices in phrase_map.items():
        if len(indices) >= min_occurrences:
            # Use measures_with_durations for original_text to preserve note durations
            repeated_phrases.append({
                'phrase': '|'.join(phrase),
                'length': phrase_length,
                'occurrences': indices,
                'original_text': '|'.join(measures_with_durations[indices[0]:indices[0]+phrase_length])
            })

    # Sort by number of occurrences (most repeated first)
    repeated_phrases.sort(key=lambda x: len(x['occurrences']), reverse=True)

    return repeated_phrases


def detect_repetition(abc: str) -> Dict:
    """
    Main function to detect all types of repetition

    Returns dict with:
        - repeated_measures: Dict of measure content -> indices
        - repeated_phrases_2bar: List of 2-bar repeated phrases
        - repeated_phrases_4bar: List of 4-bar repeated phrases
        - summary: Human-readable summary
    """
    repeated_measures = find_repeated_measures(abc)
    repeated_2bar = find_repeated_phrases(abc, phrase_length=2)
    repeated_4bar = find_repeated_phrases(abc, phrase_length=4)

    # Generate summary
    summary_parts = []

    if repeated_measures:
        summary_parts.append(
            f"Found {len(repeated_measures)} repeated measures"
        )

    if repeated_2bar:
        top_2bar = repeated_2bar[0]
        summary_parts.append(
            f"Most repeated 2-bar phrase appears {len(top_2bar['occurrences'])} times "
            f"(bars {', '.join(str(i+1) for i in top_2bar['occurrences'])})"
        )

    if repeated_4bar:
        top_4bar = repeated_4bar[0]
        summary_parts.append(
            f"Found {len(repeated_4bar)} repeated 4-bar phrases"
        )

    summary = '. '.join(summary_parts) if summary_parts else "No clear repetition detected"

    return {
        'repeated_measures': repeated_measures,
        'repeated_phrases_2bar': repeated_2bar,
        'repeated_phrases_4bar': repeated_4bar,
        'summary': summary,
        'has_repetition': bool(repeated_measures or repeated_2bar or repeated_4bar)
    }


def get_target_licks(abc: str) -> List[str]:
    """
    Get the actual lick strings to target for variation

    Returns list of lick strings (ABC notation segments)
    """
    result = detect_repetition(abc)

    licks = []

    # Prefer 2-bar phrases if available
    if result['repeated_phrases_2bar']:
        for phrase in result['repeated_phrases_2bar'][:3]:  # Top 3
            licks.append(phrase['original_text'])

    # Otherwise use single measures
    elif result['repeated_measures']:
        measures = extract_measures(abc)
        for measure_content, indices in list(result['repeated_measures'].items())[:3]:
            # Get original (non-normalized) version
            licks.append(measures[indices[0]])

    return licks
