"""
Melodic variations for Irish tunes using LLM
All variation generation uses Claude API for musical understanding
"""
import os
import anthropic
from typing import Optional, Tuple, List

# Check for Anthropic API key
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if ANTHROPIC_API_KEY:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    LLM_AVAILABLE = True
else:
    LLM_AVAILABLE = False

# Melodic variation prompts
MELODIC_PROMPTS = {
    'neighbor': """Apply neighbor tone substitution to this ABC notation:
- Replace sustained notes with upper or lower neighbor embellishments
- Keep the melodic contour recognizable
- Maintain the rhythmic feel of a jig (6/8)
- Use traditional Irish ornamentation patterns
Return ONLY the modified ABC notation, preserving all headers.""",

    'phrase_ending': """Vary the cadential patterns (phrase endings) in this ABC notation:
- Modify how phrases resolve at bar endings
- Keep strong cadence points intact
- Use traditional Irish ending variations
- Maintain the modal character
Return ONLY the modified ABC notation, preserving all headers.""",

    'note_consolidation': """Consolidate repeated notes into longer durations:
- Combine successive identical notes (e.g., AA → A2)
- Simplify melodic runs where appropriate
- Maintain rhythmic integrity for jig feel
- Keep phrase structure clear
Return ONLY the modified ABC notation, preserving all headers.""",

    'arpeggiation': """Replace scalar passages with arpeggios:
- Identify scale runs and substitute with chord-tone arpeggios
- Use diatonic harmony (A Dorian mode)
- Keep the melodic contour similar
- Maintain jig rhythm (6/8)
Return ONLY the modified ABC notation, preserving all headers.""",

    'motivic_sequence': """Apply motivic sequencing:
- Identify melodic fragments (2-3 notes)
- Repeat them at different pitch levels (transpose up/down a 2nd or 3rd)
- Maintain the overall phrase structure
- Keep traditional Irish character
Return ONLY the modified ABC notation, preserving all headers.""",

    'contour_simplification': """Simplify melodic contour by removing zigzags:
- Smooth out melodic direction changes
- Remove unnecessary neighbor tones
- Create clearer melodic lines
- Maintain rhythmic integrity
Return ONLY the modified ABC notation, preserving all headers.""",

    'octave_displacement': """Move phrases to different octaves:
- Shift selected phrases up or down an octave
- Maintain playability
- Keep modal character
- Preserve rhythmic feel
Return ONLY the modified ABC notation, preserving all headers.""",

    'chromatic': """Add chromatic passing tones (bebop-influenced):
- Insert chromatic notes between scale degrees
- Use approach notes to target tones
- Keep jig rhythm intact
- Don't overuse - stay tasteful
Return ONLY the modified ABC notation, preserving all headers.""",

    'intervallic_expansion': """Widen melodic intervals:
- Change 2nds to 3rds, 3rds to 4ths, etc.
- Maintain melodic contour
- Keep phrase structure
- Preserve modal character
Return ONLY the modified ABC notation, preserving all headers.""",

    'rhythmic_consolidation': """Consolidate rhythm to fewer, longer notes:
- Reduce rhythmic density
- Use longer note values
- Simplify without losing character
- Maintain 6/8 jig feel
Return ONLY the modified ABC notation, preserving all headers.""",

    'cross_rhythm': """Add cross-rhythm patterns (3-against-2):
- Introduce polyrhythmic patterns
- Use triplet groupings: (3ABC
- Keep traditional Irish feel
- Don't completely obscure the tune
Return ONLY the modified ABC notation, preserving all headers.""",

    'rhythmic_shift': """Apply rhythmic displacement:
- Shift note positions within the measure
- Add syncopation or anticipation
- Maintain melodic contour
- Keep jig character recognizable
Return ONLY the modified ABC notation, preserving all headers.""",

    'simplification': """Reduce to essential notes:
- Remove ornamental figures
- Keep only structural melody notes
- Simplify rhythmic patterns
- Maintain phrase shape
Return ONLY the modified ABC notation, preserving all headers."""
}

MELODIC_DESCRIPTIONS = {
    'neighbor': "Neighbor tone substitution - traditional variation technique",
    'phrase_ending': "Phrase ending variation - vary cadential patterns",
    'note_consolidation': "Note consolidation - combine repeated notes into longer durations",
    'arpeggiation': "Arpeggiation - replace scales with chord tone arpeggios",
    'motivic_sequence': "Motivic sequence - repeat fragments at different pitch levels",
    'contour_simplification': "Contour simplification - smooth out melodic zigzags",
    'octave_displacement': "Octave displacement - move phrases up/down an octave",
    'chromatic': "Chromatic passing tones - bebop-influenced approach",
    'intervallic_expansion': "Intervallic expansion - widen intervals between notes",
    'rhythmic_consolidation': "Rhythmic consolidation - fewer, longer notes",
    'cross_rhythm': "Cross-rhythm - 3-against-2 polyrhythmic patterns",
    'rhythmic_shift': "Rhythmic displacement - shift note positions",
    'simplification': "Simplification - reduce to essential notes",
}


