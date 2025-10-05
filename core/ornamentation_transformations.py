"""
Ornamentation Transformation Prompts for ABC Notation
Based on Irish traditional music ornamentation practices

These prompts add or modify ornamentation while preserving melodic identity and rhythmic integrity.
Follows the principle: ornaments are primarily rhythmic articulations, not melodic alterations.

Usage:
    from abc_ornamentation_prompts import ORNAMENTATION_TRANSFORMATIONS
    
    # Select by name
    prompt = ORNAMENTATION_TRANSFORMATIONS['cuts_on_downbeats']
    
    # Random selection
    import random
    prompt = random.choice(list(ORNAMENTATION_TRANSFORMATIONS.values()))
    
    # Get ornamentation name
    name = random.choice(list(ORNAMENTATION_TRANSFORMATIONS.keys()))
    prompt = ORNAMENTATION_TRANSFORMATIONS[name]
"""

ORNAMENTATION_TRANSFORMATIONS = {
    
    # ========================================
    # BASIC ORNAMENT TYPES
    # ========================================
    
    "cuts_on_downbeats": """
Transform this ABC notation by adding cuts (upper grace notes) on downbeats:
- Add quick upper neighbor grace notes on beats 1 and 3 (in 4/4) or beat 1 (in 6/8)
- Execute as rapidly as possible - these are percussive articulations, not melodic notes
- Cut first and second-finger notes with third finger; third-finger notes with fourth
- Use to emphasize strong beats and create rhythmic drive
- Keep crisp and distinct without breaking rhythmic flow
- In ABC notation, represent cuts as grace notes: {G}A for cutting A with upper neighbor
Output the transformed ABC notation with cuts added.
""",

    "taps_for_grounding": """
Transform this ABC notation by adding taps (lower grace notes):
- Add quick lower neighbor grace notes for subtle rhythmic emphasis
- More subtle than cuts - use to ground the melody
- Place on strong beats and at phrase beginnings
- Execute as hammer-on style articulation (quickly tapping finger onto string/hole)
- Between second and third notes of identical pitch on whistle/flute
- In ABC notation, represent as lower grace notes: {F}G for tapping G with lower neighbor
Output the transformed ABC notation with taps added.
""",

    "long_rolls_jig_placement": """
Transform this ABC notation by adding long rolls in jig-appropriate positions:
- Structure: main note – cut (above) – main note – tap (below) – main note
- **Critical:** Think as THREE notes, not five - hold first note long, add percussive grace notes
- Place on dotted quarter notes in jigs
- Place on quarter note followed by eighth of same pitch
- Place on three eighths where first and third are identical (EDE becomes roll on E)
- Takes time value of dotted quarter note
- In ABC notation: Use explicit grace note syntax like {B}A{G}A for a roll on A (cut above, main, tap below, main)
- DO NOT use ~ shorthand - always write out the full grace note pattern
Output the transformed ABC notation with long rolls in traditional jig positions.
""",

    "short_rolls_reel_placement": """
Transform this ABC notation by adding short rolls in reel-appropriate positions:
- Condensed roll omitting first main note: cut – main – tap – main
- Fits into crotchet (quarter note) duration
- More common in reels than jigs
- Same articulation principle: percussive grace notes, not melodic
- Place on quarter notes and at phrase beginnings
- In ABC notation: {B}A{G}A represents short roll on A (cut above, main, tap below, main)
- DO NOT use ~ shorthand - always write out the full grace note pattern
Output the transformed ABC notation with short rolls for reels.
""",

    "triplets_characteristic": """
Transform this ABC notation by adding characteristic Irish triplets:
- Three notes in space of one beat
- Irish timing: first two notes faster, third slightly longer (while maintaining overall timing)
- Can be ascending, descending, or identical pitch
- Single-note triplets create "stutter" on long notes
- Place on quarter notes and longer durations
- In ABC notation: (3ABC or (3AAA for triplet patterns
Output the transformed ABC notation with Irish-style triplets.
""",

    "slides_melodic": """
Transform this ABC notation by adding slides (glissando):
- Smooth glide from one note to another
- Upward slides: start half-tone lower and slide up to melody note
- Downward slides (modern): start above and slide down
- More melodic than rhythmic - common in slow airs
- Frequently used on tin whistle and flute
- In ABC notation: can represent with grace note approach or special notation
Output the transformed ABC notation with slides added.
""",

    "crans_low_notes": """
Transform this ABC notation by adding crans on low notes:
- Series of 2-4 cuts without taps (from uilleann piping tradition)
- Creates distinctive "stuttering warble" characteristic of pipes
- Use when no lower note available for traditional roll
- Most commonly on low D or other bottom register notes
- Rhythm: "dah diggi-dah"
- On whistle/flute: use 2-finger crans (EF# fingers) or 3-finger crans (EF#G fingers)
Output the transformed ABC notation with crans on appropriate low notes.
""",

    "bounces_casadh": """
Transform this ABC notation by adding bounces (casadh - "twisting"):
- Two grace notes before main note
- First grace at pitch of main note, second at lower pitch
- Best suited for flute and whistle
- Creates percussive "twist" effect
- Use sparingly for special emphasis
- Means "twisting" in Irish
Output the transformed ABC notation with bounce ornaments.
""",

    # ========================================
    # INSTRUMENT-SPECIFIC ORNAMENTS
    # ========================================
    
    "fiddle_bowed_triplets": """
Transform this ABC notation by adding fiddle-style bowed triplets:
- Execute with "jiggle of index finger" or "flick of wrist"
- Tommy Peoples' scratchy, rhythmic style widely imitated
- Three-note groups with characteristic bowing articulation
- More rhythmic than melodic - drives the beat
- Common in Donegal style (called "trebles")
- Place on quarter notes and in phrase emphasis points
Output the transformed ABC notation with bowed triplet ornaments (note: fiddle-specific).
""",

    "concertina_phantom_button": """
Transform this ABC notation by adding concertina phantom button/slap roll:
- Timing of bellows change plus finger position creates percussive cut
- "The hardest easy thing" - provides "free lunch" ornamentation
- Works better on the pull (draw)
- Finger strikes button during bellows reversal without sounding
- Creates cut-like effect without actual note
- Unique to Anglo concertina technique
Output the transformed ABC notation with phantom button ornaments marked.
""",

    "concertina_bellows_shake": """
Transform this ABC notation by adding concertina bellows shake effects:
- Rapid bellows tremolo on sustained notes
- Creates vibrato or tremolo effect
- Use on long notes in airs or at phrase endings
- Rhythmic shake can drive the beat
- Anglo concertina specific technique
- Mark in notation where bellows articulation should occur
Output the transformed ABC notation with bellows shake ornaments.
""",

    "accordion_bellows_pulse": """
Transform this ABC notation by adding accordion bellows pulses:
- Sharp bellows articulation mimics bowing
- Place on strong beats for emphasis
- Creates percussive accent without pitch change
- Direction changes on strong beats preferred
- Both button and piano accordion technique
- Marks rhythmic structure clearly
Output the transformed ABC notation with bellows pulse articulations.
""",

    "whistle_flute_tonguing": """
Transform this ABC notation with whistle/flute tonguing patterns:
- Tongue second and third notes of each group in jigs (-TK -TK pattern)
- Some players use "all T's" pattern
- Creates cuts and strikes through articulation
- Different from fingered ornaments
- Essential for defining notes and rhythm
- Mark tonguing patterns in appropriate positions
Output the transformed ABC notation with tonguing articulations marked.
""",

    "whistle_breath_ornaments": """
Transform this ABC notation with breath-based ornaments for whistle:
- Breathing becomes part of phrasing and rhythm
- Breath marks at natural phrase divisions
- Vibrato through finger oscillation in slow airs
- Strategic breath placement enhances musical flow
- Avoid breaking rhythmic momentum
- Mark breath points that serve musical phrasing
Output the transformed ABC notation with breath ornament markings.
""",

    "pipes_regulator_style": """
Transform this ABC notation adding uilleann pipes regulator-style ornaments:
- Origin of many traditional ornaments
- Staccato ("tight") vs. legato ("open") articulation
- Crans originated where rolls aren't possible on lower notes
- Continuous airflow requires different articulation
- Rich ornamentation tradition that influenced all Irish instruments
- Mark pipe-style ornamentation in appropriate contexts
Output the transformed ABC notation with pipes-style ornaments.
""",

    # ========================================
    # RHYTHMIC PLACEMENT STRATEGIES
    # ========================================
    
    "ornament_strong_beats_only": """
Transform this ABC notation by placing ornaments on strong beats only:
- Add cuts, rolls, or triplets on beats 1 and 3 (4/4) or beat 1 (6/8)
- Leave weak beats unornamented for clarity
- Creates clear rhythmic structure
- Enhances danceability and drive
- Serves the pulse without cluttering
- Most conservative ornamentation approach
Output the transformed ABC notation with strong-beat ornaments only.
""",

    "ornament_phrase_beginnings": """
Transform this ABC notation by ornamenting phrase beginnings:
- Add ornaments (cuts, rolls, triplets) at start of each phrase
- Emphasizes phrase structure and creates lift
- First note of 2-bar or 4-bar units
- Helps dancers and listeners feel structure
- Don't ornament every phrase beginning - vary the pattern
- Conservative but effective placement
Output the transformed ABC notation with phrase-beginning ornaments.
""",

    "ornament_cadence_points": """
Transform this ABC notation by ornamenting cadence points:
- Add rolls, triplets, or slides at phrase endings
- Emphasizes resolution and structural punctuation
- Particularly effective on penultimate or final notes
- Creates sense of arrival and completion
- Can elaborate final cadence more than internal cadences
- Traditional and widely accepted placement
Output the transformed ABC notation with cadential ornaments.
""",

    "ornament_long_notes_only": """
Transform this ABC notation by ornamenting long notes only:
- Add rolls, triplets, or slides on half notes, dotted quarters, whole notes
- Leave shorter note values (eighths, sixteenths) unornamented
- Allows fast passages to remain clear
- Long notes "want" ornamentation to maintain interest
- Creates breathing room in the ornamentation pattern
- Particularly suitable for beginners
Output the transformed ABC notation with long-note ornaments only.
""",

    "alternating_ornament_pattern": """
Transform this ABC notation with alternating ornament placement:
- Ornament on first repeat of phrase, leave plain on second (or vice versa)
- Creates variation between repetitions
- Question-answer effect: plain phrase then ornamented response
- Builds interest through contrast
- Traditional approach to variation
- Don't ornament same spots on every repeat
Output the transformed ABC notation with alternating ornamentation.
""",

    # ========================================
    # DENSITY AND INTENSITY LEVELS
    # ========================================
    
    "minimal_sparse_ornaments": """
Transform this ABC notation with minimal, sparse ornamentation:
- Add only 2-4 ornaments per 8-bar phrase
- Focus on strong beats and cadence points only
- "Less is more" philosophy
- Suitable for first time through tune
- East Galway/East Clare style approach
- Ornaments enhance, never dominate
Output the transformed ABC notation with minimal ornamentation.
""",

    "moderate_tasteful_ornaments": """
Transform this ABC notation with moderate, tasteful ornamentation:
- Add ornaments on approximately 50% of suitable positions
- Balance ornamented and plain notes
- Vary ornament types (cuts, rolls, triplets)
- Maintain clarity while adding interest
- Suitable for second or third repetition
- Traditional session-appropriate level
Output the transformed ABC notation with moderate ornamentation.
""",

    "dense_elaborate_ornaments": """
Transform this ABC notation with dense, elaborate ornamentation:
- Ornament most suitable positions (70-80% coverage)
- Use variety of ornament types
- Sligo style approach - highly decorated
- Maintain rhythmic clarity despite density
- Only for experienced players
- Suitable for performance or final repetition
Output the transformed ABC notation with elaborate ornamentation.
""",

    "progressive_density_build": """
Transform this ABC notation with progressive ornament density:
- Start very sparse (first A section)
- Add moderate ornaments (second A section)
- Increase to dense (first B section)
- Maximum decoration (second B section)
- Creates arc of intensity through tune
- Traditional variation approach
Output the transformed ABC notation with progressive ornamentation density.
""",

    # ========================================
    # REGIONAL STYLE APPROACHES
    # ========================================
    
    "sligo_style_ornaments": """
Transform this ABC notation with Sligo-style ornamentation:
- Fast, highly ornamented with infectious swing
- Abundant rolls and bowed triplets (if fiddle)
- Accent on back-beat of reels
- Dense but flowing ornamentation
- Use variety of ornament types
- Rhythmic drive through decoration
- Masters: Michael Coleman, James Morrison, Matt Molloy, Kevin Burke
Output the transformed ABC notation with Sligo-style ornaments.
""",

    "east_clare_galway_minimal": """
Transform this ABC notation with East Clare/East Galway minimal style:
- Slower pace, lyrical, deeply soulful
- LESS ornamentation - "less is more" philosophy
- Long notes and legato phrasing
- Martin Hayes approach: forego flashy ornaments for tone and dynamics
- Restraint and emotional depth over technical display
- Ornaments serve expression, not display
- Masters: Paddy Canny, Mike Rafferty, Martin Hayes, Mary MacNamara
Output the transformed ABC notation with East Clare/Galway minimal ornaments.
""",

    "donegal_aggressive_ornaments": """
Transform this ABC notation with Donegal-style ornamentation:
- Fast, driving rhythm with aggressive attack
- Bowed triplets (trebles) instead of rolls
- Minimal but powerful ornamentation
- Short, separate articulation (staccato feel)
- Unswung, even note spacing
- Double-stops for emphasis (if applicable)
- Masters: John Doherty, Tommy Peoples, Mairéad Ní Mhaonaigh
Output the transformed ABC notation with Donegal-style ornaments.
""",

    "west_clare_rich_ornaments": """
Transform this ABC notation with West Clare rich ornamentation:
- Generous rolls and grace notes at moderate tempo
- Flowing rhythm with rich decoration
- Concertina and fiddle ornament vocabulary
- Ornament-rich but tasteful
- Maintains danceability despite decoration
- Balanced between sparse and excessive
- Masters: Willie Clancy, Elizabeth Crotty, Noel Hill, Junior Crehan
Output the transformed ABC notation with West Clare ornaments.
""",

    "sliabh_luachra_rhythmic": """
Transform this ABC notation with Sliabh Luachra rhythmic ornamentation:
- Highly rhythmic with off-beat pulse (especially polkas)
- Mixture of slurred and single articulations
- Infectious bounce and earthy quality
- Ornaments drive the dance rhythm
- Polkas and slides dominate repertoire
- Rhythmic punch balancing smoothness and accent
- Masters: Pádraig O'Keeffe, Julia Clifford, Denis Murphy, Jackie Daly
Output the transformed ABC notation with Sliabh Luachra ornaments.
""",

    # ========================================
    # TUNE TYPE SPECIFIC
    # ========================================
    
    "jig_ornament_patterns": """
Transform this ABC notation with jig-specific ornamentation:
- Long rolls on dotted quarter notes (primary placement)
- Bouncy, lilting feel - "JIG-i-ty JIG-i-ty"
- Emphasis on first and fourth eighth notes
- Triplet groupings with characteristic timing
- Tonguing pattern (whistle): -TK -TK on each group
- Morrison's Jig style: "can't be done without rolls"
Output the transformed ABC notation with jig ornaments.
""",

    "reel_ornament_patterns": """
Transform this ABC notation with reel-specific ornamentation:
- Short rolls more common than long rolls
- Four beats per measure - "double decker" feel
- Emphasis on first and third beats
- More fluid, less formulaic than jig ornaments
- Accent notes at phrase beginnings and before breathing pauses
- Driving feel maintained through ornamentation
Output the transformed ABC notation with reel ornaments.
""",

    "slow_air_ornaments": """
Transform this ABC notation with slow air ornamentation:
- Extensive ornamentation with subtle tempo freedom
- Slides, vibrato, and expressive rubato allowed
- Grace notes and runs serve emotional expression
- Free tempo allows more melodic ornamentation
- Can be more elaborate than dance tunes
- Ornamentation serves expression rather than rhythmic drive
Output the transformed ABC notation with slow air ornaments.
""",

    "hornpipe_dotted_ornaments": """
Transform this ABC notation with hornpipe-appropriate ornaments:
- Ornaments enhance characteristic dotted rhythms
- Deliberate, swagger-like feel
- More sustained approach than reels
- Strong downbeat emphasis with ornamental accents
- Ornaments reinforce the "roll" or "lilt" of hornpipe
- 4/4 meter with distinctive swing
Output the transformed ABC notation with hornpipe ornaments.
""",

    "polka_driving_ornaments": """
Transform this ABC notation with polka-appropriate ornaments:
- Strong rhythmic drive emphasized through ornaments
- 2/4 meter with characteristic bounce
- Ornaments on strong beats primarily
- Sliabh Luachra style often features off-beat accents
- Quick, punchy ornaments maintain tempo
- Chicago Push style uses dense ornamentation
Output the transformed ABC notation with polka ornaments.
""",

    "slip_jig_graceful_ornaments": """
Transform this ABC notation with slip jig ornamentation:
- Graceful, flowing 9/8 character
- Three groups of three eighth notes
- Often melodically complex - ornaments add to elaboration
- More elaborate than standard jigs
- Maintain lilting, dance quality
- Selective but effective ornamentation
Output the transformed ABC notation with slip jig ornaments.
""",

    # ========================================
    # VARIATION APPROACHES
    # ========================================
    
    "ornament_type_substitution": """
Transform this ABC notation by substituting ornament types:
- Where cuts exist, try taps instead (or vice versa)
- Replace long rolls with triplets in same position
- Substitute crans for rolls on low notes
- Swap slides for rolls at cadences
- Same placement, different ornament vocabulary
- Creates variation while maintaining structure
Output the transformed ABC notation with ornament substitutions.
""",

    "ornament_removal_simplification": """
Transform this ABC notation by removing some ornaments:
- Take heavily ornamented version and simplify
- Remove every other ornament
- Keep only cadential and strong-beat ornaments
- Create breathing room and clarity
- Useful for creating contrast between sections
- "Less is more" approach
Output the transformed ABC notation with ornaments removed for simplification.
""",

    "ornament_displacement": """
Transform this ABC notation by displacing ornament positions:
- Move ornaments to different beats within same phrase
- Shift from strong beats to weak beats (or vice versa)
- Maintain total ornament count but change placement
- Creates different rhythmic emphasis
- Advanced variation technique
- Requires understanding of rhythmic function
Output the transformed ABC notation with displaced ornaments.
""",

    "call_response_ornamentation": """
Transform this ABC notation with call-response ornament pattern:
- First phrase (call): minimal or no ornaments
- Second phrase (response): ornament heavily
- Creates question-answer dynamic
- Alternating sparse and dense decoration
- Traditional variation approach
- Works well in 8-bar structures
Output the transformed ABC notation with call-response ornamentation.
""",

    # ========================================
    # ADVANCED TECHNIQUES
    # ========================================
    
    "spontaneous_varied_ornaments": """
Transform this ABC notation with spontaneous varied ornamentation:
- No two repeats should have identical ornaments
- Vary ornament choice on each repetition
- Different placements on each pass
- Maintain overall density level but change specifics
- Simulates live performance spontaneity
- Advanced improvisatory approach
Output the transformed ABC notation with spontaneously varied ornaments.
""",

    "cross_row_ornaments_concertina": """
Transform this ABC notation with cross-row ornamentation (concertina):
- Utilize cross-row fingering for ornamental possibilities
- Noel Hill "first choice" fingering approach
- Z-pattern ornaments between rows
- Never same finger for consecutive buttons
- Enables faster, more fluid ornamentation
- Advanced concertina-specific technique
Output the transformed ABC notation with cross-row ornaments (concertina-specific).
""",

    "double_stop_ornaments_fiddle": """
Transform this ABC notation with double-stop ornaments (fiddle):
- Add double-stops as ornamental emphasis
- Perfect fifths (G-D, D-A, A-E) most common
- Open string drones under ornamented melody
- Donegal tradition uses extensively
- Creates bagpipe-like effect
- Place at strong beats and cadences
Output the transformed ABC notation with double-stop ornaments (fiddle-specific).
""",

    "harmonic_ornament_combinations": """
Transform this ABC notation combining harmonic and ornamental elements:
- Ornaments that imply or outline harmony
- Arpeggio-based triplets and runs
- Ornamental notes chosen from chord tones
- Creates both melodic interest and harmonic clarity
- Advanced technique requiring harmonic understanding
- Common in arranged or concert settings
Output the transformed ABC notation with harmonic ornaments.
""",

    # ========================================
    # LEARNING PROGRESSION LEVELS
    # ========================================
    
    "beginner_essential_ornaments": """
Transform this ABC notation with beginner-level essential ornaments:
- Cuts and taps only
- Place on obvious strong beats and long notes
- No rolls, triplets, or complex ornaments yet
- 3-5 ornaments per 8-bar phrase maximum
- Focus on execution clarity over quantity
- Master these before advancing
Output the transformed ABC notation with beginner ornaments.
""",

    "intermediate_standard_ornaments": """
Transform this ABC notation with intermediate standard ornaments:
- Cuts, taps, and basic rolls
- Simple triplets on appropriate notes
- Standard placement patterns (strong beats, cadences)
- 6-10 ornaments per 8-bar phrase
- Building fluency and variety
- Traditional session-appropriate level
Output the transformed ABC notation with intermediate ornaments.
""",

    "advanced_master_ornaments": """
Transform this ABC notation with advanced master-level ornamentation:
- Full ornament vocabulary (cuts, taps, rolls, slides, crans, bounces)
- Spontaneous variation between repeats
- Regional style characteristics
- Instrument-specific techniques
- 10-15+ ornaments per phrase when appropriate
- Performance-level decoration
Output the transformed ABC notation with advanced ornaments.
""",

    # ========================================
    # SPECIAL CONTEXTS
    # ========================================
    
    "session_appropriate_ornaments": """
Transform this ABC notation with session-appropriate ornamentation:
- Moderate density - not showing off
- Standard placements that won't confuse other players
- Regional style appropriate to tune origins
- Blend with group rather than standing out
- Ornaments that enhance, not dominate
- Respect community standards
Output the transformed ABC notation with session-appropriate ornaments.
""",

    "solo_performance_ornaments": """
Transform this ABC notation with solo performance ornamentation:
- Fuller decoration showcasing technique
- Can use more elaborate ornaments
- Variety of ornament types
- Build intensity through piece
- Display mastery while serving musicality
- Concert or recording context
Output the transformed ABC notation with solo performance ornaments.
""",

    "teaching_demonstration_ornaments": """
Transform this ABC notation with clearly marked teaching ornaments:
- Each ornament type clearly distinguished
- Placement shows pedagogical logic
- Progression from simple to complex
- Examples of correct positioning
- Demonstrates principles in action
- Educational context
Output the transformed ABC notation with teaching-demonstration ornaments.
""",

    "accompaniment_light_ornaments": """
Transform this ABC notation with light ornaments for accompaniment:
- When playing backup to another melody instrument
- Very sparse ornamentation
- Don't compete with lead melody
- Emphasis on rhythm over decoration
- Support role, not featured
- Harmony and rhythm primary, ornaments minimal
Output the transformed ABC notation with accompaniment-level ornaments.
""",

}

