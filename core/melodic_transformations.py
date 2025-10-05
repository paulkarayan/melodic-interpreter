"""
Melodic Transformation Prompts for ABC Notation
Based on non-ornamental Irish traditional music variation techniques
"""

TRANSFORMATIONS = {

    # ========================================
    # MELODIC SUBSTITUTION TECHNIQUES
    # ========================================

    "neighbor_tone_substitution": """
Transform this ABC notation by applying neighbor tone substitution:
- Replace some notes with their upper or lower neighbors (±1 scale degree)
- Only substitute non-structural notes (avoid downbeats and cadential tones)
- Maintain the mode - use only notes from the original scale
- Keep the overall melodic contour recognizable
- Preserve phrase boundaries and measure structure
Output ONLY the transformed ABC notation, nothing else.""",

    "intervallic_expansion": """
Transform this ABC notation by expanding intervals:
- Widen some intervals between consecutive notes (e.g., 2nd → 3rd, 3rd → 4th)
- Maintain melodic direction (ascending stays ascending)
- Stay within the mode - no chromatic notes
- Preserve structural anchor tones (strong beat notes)
- Keep phrase length identical
Output ONLY the transformed ABC notation, nothing else.""",

    "intervallic_contraction": """
Transform this ABC notation by contracting intervals:
- Narrow some intervals between consecutive notes (e.g., 3rd → 2nd, 4th → 3rd)
- Maintain melodic direction (descending stays descending)
- Stay within the mode - no chromatic notes
- Preserve structural anchor tones
- Keep phrase length identical
Output ONLY the transformed ABC notation, nothing else.""",

    "scale_degree_substitution": """
Transform this ABC notation by substituting scale degrees:
- Replace notes with others of the same harmonic function
- Example: In D major, replace F# with A (both in D major triad)
- Maintain harmonic implications and chord tones on strong beats
- Stay within the mode
- Preserve phrase structure
Output ONLY the transformed ABC notation, nothing else.""",

    "arpeggio_scalar_swap": """
Transform this ABC notation by swapping between arpeggiated and scalar passages:
- Where you find arpeggios (chord tones), fill in with scalar motion
- Where you find scalar passages, simplify to arpeggios
- Maintain harmonic progression
- Keep the mode and phrase length
- Preserve rhythmic structure
Output ONLY the transformed ABC notation, nothing else.""",

    # ========================================
    # OCTAVE & REGISTER TECHNIQUES
    # ========================================

    "octave_displacement": """
Transform this ABC notation by displacing notes by octave:
- Move selected melodic fragments up or down one octave
- Maintain interval relationships within each fragment
- Create registral variety while preserving melodic identity
- Don't displace structural anchor tones on downbeats
- Keep within playable range (stay within 2 octaves total)
Output ONLY the transformed ABC notation, nothing else.""",

    "registral_redistribution": """
Transform this ABC notation by redistributing across registers:
- Alternate between high and low octaves for melodic phrases
- Create compound melody effect
- Maintain overall phrase contour and direction
- Preserve measure boundaries
- Keep within playable instrumental range
Output ONLY the transformed ABC notation, nothing else.""",

    # ========================================
    # NOTE DENSITY VARIATION
    # ========================================

    "note_addition_scalar": """
Transform this ABC notation by adding scalar notes:
- Fill in melodic leaps with scalar passing tones
- Example: C-E-G becomes C-D-E-F-G
- Maintain metric structure (subdivide existing rhythms proportionally)
- Stay within the mode
- Preserve phrase boundaries and cadences
Output ONLY the transformed ABC notation, nothing else.""",

    "note_subtraction": """
Transform this ABC notation by removing non-essential notes:
- Remove some passing tones and neighbor notes
- Simplify passages while preserving overall contour
- Example: C-D-E-D-C becomes C-E-C
- Keep structural anchor tones intact
- Maintain phrase length and measure boundaries
Output ONLY the transformed ABC notation, nothing else.""",

    "rhythmic_displacement_of_pitches": """
Transform this ABC notation by displacing pitches rhythmically:
- Move notes to different positions within the measure
- Maintain pitch content but shift rhythmic placement
- Preserve dance rhythm feel (don't disrupt downbeats excessively)
- Keep total measure duration identical
- Maintain phrase structure
Output ONLY the transformed ABC notation, nothing else.""",

    # ========================================
    # RHYTHMIC VARIATIONS
    # ========================================

    "subdivision": """
Transform this ABC notation by subdividing note durations:
- Replace longer notes with multiple shorter notes of the same pitch
- Quarter note → two eighth notes, eighth → two sixteenths
- Maintain overall phrase duration
- Keep dance music character and forward momentum
- Preserve measure boundaries
Output ONLY the transformed ABC notation, nothing else.""",

    "consolidation": """
Transform this ABC notation by consolidating note durations:
- Combine consecutive notes of same pitch into longer durations
- Two eighth notes → one quarter note
- Create more sustained, flowing lines
- Maintain phrase structure
- Preserve measure boundaries
Output ONLY the transformed ABC notation, nothing else.""",

    "make_busier": """
Transform this ABC notation by arpeggiating long held notes to make them busier:
- Replace longer notes with arpeggiated patterns of shorter notes
- Dotted quarter (3/8) → three eighth notes moving through nearby chord tones
- Quarter note (1/4) → two eighth notes moving stepwise or through chord tones
- Half note → four eighth notes creating melodic interest
- Use scale steps and chord tones appropriate to the mode
- Example in A Dorian: "A3" (dotted quarter) could become "AcA" or "ABA"
- Example: "d2" (half note) could become "dcBA" or "dede"
- Maintain overall phrase structure and measure boundaries
- Stay within the mode
Output ONLY the transformed ABC notation, nothing else.""",

    "tripleter": """
Transform this ABC notation by injecting triplets into longer notes:
- Replace quarter notes and longer durations with eighth-note triplets
- Use ABC triplet notation: (3ABC for triplet of A, B, C
- Quarter note → (3ABC where ABC are scale-appropriate notes
- Dotted quarter → (3ABC D where the triplet fills part of the duration
- Common in Irish music for adding rhythmic interest
- Example: "A2" becomes "(3ABA c" or "(3cBA G"
- Example: "d" becomes "(3dcB" (fills a quarter note with triplet)
- Use neighbor tones, passing tones, or chord tones for triplet notes
- Maintain phrase structure and stay within mode
- Preserve measure boundaries
Output ONLY the transformed ABC notation, nothing else.""",

    "dotted_rhythm_introduction": """
Transform this ABC notation by introducing dotted rhythms:
- Convert even rhythms to dotted patterns (long-short)
- Even eighths become dotted eighth-sixteenth
- Appropriate for hornpipe character or adding lilt
- Preserve total duration of each measure
- Maintain phrase boundaries
Output ONLY the transformed ABC notation, nothing else.""",

    "triplet_conversion": """
Transform this ABC notation by converting to triplets:
- Convert duple divisions to triple rhythms where appropriate
- Two eighth notes can become eighth-note triplet
- Works well in 6/8 jigs
- Maintain measure duration
- Preserve phrase structure
Output ONLY the transformed ABC notation, nothing else.""",

    "syncopation": """
Transform this ABC notation by adding syncopation:
- Place melodic emphasis on normally weak beats
- Create rhythmic tension while maintaining danceability
- Don't disrupt fundamental pulse too much
- Keep in character with dance genre
- Preserve measure and phrase boundaries
Output ONLY the transformed ABC notation, nothing else.""",

    "anacrusis_addition": """
Transform this ABC notation by adding pickup notes:
- Add anacrusis (pickup notes) to phrases that begin on downbeat
- Borrow duration from previous measure or phrase ending
- Creates forward momentum
- Maintain total phrase duration
- Preserve overall structure
Output ONLY the transformed ABC notation, nothing else.""",

    "anacrusis_removal": """
Transform this ABC notation by removing pickup notes:
- Remove anacrusis from phrases, start directly on downbeat
- Extend final note of phrase or add rest to compensate
- Changes relationship to downbeat
- Maintain total phrase duration
- Preserve overall structure
Output ONLY the transformed ABC notation, nothing else.""",

    "hemiola": """
Transform this ABC notation by creating hemiola patterns:
- Create 3-against-2 or 2-against-3 rhythmic patterns
- In 6/8: group six eighth notes as 3+3 instead of 2+2+2
- Temporary metric reinterpretation
- Maintain measure boundaries and total duration
- Works especially well in jigs
Output ONLY the transformed ABC notation, nothing else.""",

    # ========================================
    # CONTOUR TRANSFORMATIONS
    # ========================================

    "melodic_inversion": """
Transform this ABC notation by inverting the melodic contour:
- Upward intervals become downward, downward become upward
- Use tonal inversion (respect the scale/mode)
- Preserve rhythmic structure
- Maintain phrase boundaries
- Keep structural tones on strong beats when possible
Output ONLY the transformed ABC notation, nothing else.""",

    "retrograde": """
Transform this ABC notation by applying retrograde:
- Reverse the order of notes in selected phrases
- Can apply to pitch sequence, rhythm sequence, or both
- Maintain measure and phrase boundaries
- Ensure result stays within mode
- Keep structural coherence
Output ONLY the transformed ABC notation, nothing else.""",

    "contour_simplification": """
Transform this ABC notation by simplifying melodic contour:
- Remove melodic "zigzags" to create smoother lines
- Example: C-E-D-F-E-G becomes C-D-E-F-G (remove backtracking)
- Maintain general melodic direction
- Create more conjunct, stepwise motion
- Preserve phrase length and cadences
Output ONLY the transformed ABC notation, nothing else.""",

    "contour_elaboration": """
Transform this ABC notation by elaborating melodic contour:
- Add directional changes to create more complex contours
- Example: C-D-C-E-F-E-G (add neighbor-tone motion)
- Increase melodic interest
- Don't obscure underlying harmonic progression
- Maintain phrase boundaries
Output ONLY the transformed ABC notation, nothing else.""",

    # ========================================
    # PHRASE & STRUCTURAL VARIATIONS
    # ========================================

    "sequence_ascending": """
Transform this ABC notation by creating an ascending sequence:
- Take a melodic fragment and repeat it at progressively higher pitch levels
- Use tonal sequence (adjust intervals to stay in mode)
- Typically transpose up by 2nd or 3rd
- Maintain rhythmic pattern exactly
- Preserve phrase length
Output ONLY the transformed ABC notation, nothing else.""",

    "sequence_descending": """
Transform this ABC notation by creating a descending sequence:
- Take a melodic fragment and repeat it at progressively lower pitch levels
- Use tonal sequence (adjust intervals to stay in mode)
- Typically transpose down by 2nd or 3rd
- Maintain rhythmic pattern exactly
- Preserve phrase length
Output ONLY the transformed ABC notation, nothing else.""",

    "call_response_enhancement": """
Transform this ABC notation by enhancing call-response structure:
- Organize into question-answer phrase pairs
- First phrase poses "question" (half cadence or incomplete feeling)
- Second phrase "answers" (authentic cadence, resolution)
- Maintain 2-bar or 4-bar sub-phrase units
- Keep overall 8-bar structure
Output ONLY the transformed ABC notation, nothing else.""",

    "phrase_extension": """
Transform this ABC notation by extending phrases:
- Add extra beats or measures to create delayed resolution
- Can repeat cadential material or add interpolations
- Use sparingly - Irish dance music typically strict 8-bar
- Maintain structural coherence
- Create tension through extension
Output ONLY the transformed ABC notation, nothing else.""",

    "phrase_compression": """
Transform this ABC notation by compressing phrases:
- Remove some repeated notes or scalar passages
- Shorten phrases while keeping essential structural tones
- Create more urgent, condensed character
- Maintain phrase boundaries overall
- Preserve cadential structure
Output ONLY the transformed ABC notation, nothing else.""",

    "elision": """
Transform this ABC notation by eliding phrases:
- Overlap end of one phrase with beginning of next
- Last note of phrase 1 becomes first note of phrase 2
- Create seamless, connected flow
- Maintain total duration
- Preserve structural anchor points
Output ONLY the transformed ABC notation, nothing else.""",

    "motivic_fragmentation": """
Transform this ABC notation by fragmenting motives:
- Extract a small portion (2-4 notes) from the melody
- Use that fragment as building material for variation
- Repeat, sequence, or develop the fragment
- Common in B parts or developmental sections
- Maintain phrase structure and mode
Output ONLY the transformed ABC notation, nothing else.""",

    # ========================================
    # MODE-SPECIFIC VARIATIONS
    # ========================================

    "mixolydian_emphasis": """
Transform this ABC notation to emphasize Mixolydian character:
- If in major mode, add/emphasize the ♭7 to create Mixolydian feel
- Make the flattened 7th more prominent in cadences
- Avoid leading tone (♮7) resolutions
- Maintain tune structure
- Stay within Mixolydian mode (no additional accidentals)
Output ONLY the transformed ABC notation, nothing else.""",

    "dorian_emphasis": """
Transform this ABC notation to emphasize Dorian character:
- If in minor mode, add/emphasize the ♮6 to create Dorian feel
- Make the natural 6th more prominent
- Avoid ♭6 when possible
- Maintain tune structure
- Stay within Dorian mode (no additional accidentals)
Output ONLY the transformed ABC notation, nothing else.""",

    # ========================================
    # HYBRID/COMBINED VARIATIONS
    # ========================================

    "rhythmic_melodic_swap": """
Transform this ABC notation by swapping rhythmic and melodic emphasis:
- Where rhythm is active and melody simple, make melody more active
- Where melody is complex and rhythm simple, make rhythm more active
- Maintain overall phrase energy and character
- Preserve structural boundaries
- Stay within mode
Output ONLY the transformed ABC notation, nothing else.""",

    "contrast_enhancement": """
Transform this ABC notation by enhancing internal contrast:
- Make A and B sections more different from each other
- If A is stepwise, make B more disjunct (or vice versa)
- If A is rhythmically even, make B more syncopated
- Preserve tune identity
- Maintain structural integrity
Output ONLY the transformed ABC notation, nothing else.""",

    "density_gradient": """
Transform this ABC notation by creating a density gradient:
- Start sparse (fewer notes, longer durations)
- Gradually increase density (more notes, subdivisions)
- Or reverse: start dense, end sparse
- Maintain phrase boundaries
- Preserve structural tones
Output ONLY the transformed ABC notation, nothing else.""",

    "arch_contour": """
Transform this ABC notation by creating arch contour:
- Shape the melody to rise then fall (or fall then rise)
- Create clear melodic peak or valley point
- Maintain mode and harmonic structure
- Preserve phrase length
- Keep structural anchor tones
Output ONLY the transformed ABC notation, nothing else.""",

    # ========================================
    # GENRE-SPECIFIC VARIATIONS
    # ========================================

    "reel_variation": """
Transform this ABC notation with reel-specific variation:
- Maintain continuous driving eighth-note motion
- Keep forward momentum essential to reels
- Minimal rests or sustained notes
- Preserve the "reel" character and energy
- Stay in 4/4 or 2/2 meter
Output ONLY the transformed ABC notation, nothing else.""",

    "jig_variation": """
Transform this ABC notation with jig-specific variation:
- Emphasize lilting, bouncing 6/8 character
- Use triplet-based feel
- Create "hop" or "skip" quality
- Allow more rhythmic variety than reels
- Maintain 6/8 compound meter feel
Output ONLY the transformed ABC notation, nothing else.""",

    "hornpipe_variation": """
Transform this ABC notation with hornpipe-specific variation:
- Add or enhance characteristic dotted rhythms
- Create "swagger" or deliberate character
- More sustained notes than reels
- Strong downbeat emphasis
- Maintain 4/4 meter with hornpipe feel
Output ONLY the transformed ABC notation, nothing else.""",

    "slip_jig_variation": """
Transform this ABC notation with slip jig-specific variation:
- Maintain graceful, flowing 9/8 character
- Three groups of three eighth notes
- More elaborate than standard jigs
- Often melodically complex
- Preserve 9/8 meter structure
Output ONLY the transformed ABC notation, nothing else.""",

    # ========================================
    # CONSERVATIVE VARIATIONS (A section)
    # ========================================

    "minimal_variation": """
Transform this ABC notation with minimal variation (suitable for A sections):
- Make only subtle changes
- Preserve tune identity strongly
- Change 1-2 notes maximum per measure
- Keep rhythm mostly intact
- Maintain all structural elements
Output ONLY the transformed ABC notation, nothing else.""",

    "establishing_variation": """
Transform this ABC notation with establishing variation (first time through):
- Establish the tune clearly with minimal deviation
- Add just enough personality to show interpretation
- Keep very close to original
- Preserve all essential melodic features
- Maintain strict structure
Output ONLY the transformed ABC notation, nothing else.""",

    # ========================================
    # PROGRESSIVE VARIATIONS (B section)
    # ========================================

    "moderate_variation": """
Transform this ABC notation with moderate variation (suitable for B sections):
- More freedom than A section but still recognizable
- Can alter rhythm and melody simultaneously
- Change 3-4 notes per measure
- Add some rhythmic interest
- Maintain structural anchor points
Output ONLY the transformed ABC notation, nothing else.""",

    "creative_variation": """
Transform this ABC notation with creative variation (B section repeats):
- Maximum variation while maintaining identity
- Can substantially alter melody and rhythm
- Demonstrate musical creativity and skill
- Keep tune still recognizable
- Preserve mode, structure, and key cadential points
Output ONLY the transformed ABC notation, nothing else.""",

    # ========================================
    # STYLE-SPECIFIC VARIATIONS
    # ========================================

    "clare_style": """
Transform this ABC notation with Clare style characteristics:
- More ornamentation and complexity (but not grace notes - use note substitution)
- Driving, energetic feel
- Emphasis on melodic variation over strict rhythm
- Add some syncopation
- Maintain tune structure
Output ONLY the transformed ABC notation, nothing else.""",

    "donegal_style": """
Transform this ABC notation with Donegal style characteristics:
- Simpler, more direct melodic approach
- Strong rhythmic drive
- Less melodic elaboration
- Steady, driving character
- Maintain tune structure
Output ONLY the transformed ABC notation, nothing else.""",

    "sliabh_luachra_style": """
Transform this ABC notation with Sliabh Luachra style characteristics:
- Emphasis on slides and smooth connections (via pitch, not ornaments)
- Polka and sliding reel style
- Characteristic rhythmic lilt
- Smoother melodic contours
- Maintain tune structure and regional character
Output ONLY the transformed ABC notation, nothing else.""",
}


def get_all_transformation_names():
    """Return list of all transformation names."""
    return list(TRANSFORMATIONS.keys())


def get_random_transformations(count=5):
    """Return random transformation names."""
    import random
    return random.sample(list(TRANSFORMATIONS.keys()), min(count, len(TRANSFORMATIONS)))