def _diff_abc_bars(original_abc: str, modified_abc: str, expected_changes: int) -> List[dict]:
    """
    Diff two ABC strings and return list of changed bars

    Returns:
        List of dicts with keys: bar_number, original, modified
    """
    try:
        # Extract just the music (skip headers)
        def get_music_lines(abc_text):
            lines = abc_text.strip().split('\n')
            music_start = 0
            for i, line in enumerate(lines):
                if line.startswith('K:'):
                    music_start = i + 1
                    break
            return '\n'.join(lines[music_start:])

        original_music = get_music_lines(original_abc)
        modified_music = get_music_lines(modified_abc)

        # Split into bars (simple split on |)
        original_bars = [b.strip() for b in original_music.split('|') if b.strip()]
        modified_bars = [b.strip() for b in modified_music.split('|') if b.strip()]

        changed = []
        for i, (orig, mod) in enumerate(zip(original_bars, modified_bars)):
            # Normalize for comparison (remove extra spaces, etc)
            orig_norm = ' '.join(orig.split())
            mod_norm = ' '.join(mod.split())

            if orig_norm != mod_norm:
                changed.append({
                    'bar_number': i + 1,
                    'original': orig,
                    'modified': mod
                })

        # Return up to expected_changes bars
        return changed[:expected_changes] if expected_changes else changed

    except Exception as e:
        print(f"[DIFF ERROR] {e}")
        return []


def apply_melodic_multiple(
    abc: str,
    variation_type: str,
    target_lick: Optional[str] = None,
    num_spots: Optional[int] = None
) -> Tuple[str, str, List]:
    """
    Apply melodic variation using LLM to 2-5 spots (or specific lick)

    Args:
        abc: Input ABC notation
        variation_type: Type of variation
        target_lick: Optional specific lick to target (e.g., "eAABcd")
        num_spots: Optional number of spots (2-5). If None, randomly chosen.

    Returns:
        (modified_abc, description, changed_bars_info)
    """
    if not LLM_AVAILABLE:
        return (abc, "LLM not available - set ANTHROPIC_API_KEY", [])

    if variation_type not in MELODIC_PROMPTS:
        return (abc, f"Unknown variation type: {variation_type}", [])

    # Build prompt
    if target_lick:
        instruction = f"""Given this ABC notation:

{abc}

{MELODIC_PROMPTS[variation_type]}

IMPORTANT: Only modify the specific lick pattern "{target_lick}" wherever it appears.
Leave all other parts of the tune unchanged.
Return ONLY the modified ABC notation with the same headers (X:, T:, M:, L:, R:, K:)."""
    else:
        if num_spots is None:
            import random
            num_spots = random.randint(2, 5)

        instruction = f"""Given this ABC notation:

{abc}

{MELODIC_PROMPTS[variation_type]}

IMPORTANT: Apply this variation to {num_spots} different locations in the tune.
Choose musically appropriate spots (varied bars, not all in one section).
Return ONLY the modified ABC notation with the same headers (X:, T:, M:, L:, R:, K:)."""

    print(f"[MELODIC LLM] Generating {variation_type} variation...")
    print(f"[MELODIC LLM] Target lick: {target_lick or 'none'}, spots: {num_spots if not target_lick else 'all occurrences'}")

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": instruction
            }]
        )

        modified_abc = message.content[0].text.strip()

        # Clean up markdown code blocks if present
        if modified_abc.startswith('```'):
            lines = modified_abc.split('\n')
            modified_abc = '\n'.join(lines[1:-1]) if len(lines) > 2 else modified_abc

        # Description
        if target_lick:
            description = f'Applied to lick "{target_lick}"'
        else:
            description = f'Applied to {num_spots} different locations'

        print(f"[MELODIC LLM] Successfully generated variation")

        # Diff original vs modified to find changed bars
        changed_bars = _diff_abc_bars(abc, modified_abc, num_spots)

        return (modified_abc, description, changed_bars)

    except Exception as e:
        print(f"[MELODIC LLM ERROR] {e}")
        return (abc, f"LLM error: {str(e)}", [])
