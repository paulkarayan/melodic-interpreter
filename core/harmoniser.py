"""
Anglo Concertina Harmoniser
Hybrid approach: Programmatic chord analysis + AI voicing generation
"""
import re
import os
from typing import Dict, List, Tuple, Optional

# Check for Anthropic API key
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if ANTHROPIC_API_KEY:
    import anthropic
    LLM_AVAILABLE = True
else:
    LLM_AVAILABLE = False


def detect_mode_and_key(abc: str) -> Tuple[str, str]:
    """
    Extract key signature and detect mode from ABC notation

    Returns:
        (key, mode) e.g., ("Ador", "Dorian"), ("DMix", "Mixolydian")
    """
    # Extract K: header
    key_match = re.search(r'K:\s*([^\n]+)', abc)
    if not key_match:
        return ("D", "Ionian")  # Default

    key_sig = key_match.group(1).strip()

    # Detect mode from key signature
    if 'dor' in key_sig.lower():
        mode = "Dorian"
    elif 'mix' in key_sig.lower():
        mode = "Mixolydian"
    elif 'aeo' in key_sig.lower() or 'm' in key_sig:
        mode = "Aeolian"
    else:
        mode = "Ionian"

    return (key_sig, mode)


def detect_tune_type(abc: str) -> str:
    """Extract tune type (jig, reel, etc.) from R: header"""
    type_match = re.search(r'R:\s*([^\n]+)', abc)
    if not type_match:
        return "reel"  # Default

    tune_type = type_match.group(1).strip().lower()

    if 'jig' in tune_type:
        return "jig"
    elif 'reel' in tune_type:
        return "reel"
    elif 'hornpipe' in tune_type:
        return "hornpipe"
    elif 'polka' in tune_type:
        return "polka"
    elif 'slide' in tune_type:
        return "slide"
    elif 'waltz' in tune_type:
        return "waltz"
    else:
        return "reel"