# Utility functions for working with ornamentation transformations

def get_all_ornamentation_names():
    """Return list of all ornamentation transformation names."""
    return list(ORNAMENTATION_TRANSFORMATIONS.keys())

def get_random_ornamentation():
    """Return a random ornamentation transformation name and its prompt."""
    import random
    name = random.choice(list(ORNAMENTATION_TRANSFORMATIONS.keys()))
    return name, ORNAMENTATION_TRANSFORMATIONS[name]

def get_ornamentation_by_category(category):
    """
    Get ornamentation transformations by category.
    
    Categories:
    - basic: Basic ornament types
    - instrument: Instrument-specific ornaments
    - rhythm: Rhythmic placement strategies
    - density: Density and intensity levels
    - regional: Regional style approaches
    - tune_type: Tune type specific
    - variation: Variation approaches
    - advanced: Advanced techniques
    - learning: Learning progression levels
    - context: Special contexts
    """
    
    categories = {
        'basic': [
            'cuts_on_downbeats', 'taps_for_grounding', 'long_rolls_jig_placement',
            'short_rolls_reel_placement', 'triplets_characteristic', 'slides_melodic',
            'crans_low_notes', 'bounces_casadh'
        ],
        'instrument': [
            'fiddle_bowed_triplets', 'concertina_phantom_button', 'concertina_bellows_shake',
            'accordion_bellows_pulse', 'whistle_flute_tonguing', 'whistle_breath_ornaments',
            'pipes_regulator_style'
        ],
        'rhythm': [
            'ornament_strong_beats_only', 'ornament_phrase_beginnings', 'ornament_cadence_points',
            'ornament_long_notes_only', 'alternating_ornament_pattern'
        ],
        'density': [
            'minimal_sparse_ornaments', 'moderate_tasteful_ornaments', 'dense_elaborate_ornaments',
            'progressive_density_build'
        ],
        'regional': [
            'sligo_style_ornaments', 'east_clare_galway_minimal', 'donegal_aggressive_ornaments',
            'west_clare_rich_ornaments', 'sliabh_luachra_rhythmic'
        ],
        'tune_type': [
            'jig_ornament_patterns', 'reel_ornament_patterns', 'slow_air_ornaments',
            'hornpipe_dotted_ornaments', 'polka_driving_ornaments', 'slip_jig_graceful_ornaments'
        ],
        'variation': [
            'ornament_type_substitution', 'ornament_removal_simplification', 'ornament_displacement',
            'call_response_ornamentation'
        ],
        'advanced': [
            'spontaneous_varied_ornaments', 'cross_row_ornaments_concertina',
            'double_stop_ornaments_fiddle', 'harmonic_ornament_combinations'
        ],
        'learning': [
            'beginner_essential_ornaments', 'intermediate_standard_ornaments',
            'advanced_master_ornaments'
        ],
        'context': [
            'session_appropriate_ornaments', 'solo_performance_ornaments',
            'teaching_demonstration_ornaments', 'accompaniment_light_ornaments'
        ]
    }
    
    if category not in categories:
        raise ValueError(f"Unknown category: {category}. Valid categories: {list(categories.keys())}")
    
    return {name: ORNAMENTATION_TRANSFORMATIONS[name] for name in categories[category]}

