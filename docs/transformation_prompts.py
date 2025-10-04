"""
Transformation Prompts for LLM-based Style Variations
These prompts guide an LLM to reinterpret Irish tunes in different musical styles
"""

TRANSFORMATION_PROMPTS = {
    "drone_minimalist": {
        "name": "Drone Minimalist (Ó Raghallaigh-style)",
        "description": "Stretch the melody across a shifting drone; let notes ring into silence. Focus on texture, bow pressure, and harmonic overtones.",
        "prompt": """
You are transforming an Irish traditional tune into a **drone minimalist** interpretation
inspired by Caoimhín Ó Raghallaigh.

INSTRUCTIONS:
1. Stretch the melody across a shifting drone (A-D or E-A pedal)
2. Let notes ring into silence - add rests and sustained tones
3. Focus on texture and harmonic overtones
4. Space and resonance become part of the rhythm
5. Slow the tempo to 30-50% of original
6. Use sparse harmony - only essential notes
7. Output as ABC notation with:
   - Extended note durations (4, 8, 16 beats)
   - Drone notes in lower octave [AD]16 or similar
   - Long rests between phrases (z4, z8)

ABC INPUT:
{abc_notation}

Generate the drone minimalist variation in ABC notation:
""",
    },

    "groove_fusion": {
        "name": "Groove Fusion (the olllam-style)",
        "description": "Keep the tune's contour but anchor it in a deep, syncopated groove. Layer bass and drums under modal harmony.",
        "prompt": """
You are transforming an Irish traditional tune into a **groove fusion** interpretation
inspired by the olllam.

INSTRUCTIONS:
1. Keep the melodic contour recognizable
2. Anchor it in a deep, syncopated groove
3. Add bass line suggestions in ABC (low octave notes)
4. Use modal harmony - quartal chords, suspended voicings
5. Weave subtle improvisation between phrases
6. Add dynamic markings and rhythmic emphasis
7. Maintain danceable pulse but with unexpected accents

ABC INPUT:
{abc_notation}

Generate the groove fusion variation in ABC notation:
""",
    },

    "ambient_chamber": {
        "name": "Ambient Chamber (Gloaming-style)",
        "description": "Slow the melody, widen phrasing, pair with piano or strings. Use long reverb tails and counterlines.",
        "prompt": """
You are transforming an Irish traditional tune into an **ambient chamber** interpretation
inspired by The Gloaming.

INSTRUCTIONS:
1. Slow the melody significantly (60-70% of original tempo)
2. Widen phrasing - let phrases breathe
3. Add piano/string counterlines in harmony
4. Use long reverb tails - sustained notes and overlaps
5. Turn dance rhythm into emotional atmosphere
6. Add dynamics: crescendo, diminuendo
7. Use rich harmonic voicings - thirds, fourths, fifths

ABC INPUT:
{abc_notation}

Generate the ambient chamber variation in ABC notation:
""",
    },

    "jazz_improv": {
        "name": "Jazz-Improv Trad (Notify / McSherry)",
        "description": "Treat the melody as a theme for improvisation. Shift between time signatures, reharmonize cadences.",
        "prompt": """
You are transforming an Irish traditional tune into a **jazz-improv trad** interpretation
inspired by Notify and John McSherry.

INSTRUCTIONS:
1. Treat the melody as a theme for improvisation
2. Shift between 5/4 and 6/8 (or 7/8 and 4/4 for reels)
3. Reharmonize key cadences with jazz voicings
4. Add chromatic passing tones and approach notes
5. Create modal vamps over which melody floats
6. Add short exploratory solo sections (4-8 bars)
7. Use bebop-influenced phrasing

ABC INPUT:
{abc_notation}

Generate the jazz-improv variation in ABC notation:
""",
    },

    "electro_trad": {
        "name": "Electro-Trad Texture (Córas-style)",
        "description": "Feed the tune through looping and delay; layer organic samples and evolving drones.",
        "prompt": """
You are transforming an Irish traditional tune into an **electro-trad texture** interpretation
inspired by Córas.

INSTRUCTIONS:
1. Feed melody through looping and delay - repeat short motifs
2. Layer organic samples (suggest in notation as repeated fragments)
3. Add evolving drones underneath
4. Keep ornamentation human but stretch time and space
5. Use electronics-inspired notation: repeated patterns, phase shifts
6. Build texture gradually through layering
7. Add ambient noise suggestions (whistle, breath tones)

ABC INPUT:
{abc_notation}

Generate the electro-trad variation in ABC notation:
""",
    },

    "post_rock_build": {
        "name": "Post-Rock Build",
        "description": "Start sparse with solo melody + drone. Gradually build texture over 60-90 seconds to full climax, then decay.",
        "prompt": """
You are transforming an Irish traditional tune into a **post-rock build** interpretation.

INSTRUCTIONS:
1. Start with solo melodic voice + light ambient drone
2. Over ~60-90 seconds, gradually introduce:
   - Harmonic pads (sustained chords)
   - Rhythmic pulse (soft percussion suggestions)
   - Layered texture
3. Use crescendo and modulation
4. Build to climax with full texture / interplay
5. Then decay back to sparse melody + drone
6. Mark dynamic sections clearly in ABC

ABC INPUT:
{abc_notation}

Generate the post-rock build variation in ABC notation with section markers:
""",
    },

    "dark_drone": {
        "name": "Dark Drone",
        "description": "Overlay melody above a deep, slowly evolving drone. Use sustained tones, microtonal shifts, occasional harmonic 'cracks'.",
        "prompt": """
You are transforming an Irish traditional tune into a **dark drone** interpretation.

INSTRUCTIONS:
1. Overlay melody above a deep, slowly evolving drone (low register)
2. Use sustained, overlapping tones
3. Add microtonal shifts (suggest with approach notes)
4. Create occasional harmonic "cracks" or dissonances
5. Keep dynamics minimal
6. Emphasize resonance and overtones
7. Slow temporal unfolding - stretch time

ABC INPUT:
{abc_notation}

Generate the dark drone variation in ABC notation:
""",
    },

    "traditional_session": {
        "name": "Traditional Session Style",
        "description": "Stay within session-standard variation techniques: neighbor tones, diatonic substitution, rhythmic grouping.",
        "prompt": """
You are creating a **traditional session-style** variation of an Irish tune.

INSTRUCTIONS:
1. Stay strictly within the mode (no chromatic notes)
2. Use only traditional variation techniques:
   - Neighbor tones (replace note with upper/lower neighbor)
   - Diatonic substitution (swap notes within mode)
   - Rhythmic grouping changes
   - Ending variations
3. Preserve phrase structure
4. Keep it recognizable to session musicians
5. Could have been played 100 years ago

ABC INPUT:
{abc_notation}

Generate the traditional variation in ABC notation:
""",
    },

    "modal_reharmonization": {
        "name": "Modal Reharmonization",
        "description": "Keep melody intact but reharmonize with modal interchange, secondary dominants, suspended voicings.",
        "prompt": """
You are creating a **modal reharmonization** of an Irish tune.

INSTRUCTIONS:
1. Keep the original melody mostly intact
2. Reharmonize with:
   - Modal interchange (borrow from parallel modes)
   - Secondary dominants (brief tonicizations)
   - Suspended harmonies (add tension/release)
   - Quartal voicings where appropriate
3. Add harmonic interest without obscuring melody
4. Use jazz-influenced chord progressions

ABC INPUT:
{abc_notation}

Generate the reharmonized variation in ABC notation with chord symbols:
""",
    },

    "rhythmic_displacement": {
        "name": "Rhythmic Displacement",
        "description": "Displace the melody rhythmically - shift accents, change meter, create metric modulation.",
        "prompt": """
You are creating a **rhythmic displacement** variation of an Irish tune.

INSTRUCTIONS:
1. Keep melodic contour but displace rhythmically
2. Shift accents to create new pulse
3. Consider changing meter (6/8 to 5/4, 4/4 to 7/8, etc.)
4. Create metric modulation if appropriate
5. Use syncopation and off-beat accents
6. Maintain energy and drive

ABC INPUT:
{abc_notation}

Generate the rhythmically displaced variation in ABC notation:
""",
    },

    "octave_exploration": {
        "name": "Octave Exploration",
        "description": "Move phrases between octaves, create wide intervallic leaps, explore register contrast.",
        "prompt": """
You are creating an **octave exploration** variation of an Irish tune.

INSTRUCTIONS:
1. Move phrases between octaves strategically
2. Create wide intervallic leaps
3. Explore register contrast (high vs low)
4. Use octave displacement to create drama
5. Maintain melodic integrity despite register changes
6. Add octave doubling where effective

ABC INPUT:
{abc_notation}

Generate the octave exploration variation in ABC notation:
""",
    },
}


def get_prompt(style: str, abc_notation: str) -> str:
    """
    Get the formatted prompt for a specific style

    Args:
        style: One of the keys in TRANSFORMATION_PROMPTS
        abc_notation: The ABC notation to transform

    Returns:
        Formatted prompt string ready for LLM
    """
    if style not in TRANSFORMATION_PROMPTS:
        raise ValueError(f"Unknown style: {style}. Available: {list(TRANSFORMATION_PROMPTS.keys())}")

    return TRANSFORMATION_PROMPTS[style]["prompt"].format(abc_notation=abc_notation)


def get_all_styles() -> list:
    """Get list of all available transformation styles"""
    return [
        {
            "key": key,
            "name": value["name"],
            "description": value["description"]
        }
        for key, value in TRANSFORMATION_PROMPTS.items()
    ]