def analyze_chord_changes(abc: str, harmonic_rhythm: str, tune_type: str, mode: str) -> List[Dict]:
    """
    Programmatically determine WHERE chord changes should occur

    Returns list of chord change points with bar numbers and suggested chords
    """
    # Extract music body (after K: header)
    lines = abc.split('\n')
    music_start = 0
    for i, line in enumerate(lines):
        if line.startswith('K:'):
            music_start = i + 1
            break

    music_body = '\n'.join(lines[music_start:])

    # Split into bars
    bars = [b.strip() for b in music_body.split('|') if b.strip() and not re.match(r'^[\s:12]*$', b)]

    # Determine chord change frequency based on harmonic rhythm and tune type
    if harmonic_rhythm == "drone":
        change_frequency = 999  # Never change (stay on tonic)
    elif harmonic_rhythm == "sparse":
        change_frequency = 4  # Every 4 bars
    elif harmonic_rhythm == "moderate":
        change_frequency = 2  # Every 2 bars
    else:  # active
        change_frequency = 1  # Every bar at phrase points

    # Adjust for tune type (jigs and reels prefer longer chord durations)
    if tune_type in ["jig", "reel"] and harmonic_rhythm != "drone":
        change_frequency = max(2, change_frequency)  # Minimum 2 bars

    # Detect phrase boundaries (typically every 4 or 8 bars in Irish music)
    phrase_boundaries = []
    for i in range(0, len(bars), 4):
        phrase_boundaries.append(i)

    # Generate chord change points
    chord_changes = []
    current_bar = 0

    while current_bar < len(bars):
        # Determine chord for this section
        # This is simplified - AI will refine based on actual melody
        if mode == "Mixolydian":
            # Alternate between I and bVII
            chord = "I" if (current_bar // change_frequency) % 2 == 0 else "bVII"
        elif mode == "Dorian":
            # Alternate between i and IV
            chord = "i" if (current_bar // change_frequency) % 2 == 0 else "IV"
        elif mode == "Aeolian":
            # i -> bVII -> bVI pattern
            position = (current_bar // change_frequency) % 3
            chord = ["i", "bVII", "bVI"][position]
        else:  # Ionian
            # I -> IV -> V pattern
            position = (current_bar // change_frequency) % 3
            chord = ["I", "IV", "V"][position]

        chord_changes.append({
            'bar_number': current_bar + 1,
            'bar_content': bars[current_bar] if current_bar < len(bars) else '',
            'suggested_chord': chord,
            'duration_bars': min(change_frequency, len(bars) - current_bar)
        })

        current_bar += change_frequency

    return chord_changes


def generate_harmony_with_ai(
    abc: str,
    harmonic_rhythm: str,
    layers: List[str],
    chord_changes: List[Dict],
    key: str,
    mode: str,
    tune_type: str
) -> Dict:
    """
    Use AI to generate actual harmony voicings based on programmatic chord analysis
    """
    if not LLM_AVAILABLE:
        raise Exception("Anthropic API not available")

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # Build layer description
    layer_desc = []
    if 'power_chords' in layers:
        layer_desc.append("Power chords (root + 5th, modal-safe)")
    if 'thirds' in layers:
        layer_desc.append("Parallel thirds")
    if 'bass' in layers:
        layer_desc.append("Bass notes on chord changes only")
    if 'chords' in layers:
        layer_desc.append("Full triads at phrase points")

    layers_text = ", ".join(layer_desc)

    # Build chord change summary
    chord_summary = "\n".join([
        f"Bar {cc['bar_number']}: {cc['suggested_chord']} chord for {cc['duration_bars']} bars"
        for cc in chord_changes[:6]  # Show first 6 for context
    ])

    prompt = f"""You are adding Anglo concertina harmony to this Irish traditional {tune_type} in {key} ({mode} mode).

Original ABC:
{abc}

CHORD CHANGE ANALYSIS (programmatically determined):
{chord_summary}

HARMONY REQUIREMENTS:
1. Harmonic Rhythm: {harmonic_rhythm}
2. Layers to include: {layers_text}
3. Mode: {mode} - CRITICAL modal harmony rules:
   - Mixolydian: Use bVII (NOT V7), progression I → bVII → I
   - Dorian: Use major IV (NOT minor iv), progression i → IV → i
   - Aeolian: Use bVII and bVI, progression i → bVII → bVI → bVII
   - Ionian: Standard I → IV → V

ANGLO CONCERTINA CONSTRAINTS:
- Maximum chord duration: 1-2 beats (bellows change limitation)
- Use staccato articulation for chords
- Bass notes only on chord changes (NOT every downbeat)
- For {tune_type}s: {"Bass on chord changes, chord buttons on beats 3 and 6" if tune_type == "jig" else "Bass on chord changes, chord buttons on offbeats"}
- Power chords (omit 3rd) for modal ambiguity
- Keep melody clearly audible - sparse accompaniment

OUTPUT FORMAT:
Generate TWO separate ABC notations:

1. **Harmony only** - Just the harmony parts (bass notes, chords, thirds) as standalone ABC
2. **Combined** - Single staff with melody + inline harmony in playable range:
   - ADD CHORD NAME ANNOTATIONS above melody: |:"Am"eAA Bcd|"G"eaf ged|
   - Add harmony notes INLINE using square brackets: [Ae] means melody e with harmony A below it
   - Use SAME REGISTER as anglo concertina (treble clef, melody on top)
   - Harmony notes should be 3rd, 5th, or octave below melody
   - CRITICAL DENSITY RULES based on harmonic_rhythm = "{harmonic_rhythm}":
     * "drone": Add harmony bass note ONLY on first note of tune, then leave melody alone
     * "sparse": Add harmony ONLY every 4 bars on beat 1
     * "moderate": Add harmony every 2 bars on beat 1
     * "active": Add harmony on beats 1 and 4 in jigs (beats 1 and 3 in reels)
   - Keep all headers (X:, T:, R:, M:, L:, K:) from original

Examples:

DRONE (harmony only on first note):
|:"Am"[Ae]AA Bcd|eaf ged|edB cBA|BAG ABd:|

SPARSE (harmony every 4 bars on beat 1):
|:"Am"[Ae]AA Bcd|eaf ged|edB cBA|BAG ABd|
"Am"eAA Bcd|eaf ged|edB cBA|1 BAG A3:|2 BAG ABd||

ACTIVE (harmony on beats 1 and 4):
|:"Am"[Ae]AA [Bc]cd|"Am"[Ae]af [Gg]ed|"G"[Ge]dB [Cc]BA|"G"[GB]AG [AA]Bd:|

Return as JSON:
{{
  "harmony_only": "ABC notation with just harmony",
  "combined": "ABC notation single staff with inline harmony and chord annotations",
  "description": "Brief description of harmony approach used",
  "analysis": "2-3 sentences explaining which chords were chosen and why"
}}

CRITICAL: Return ONLY valid JSON, nothing else."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=3000,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    response_text = message.content[0].text.strip()

    # Clean up markdown if present
    if response_text.startswith('```json'):
        response_text = response_text.replace('```json', '').replace('```', '').strip()
    elif response_text.startswith('```'):
        response_text = response_text.replace('```', '').strip()

    # Parse JSON response
    import json
    try:
        result = json.loads(response_text)
    except json.JSONDecodeError as je:
        print(f"[ERROR] JSON Parse Error: {je}")
        print(f"[ERROR] Response text:\n{response_text[:500]}...")
        raise Exception(f'Invalid JSON from AI: {str(je)}')

    return result


def harmonise_abc(
    abc: str,
    harmonic_rhythm: str = "sparse",
    layers: List[str] = None
) -> Dict:
    """
    Main harmonisation function - hybrid approach

    Args:
        abc: Original ABC notation
        harmonic_rhythm: "drone", "sparse", "moderate", or "active"
        layers: List of layer names: ["power_chords", "thirds", "bass", "chords"]

    Returns:
        Dict with melody_only, harmony_only, combined, description, analysis
    """
    if layers is None:
        layers = ["bass"]  # Default to bass only

    # Step 1: Detect mode and key
    key, mode = detect_mode_and_key(abc)

    # Step 2: Detect tune type
    tune_type = detect_tune_type(abc)

    # Step 3: Programmatically determine chord change points
    chord_changes = analyze_chord_changes(abc, harmonic_rhythm, tune_type, mode)

    # Step 4: Use AI to generate voicings based on constraints
    result = generate_harmony_with_ai(
        abc, harmonic_rhythm, layers, chord_changes, key, mode, tune_type
    )

    # Add original melody for reference
    result['melody_only'] = abc

    return result