def get_ornamentation_for_tune_type(tune_type):
    """
    Get appropriate ornamentation based on tune type.
    
    Args:
        tune_type: 'reel', 'jig', 'hornpipe', 'polka', 'waltz', 'slip_jig', or 'air'
    
    Returns:
        Dictionary of recommended ornamentation transformations
    """
    
    tune_mappings = {
        'reel': ['reel_ornament_patterns', 'short_rolls_reel_placement', 'ornament_strong_beats_only'],
        'jig': ['jig_ornament_patterns', 'long_rolls_jig_placement', 'triplets_characteristic'],
        'hornpipe': ['hornpipe_dotted_ornaments', 'moderate_tasteful_ornaments'],
        'polka': ['polka_driving_ornaments', 'sliabh_luachra_rhythmic'],
        'slip_jig': ['slip_jig_graceful_ornaments', 'long_rolls_jig_placement'],
        'air': ['slow_air_ornaments', 'slides_melodic', 'dense_elaborate_ornaments']
    }
    
    if tune_type not in tune_mappings:
        raise ValueError(f"Unknown tune type: {tune_type}. Valid types: {list(tune_mappings.keys())}")
    
    return {name: ORNAMENTATION_TRANSFORMATIONS[name] for name in tune_mappings[tune_type]}

def get_ornamentation_for_skill_level(skill='beginner'):
    """
    Get appropriate ornamentation based on player skill level.
    
    Args:
        skill: 'beginner', 'intermediate', or 'advanced'
    
    Returns:
        Recommended ornamentation transformation name and prompt
    """
    import random
    
    skill_map = {
        'beginner': ['beginner_essential_ornaments', 'cuts_on_downbeats', 'ornament_long_notes_only'],
        'intermediate': ['intermediate_standard_ornaments', 'moderate_tasteful_ornaments', 
                        'long_rolls_jig_placement', 'short_rolls_reel_placement'],
        'advanced': ['advanced_master_ornaments', 'spontaneous_varied_ornaments',
                    'dense_elaborate_ornaments']
    }
    
    options = skill_map.get(skill, skill_map['beginner'])
    name = random.choice(options)
    return name, ORNAMENTATION_TRANSFORMATIONS[name]

def get_ornamentation_for_regional_style(region):
    """
    Get ornamentation appropriate to regional style.
    
    Args:
        region: 'sligo', 'east_clare', 'donegal', 'west_clare', or 'sliabh_luachra'
    
    Returns:
        Regional ornamentation transformation name and prompt
    """
    
    region_map = {
        'sligo': 'sligo_style_ornaments',
        'east_clare': 'east_clare_galway_minimal',
        'east_galway': 'east_clare_galway_minimal',
        'donegal': 'donegal_aggressive_ornaments',
        'west_clare': 'west_clare_rich_ornaments',
        'sliabh_luachra': 'sliabh_luachra_rhythmic'
    }
    
    name = region_map.get(region.lower())
    if not name:
        raise ValueError(f"Unknown region: {region}. Valid regions: {list(region_map.keys())}")
    
    return name, ORNAMENTATION_TRANSFORMATIONS[name]

def get_progressive_ornamentation_sequence(num_repeats=4):
    """
    Get a sequence of progressively denser ornamentation for repeated sections.
    
    Args:
        num_repeats: Number of times section repeats (typically 2-4)
    
    Returns:
        List of (name, prompt) tuples in order of increasing density
    """
    
    progression_sequence = [
        'minimal_sparse_ornaments',
        'moderate_tasteful_ornaments',
        'dense_elaborate_ornaments',
        'spontaneous_varied_ornaments'
    ]
    
    # Return appropriate number based on repeats
    selected = progression_sequence[:num_repeats]
    return [(name, ORNAMENTATION_TRANSFORMATIONS[name]) for name in selected]

def combine_ornament_styles(tune_type, region, skill='intermediate'):
    """
    Combine tune type, regional style, and skill level to get optimal ornamentation.
    
    Args:
        tune_type: Type of tune (reel, jig, etc.)
        region: Regional style
        skill: Player skill level
    
    Returns:
        Combined recommendation
    """
    import random
    
    # Get all three recommendation sets
    tune_ornaments = get_ornamentation_for_tune_type(tune_type)
    region_name, region_prompt = get_ornamentation_for_regional_style(region)
    skill_name, skill_prompt = get_ornamentation_for_skill_level(skill)
    
    # Combine and pick one
    all_options = list(tune_ornaments.keys()) + [region_name, skill_name]
    selected = random.choice(all_options)
    
    return selected, ORNAMENTATION_TRANSFORMATIONS[selected]

# Example usage
if __name__ == "__main__":
    import random
    
    print("=== ABC Ornamentation Transformation Prompts ===\n")
    
    # Example 1: Get specific transformation
    print("1. Specific transformation (long_rolls_jig_placement):")
    print(ORNAMENTATION_TRANSFORMATIONS['long_rolls_jig_placement'])
    
    # Example 2: Random transformation
    print("\n2. Random ornamentation:")
    name, prompt = get_random_ornamentation()
    print(f"Name: {name}")
    print(f"Prompt: {prompt}")
    
    # Example 3: Get by category
    print("\n3. All basic ornament types:")
    basic = get_ornamentation_by_category('basic')
    for name in basic:
        print(f"  - {name}")
    
    # Example 4: Tune-type specific
    print("\n4. Ornamentation for jig:")
    jig_ornaments = get_ornamentation_for_tune_type('jig')
    for name in jig_ornaments:
        print(f"  - {name}")
    
    # Example 5: Skill level
    print("\n5. Ornamentation for intermediate player:")
    name, prompt = get_ornamentation_for_skill_level('intermediate')
    print(f"Name: {name}")
    print(f"Prompt: {prompt}")
    
    # Example 6: Regional style
    print("\n6. Ornamentation for Sligo style:")
    name, prompt = get_ornamentation_for_regional_style('sligo')
    print(f"Name: {name}")
    
    # Example 7: Progressive sequence
    print("\n7. Progressive ornamentation for 3 repeats:")
    sequence = get_progressive_ornamentation_sequence(3)
    for i, (name, _) in enumerate(sequence, 1):
        print(f"  Repeat {i}: {name}")
    
    # Example 8: Combined recommendation
    print("\n8. Combined recommendation (reel, donegal style, advanced):")
    name, prompt = combine_ornament_styles('reel', 'donegal', 'advanced')
    print(f"Recommended: {name}")
    
    print("\n9. All available categories:")
    categories = ['basic', 'instrument', 'rhythm', 'density', 'regional',
                  'tune_type', 'variation', 'advanced', 'learning', 'context']
    for cat in categories:
        count = len(get_ornamentation_by_category(cat))
        print(f"  - {cat}: {count} transformations")