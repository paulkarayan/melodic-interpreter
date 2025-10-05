"""
Harmonic Transformation Prompts for ABC Notation
Based on Anglo concertina self-accompaniment in Irish traditional music

These prompts add or modify harmonic accompaniment while preserving melodic identity.
Designed for bisonoric instruments but applicable to any accompaniment context.

Usage:
    from abc_harmony_prompts import HARMONY_TRANSFORMATIONS
    
    # Select by name
    prompt = HARMONY_TRANSFORMATIONS['fifth_drone_bass']
    
    # Random selection
    import random
    prompt = random.choice(list(HARMONY_TRANSFORMATIONS.values()))
    
    # Get transformation name
    name = random.choice(list(HARMONY_TRANSFORMATIONS.keys()))
    prompt = HARMONY_TRANSFORMATIONS[name]
"""

HARMONY_TRANSFORMATIONS = {
    
    # ========================================
    # FUNDAMENTAL INTERVAL VOICINGS
    # ========================================
    
    "fifth_drone_bass": """
Transform this ABC notation by adding fifth-based drone accompaniment in ABC format:
- Add bass harmony notes using ABC chord notation with square brackets [AD] for chords
- Use root and fifth intervals (e.g., if melody is in A, add [AD] or [AE])
- Place harmony on strong beats only (beat 1 in 6/8, beats 1 and 3 in 4/4)
- Example: if melody bar is "eAA Bcd" in A minor, add bass like "[AE]eAA Bcd" or "e[AE]A Bcd"
- Keep it simple - use longer note values for the bass (half notes or dotted quarters in bass clef)
- The ABC notation should use [XY] for simultaneous notes/chords
Output ONLY the complete transformed ABC notation with the bass harmony added.
""",

    "root_fifth_power_chords": """
Transform this ABC notation by adding power chord accompaniment in ABC format:
- Add root-fifth chords using square brackets like [AD] or [AE]
- Place at phrase beginnings and endings, and on strong beats
- Example: "eAA Bcd|eaf ged|" becomes "[AE]eAA Bcd|[AE]eaf ged|"
- Use the root and fifth of the key (for A minor: [AE], for D major: [DA])
- Keep sparse - don't add to every bar
- The ABC notation uses [XY] for simultaneous notes
Output ONLY the complete transformed ABC notation with power chords added.
""",

    "strategic_bass_notes": """
Transform this ABC notation by adding strategic bass notes in ABC format:
- Add single low bass notes on strong beats using uppercase letters (A, D, E, G, etc.)
- Place before the melody notes on beat 1
- Example: "eAA Bcd|" becomes "AeAA Bcd|" (A bass note before melody)
- Use root notes of the key (for A minor: A, E; for D major: D, A)
- Keep very sparse - only on beat 1 of some bars
- Do NOT use chords, only single bass notes
Output ONLY the complete transformed ABC notation with bass notes added.
""",

    "open_fourth_voicing": """
Transform this ABC notation by adding fourth-based harmonies:
- Add perfect fourth intervals (E-A, A-D, D-G common in Irish music)
- Particularly effective in Dorian mode tunes
- Place on long notes and phrase endings
- Use ascending fourths as characteristic Irish sound
- Match bellows direction of melody
- Keep texture open and modal
Output the transformed ABC notation with fourth-based harmonies.
""",

    "octave_doubling": """
Transform this ABC notation by adding octave doubling in ABC format:
- Double some melody notes with the same note an octave lower
- In ABC: lowercase is middle octave, uppercase is octave below, add comma for octave above
- Example: "eAA Bcd" could become "[Ee][AA][AA] [Bb]cd" (octave doubling on some notes)
- Use square brackets [Xx] to play two notes simultaneously
- Don't double every note - be selective (phrase beginnings, long notes)
- This creates fuller sound without changing harmony
Output ONLY the complete transformed ABC notation with octave doubling added.
""",

    "thirds_harmony": """
Transform this ABC notation by adding harmony in thirds in ABC format:
- Add harmony notes a third above or below the melody
- In ABC: use square brackets to play notes together like [ec] for E and C together
- Example: melody "eAA Bcd" could become "[ec][AC][AC] [Bd]cd" (thirds added)
- Use major or minor thirds based on the key (A minor: A-C, E-G; D major: D-F#, A-C#)
- Be selective - don't harmonize every note, just important melody notes
- Creates richer sound while maintaining melody
Output ONLY the complete transformed ABC notation with thirds harmony added.
""",

    "simple_chord_progression": """
Transform this ABC notation by adding simple I-IV-V chord progressions in ABC format:
- Use simple I-IV-V (tonic-subdominant-dominant) progressions with occasional vi (relative minor)
- Example in G major: G-Em-C-D corresponds to I-vi-IV-V
- Example in A minor: Am-Dm-Em corresponds to i-iv-v
- Add chord notes using square brackets on strong beats: [GBd] for G major, [ACE] for A minor
- Place chords at phrase beginnings/endings and cadence points
- Example: "GAB cde|" becomes "[GBd]GAB [ceg]cde|" (I chord, then V chord)
- Keep it simple - use root position triads (root, third, fifth)
Output ONLY the complete transformed ABC notation with chord progression added.
""",

    "simple_chord_changes": """
Transform this ABC notation by analyzing the melody and adding anglo concertina chord voicings:
- Analyze the melody to identify what chords fit each section (I, IV, V, vi, etc.)
- When the chord changes (and on the first note of the piece), replace the melody note with 2-3 chord notes using square brackets
- Write the chord name above each chord change using ABC notation: "Am" for chord annotations
- Use anglo concertina-appropriate voicings: limit to 2-3 notes maximum
- Example in A Dorian: if bar starts with "eAA Bcd" and chord is Am, replace with "\"Am\"[ACE]AA Bcd|"
- Example chord change: "|eAA Bcd|" becomes "|\"Am\"[ACE]AA Bcd|" then next bar "|\"Dm\"[DFA] eaf ged|" if chord changes to Dm
- Common chords for A Dorian: Am, Dm, G, C
- Common chords for D Major: D, G, A, Bm
- Common chords for D Mixolydian: D, C, G, Am
- Common chords for G Major: G, C, D, Em
- Keep rhythm natural - chord voicing should fit the same duration as the note it replaces
Output ONLY the complete transformed ABC notation with chord changes added.
""",

    "bass_line": """
Transform this ABC notation by adding a simple walking bass line in ABC format:
- Add bass notes that move stepwise or by small intervals
- Use low register notes (uppercase letters: A, B, C, D, E, F, G)
- Example: "eAA Bcd|eaf ged|" becomes "AeAA BcBcd|CeaDf Eged|" (bass notes A, B, C, E added)
- Connect the root notes of chords with passing notes
- Keep it simple and rhythmic - quarter notes or half notes
- Bass should support the melody, not compete with it
Output ONLY the complete transformed ABC notation with bass line added.
""",

    "selective_thirds_color": """
Transform this ABC notation by adding selective thirds for color:
- Add thirds (major or minor) sparingly for harmonic color
- Use only at phrase endings or on long sustained notes
- Keep minimal - thirds can sound "too full" if overused
- Determine major vs minor from melodic context
- Primary harmony should remain fifths; thirds are accent only
- Match bellows direction
Output the transformed ABC notation with selective third intervals.
""",

    # ========================================
    # RHYTHMIC PLACEMENT PATTERNS
    # ========================================
    
    "oom_pah_pattern": """
Transform this ABC notation by adding oom-pah accompaniment pattern:
- Bass note (root) on strong beats (1, 3 in 4/4)
- Chord (typically root-fifth) on weak beats (2, 4 in 4/4)
- Creates alternating bass-chord "oom-pah" feel
- Particularly effective for polkas and hornpipes
- Keep right hand melody independent
- Match bellows direction for each element
Output the transformed ABC notation with oom-pah accompaniment.
""",

    "waltz_bass_chord_chord": """
Transform this ABC notation by adding waltz accompaniment pattern:
- Bass note on beat 1 (oom)
- Chord on beat 2 (pah)
- Chord on beat 3 (pah)
- Creates "oom-pah-pah" pattern characteristic of 3/4 time
- Use root-fifth chords or simple triads
- Sustain chords through their duration
- Match bellows direction
Output the transformed ABC notation with waltz accompaniment pattern.
""",

    "jig_dotted_quarter_chords": """
Transform this ABC notation by adding jig-appropriate harmony:
- Use dotted quarter note chord pulses matching jig rhythm
- Place on main beats (1 and 4 in 6/8 meter)
- Follow "jiggety-jiggety" or "carrots and cabbages" feel
- Use root-fifth or simple thirds
- Allow harmony to bounce with the jig lilt
- Less frantic than reels - more room for chord voicings
Output the transformed ABC notation with jig harmonization.
""",

    "reel_minimal_harmony": """
Transform this ABC notation by adding minimal reel harmony:
- Keep harmony extremely sparse due to fast tempo
- Brief fifth chords on strong beats only (beat 1 primarily)
- No continuous accompaniment - breaks for melody focus
- Single beat accents rather than sustained chords
- Minimize bellows work to maintain reel speed
- Preserve "double decker" driving rhythm
Output the transformed ABC notation with minimal reel harmony.
""",

    "hornpipe_deliberate_chords": """
Transform this ABC notation by adding hornpipe-style harmony:
- Fuller, more deliberate chord voicings suitable for slower tempo
- Follow characteristic dotted rhythm (dotted eighth + sixteenth)
- Clear "oom-pah" bass-chord alternation works well
- More sustained harmonies than reels
- Can incorporate chord changes more easily
- Match the "swagger" or "roll" of hornpipe rhythm
Output the transformed ABC notation with hornpipe harmonization.
""",

    "polka_strong_bass_pattern": """
Transform this ABC notation by adding polka bass pattern:
- Strong characteristic alternating bass-chord on each beat in 2/4
- Bass note (root) on beat 1, chord on beat 2
- Bass note (root or fifth) on next beat 1, chord on beat 2
- Creates classic "oom-pah oom-pah" feel
- Right hand plays complete melody independently
- Particularly important in Chicago Push style
Output the transformed ABC notation with polka bass pattern.
""",

    "even_beat_emphasis": """
Transform this ABC notation by adding harmony on even beats only:
- Place chords or double-stops on beats 2, 4 (in 4/4) or 2, 4, 6 (in 6/8)
- Leave strong beats for melody emphasis
- Similar to fiddle double-stop technique
- Creates rhythmic lift without overpowering
- Use simple fifth or fourth intervals
- Sparse but strategically placed
Output the transformed ABC notation with even-beat harmony.
""",

    # ========================================
    # DRONE AND SUSTAINED TECHNIQUES
    # ========================================
    
    "tonic_drone_sustain": """
Transform this ABC notation by adding sustained tonic drone in ABC format:
- Add a sustained low tonic note (root of the key) that continues through bars
- Use uppercase for low octave: for A minor use "A", for D major use "D"
- Make it very long duration using number notation (A4 = whole note, A8 = double whole)
- Example in A minor: Add "A8" at start to sustain through multiple bars
- Place the drone in a separate voice or at the beginning of bars
- The drone should be constant while melody moves above it
- Example: "|:A8 eAA Bcd|eaf ged|" (A drone sustains while melody plays)
Output ONLY the complete transformed ABC notation with tonic drone added.
""",

    "fifth_drone_sustain": """
Transform this ABC notation by adding sustained fifth drone in ABC format:
- Add a sustained root-fifth interval using square brackets [AE] or [DA]
- Use uppercase for low octave and make very long duration with numbers
- Example for A minor: "[AE]8" sustains A and E together for 8 beats
- Place at the start of phrases and let it sustain
- Example: "|:[AE]8 eAA Bcd|eaf ged|" (root-fifth drone while melody plays)
- This creates the classic Irish traditional drone sound
- Neither major nor minor - just root and fifth
Output ONLY the complete transformed ABC notation with fifth drone added.
""",

    "modal_drone_ambiguity": """
Transform this ABC notation by adding ambiguous modal drone in ABC format:
- Add root and fifth intervals ONLY - NO thirds to maintain modal ambiguity
- Use square brackets for simultaneous notes [AE] or [DA]
- Can be sustained long notes OR repeated on beats
- Example sustained: "|:[AE]8 eAA Bcd|" (one long drone)
- Example repeated: "|:[AE][AE][AE] Bcd|" (repeated drone pulses)
- Allows the melody to move between major/minor/modal over neutral drone
- Works great for Dorian and Mixolydian tunes
Output ONLY the complete transformed ABC notation with modal drone added.
""",

    "regulator_style_chords": """
Transform this ABC notation by adding uilleann pipe regulator-style chords:
- Add brief, percussive chord accents emulating pipe regulators
- Place on strong beats or syncopated positions
- Use stacked thirds or root-fifth-octave voicings
- Keep short and punchy, not sustained
- Match the bellows articulation style of pipes
- Strategic placement for rhythmic emphasis
Output the transformed ABC notation with regulator-style chords.
""",

    # ========================================
    # TEXTURE AND DENSITY VARIATIONS
    # ========================================
    
    "sparse_to_dense_progression": """
Transform this ABC notation with progressive harmonic density:
- Start with no harmony or single bass notes only
- Gradually add fifth chords at phrase endings
- Progress to more continuous harmony
- End with fuller triadic voicings if appropriate
- Create arc of harmonic intensity through the tune
- Maintain melody primacy throughout
Output the transformed ABC notation with density progression.
""",

    "phrase_ending_harmony_only": """
Transform this ABC notation by adding harmony at phrase endings only:
- Leave entire phrases as melody alone
- Add chord (root-fifth or triad) only on final note of phrase
- Creates punctuation and harmonic confirmation
- Cadential emphasis without continuous accompaniment
- Matches traditional sparse approach
- Very suitable for session context
Output the transformed ABC notation with phrase-ending harmony.
""",

    "long_note_harmony": """
Transform this ABC notation by adding harmony on long notes only:
- Identify sustained notes (half notes, dotted quarters, etc.)
- Add harmonic support only on these sustained pitches
- Use root-fifth or appropriate chord voicing
- Leave shorter, moving notes unharmonized
- Creates breathing room and emphasizes structural tones
- Tasteful and minimal approach
Output the transformed ABC notation with long-note harmony.
""",

    "call_response_harmony": """
Transform this ABC notation by harmonizing response phrases only:
- Leave "call" phrases (questions) as melody alone
- Add harmony to "answer" phrases (resolutions)
- Creates question-answer texture dynamic
- Typically harmonize second half of each 8-bar section
- Use fuller harmony on final cadences
- Builds harmonic intensity toward resolution
Output the transformed ABC notation with call-response harmony.
""",

    "section_contrast_harmony": """
Transform this ABC notation with sectional harmonic contrast:
- Keep A section with minimal or no harmony (melody focus)
- Add fuller harmony to B section
- Creates textural contrast between sections
- B section can feature continuous accompaniment
- Return to sparse texture for A section repeats
- Highlights structural divisions
Output the transformed ABC notation with sectional harmonic contrast.
""",

    # ========================================
    # BELLOWS DIRECTION TECHNIQUES
    # ========================================
    
    "press_direction_harmony": """
Transform this ABC notation by adding harmony only on press (bellows compression):
- Analyze melody for press notes (bellows closing)
- Add harmonic support only when bellows are pressing
- Draw notes remain as melody alone
- Uses bisonoric constraint as musical feature
- Common chords: G5, C5, E minor on press
- Creates rhythmic pattern based on bellows
Output the transformed ABC notation with press-direction harmony.
""",

    "draw_direction_harmony": """
Transform this ABC notation by adding harmony only on draw (bellows expansion):
- Analyze melody for draw notes (bellows opening)
- Add harmonic support only when bellows are drawing
- Press notes remain as melody alone
- Uses bisonoric constraint as musical feature
- Common chords: D5, A5, A minor on draw
- Creates rhythmic pattern based on bellows
Output the transformed ABC notation with draw-direction harmony.
""",

    "bellows_articulated_chords": """
Transform this ABC notation by using bellows direction for chord articulation:
- Make bellows changes align with chord changes
- Each direction shift = new harmony
- Use bellows rhythm as musical phrasing device
- Press chords for one harmonic function, draw for another
- Creates natural articulation and separation
- Bellows becomes conductor of harmony
Output the transformed ABC notation with bellows-articulated chords.
""",

    # ========================================
    # ADVANCED HARMONIC TECHNIQUES
    # ========================================
    
    "walking_bass_line": """
Transform this ABC notation by adding walking bass line:
- Create melodic bass movement connecting chord roots
- Use scale-wise motion (stepwise bass)
- Move smoothly between harmonic anchor points
- Keep independent from melody rhythm
- Descending or ascending scalar patterns
- More common in slow airs or arranged contexts
Output the transformed ABC notation with walking bass.
""",

    "countermelody_harmony": """
Transform this ABC notation by adding harmonic countermelody:
- Create independent melodic line that implies harmony
- Moves against main melody (contrary or oblique motion)
- Uses chord tones to define harmony while being melodic
- Interweaves rhythmically with main melody
- Requires cross-row fingering skill
- More advanced technique for performance settings
Output the transformed ABC notation with countermelody.
""",

    "quartal_voicing": """
Transform this ABC notation by using quartal (fourth-based) harmony:
- Stack perfect fourths instead of thirds
- Creates modern, open sound while staying modal
- Example: D-G-C or A-D-G stacks
- More ambiguous than triads but richer than fifths
- Particularly effective in Dorian mode
- Requires wider stretches but powerful effect
Output the transformed ABC notation with quartal harmony.
""",

    "seventh_chord_color": """
Transform this ABC notation by adding selective seventh chords:
- Use major 7ths, dominant 7ths, or minor 7ths sparingly
- Only at major cadence points or slow air passages
- Creates richer harmonic color
- Example: G major 7 (G-B-D-F#) or D7 (D-F#-A-C)
- Must be very tasteful - can sound "too jazzy" if overused
- Match bellows direction constraints
Output the transformed ABC notation with seventh chord coloring.
""",

    "chromatic_passing_harmony": """
Transform this ABC notation by adding chromatic passing chords:
- Use brief chromatic harmonies as passing movement
- Connect diatonic chords with chromatic voice leading
- Example: G to G# diminished to A minor
- Very brief - quarter note or eighth note duration
- Creates harmonic interest and forward motion
- Must be subtle and quick to maintain traditional feel
Output the transformed ABC notation with chromatic passing harmony.
""",

    # ========================================
    # MODAL-SPECIFIC HARMONIZATIONS
    # ========================================
    
    "mixolydian_harmony": """
Transform this ABC notation with Mixolydian-appropriate harmony:
- Emphasize ♭7 chord (F major in G Mixolydian)
- Avoid V7-I resolutions (use ♭VII-I instead)
- No leading tone (F# in G Mixolydian) in harmony
- Common progression: I - ♭VII - I (G-F-G)
- Drone on tonic works well
- Creates characteristic modal sound avoiding major key feeling
Output the transformed ABC notation with Mixolydian harmonization.
""",

    "dorian_harmony": """
Transform this ABC notation with Dorian-appropriate harmony:
- Emphasize ♮6 chord (B minor in D Dorian)
- Use IV chord (G major in D Dorian) prominently
- Avoid ♭6 (B♭) in harmonization
- Common progression: i - IV - i (Dm - G - Dm)
- A-D fourths work well as characteristic interval
- Creates minor mode with bright sixth degree
Output the transformed ABC notation with Dorian harmonization.
""",

    "aeolian_natural_minor_harmony": """
Transform this ABC notation with Aeolian (natural minor) harmony:
- Use natural minor scale harmony (no raised 7th)
- Prominent ♭VII and ♭VI chords
- Avoid leading tone resolutions
- Example in A minor: Am - G - F - G - Am
- More melancholic than Dorian
- Keep modal character without harmonic minor alterations
Output the transformed ABC notation with Aeolian harmonization.
""",

    # ========================================
    # REGIONAL STYLE HARMONIZATIONS
    # ========================================
    
    "clare_fuller_harmony": """
Transform this ABC notation with Clare-style fuller harmony:
- More complex harmonic support reflecting Clare's ornate style
- Add melodic fills between phrases in bass
- Use syncopated chord placement
- More active left hand than other styles
- Driving, energetic harmonic rhythm
- Reflects Noel Hill and Edel Fox approaches
Output the transformed ABC notation with Clare-style harmony.
""",

    "donegal_sparse_rhythm": """
Transform this ABC notation with Donegal-style sparse rhythmic harmony:
- Minimal melodic elaboration in harmony
- Strong rhythmic drive with simple bass-chord
- Straightforward root-fifth voicings
- Less harmonic complexity, more rhythmic emphasis
- Steady, driving character without embellishment
- Reflects direct, powerful style
Output the transformed ABC notation with Donegal-style harmony.
""",

    "sliabh_luachra_sliding_harmony": """
Transform this ABC notation with Sliabh Luachra-style sliding harmony:
- Smooth chromatic voice leading between chords
- Emphasis on melodic bass lines that "slide"
- Polka and sliding reel style harmonic approach
- Characteristic rhythmic lilt in harmony
- Bass moves in slides and steps
- Reflects regional polka tradition
Output the transformed ABC notation with Sliabh Luachra-style harmony.
""",

    # ========================================
    # SESSION VS PERFORMANCE CONTEXTS
    # ========================================
    
    "session_appropriate_minimal": """
Transform this ABC notation with session-appropriate minimal harmony:
- Extremely sparse - mostly melody alone
- Brief bass notes or fifth chords only at major cadences
- No continuous accompaniment
- Respects session etiquette of melody primacy
- Allows other players' melodies to come through
- Won't "annoy" other musicians with excessive harmony
Output the transformed ABC notation with session-minimal harmony.
""",

    "solo_performance_fuller": """
Transform this ABC notation with solo performance harmonic arrangement:
- Fuller harmony appropriate when playing alone
- Can use continuous accompaniment patterns
- Triads, seventh chords, and richer voicings allowed
- More deliberate harmonic rhythm and changes
- Showcase instrumental capability
- Balance melody and harmony for listening (not just dancing)
Output the transformed ABC notation with solo performance harmony.
""",

    "arranged_ensemble_parts": """
Transform this ABC notation with arranged ensemble harmonization:
- Create distinct harmonic parts for multiple players
- Planned chord voicings and distribution
- Can include sustained pads, countermelodies, and bass
- More sophisticated than session spontaneous harmony
- Pre-composed harmonic arrangement
- Suitable for concert or recording context
Output the transformed ABC notation with ensemble arrangement.
""",

    # ========================================
    # FIDDLE-INFLUENCED TECHNIQUES
    # ========================================
    
    "double_stop_style": """
Transform this ABC notation with fiddle double-stop style harmony:
- Add intervals playable as double-stops: fifths, fourths, octaves
- Place on beats 2, 4, 6 (even beats) for emphasis
- Use open string equivalents: G-D, D-A, A-E intervals
- Brief duration - eighth notes typically
- Emulates Donegal fiddle aggressive double-stop style
- Strategic placement, not continuous
Output the transformed ABC notation with double-stop style harmony.
""",

    "open_string_drone_equivalent": """
Transform this ABC notation with open-string drone equivalents:
- Sustain lower note while melody moves above
- Emulates fiddle playing melody on one string with drone below
- Common: D drone under melody in D major/Dorian
- Creates bagpipe-like effect
- Can sustain through phrase or intermittently
- Bass-register drone with treble melody
Output the transformed ABC notation with drone-equivalent harmony.
""",

    # ========================================
    # ACCORDION-INFLUENCED TECHNIQUES
    # ========================================
    
    "piano_accordion_vamping": """
Transform this ABC notation with piano accordion vamping style:
- Right hand: triadic chords on off-beats
- Left hand: single bass notes on beats
- Creates highly rhythmic chordal style
- Fuller sound than traditional concertina approach
- More continuous harmonic texture
- Characteristic of piano box style
Output the transformed ABC notation with vamping-style harmony.
""",

    "button_accordion_bass_chord": """
Transform this ABC notation with button accordion style bass-chord:
- Bass button on beat 1 (root note)
- Chord button on beat 2 (major triad: root-third-fifth)
- Alternate between bass and chord consistently
- Common in B/C box: C bass/chord on push, G bass/chord on pull
- More predetermined harmonic pattern
- Works well for jigs and reels
Output the transformed ABC notation with bass-chord style.
""",

    # ========================================
    # INTENSITY AND DEVELOPMENT
    # ========================================
    
    "establishing_first_time": """
Transform this ABC notation with establishing first-time harmony:
- Very minimal harmony on first time through tune
- Perhaps single bass note at beginning and end
- Establishes tune identity before adding harmony
- Let melody be clearly heard first
- Prepare listener before harmonic elaboration
- Traditional "play it straight first" approach
Output the transformed ABC notation with establishing harmony.
""",

    "moderate_second_time": """
Transform this ABC notation with moderate second-time harmony:
- Add modest harmonic support on second pass
- Root-fifth chords at phrase endings
- Occasional bass notes on strong beats
- More than first time, less than maximum
- Build harmonic interest gradually
- Suitable for second A or B section
Output the transformed ABC notation with moderate harmony.
""",

    "full_final_time": """
Transform this ABC notation with full final-time harmony:
- Maximum appropriate harmonic elaboration
- Continuous or near-continuous accompaniment
- Fuller voicings: triads, sevenths where appropriate
- Walking bass or countermelody possible
- Climactic harmonic presentation
- Final statement can be most harmonically rich
Output the transformed ABC notation with full harmony.
""",

    # ========================================
    # SPECIAL TECHNIQUES
    # ========================================
    
    "percussive_chordal_accents": """
Transform this ABC notation with percussive chordal accents:
- Brief, sharp chord attacks as rhythmic punctuation
- Use bellows snap or strong articulation
- Place on syncopated beats or off-beats
- Emulates bodhrán or percussion
- Quarter note or shorter duration
- Creates rhythmic drive without sustained harmony
Output the transformed ABC notation with percussive chord accents.
""",

    "air_button_rests_for_harmony": """
Transform this ABC notation using air button for harmonic rests:
- Use air button (non-sounding) to maintain bellows direction
- Allows changing chords without bellows reversal
- Creates space between harmonic statements
- Technical solution for bisonoric harmony management
- Enables longer phrases in single direction with varied harmony
- Advanced bellows technique
Output the transformed ABC notation with air-button harmonic management.
""",

    "cross_rhythm_harmony": """
Transform this ABC notation with cross-rhythm harmonic pattern:
- Place harmony in different rhythmic pattern than melody
- Example: melody in eighths, harmony in dotted quarters
- Creates polyrhythmic texture
- Must maintain dance groove if appropriate
- Can use hemiola (3-against-2) in jigs
- More experimental, less traditional
Output the transformed ABC notation with cross-rhythm harmony.
""",

}

# Utility functions for working with harmony transformations

def get_all_harmony_transformation_names():
    """Return list of all harmony transformation names."""
    return list(HARMONY_TRANSFORMATIONS.keys())

def get_random_harmony_transformation():
    """Return a random harmony transformation name and its prompt."""
    import random
    name = random.choice(list(HARMONY_TRANSFORMATIONS.keys()))
    return name, HARMONY_TRANSFORMATIONS[name]

def get_harmony_by_category(category):
    """
    Get harmony transformations by category.
    
    Categories:
    - voicing: Fundamental interval voicings
    - rhythm: Rhythmic placement patterns
    - drone: Drone and sustained techniques
    - texture: Texture and density variations
    - bellows: Bellows direction techniques
    - advanced: Advanced harmonic techniques
    - modal: Modal-specific harmonizations
    - regional: Regional style harmonizations
    - context: Session vs performance contexts
    - fiddle: Fiddle-influenced techniques
    - accordion: Accordion-influenced techniques
    - intensity: Intensity and development
    - special: Special techniques
    """
    
    categories = {
        'voicing': [
            'fifth_drone_bass', 'root_fifth_power_chords', 'strategic_bass_notes',
            'open_fourth_voicing', 'octave_doubling', 'selective_thirds_color'
        ],
        'rhythm': [
            'oom_pah_pattern', 'waltz_bass_chord_chord', 'jig_dotted_quarter_chords',
            'reel_minimal_harmony', 'hornpipe_deliberate_chords', 'polka_strong_bass_pattern',
            'even_beat_emphasis'
        ],
        'drone': [
            'tonic_drone_sustain', 'fifth_drone_sustain', 'modal_drone_ambiguity',
            'regulator_style_chords'
        ],
        'texture': [
            'sparse_to_dense_progression', 'phrase_ending_harmony_only', 'long_note_harmony',
            'call_response_harmony', 'section_contrast_harmony'
        ],
        'bellows': [
            'press_direction_harmony', 'draw_direction_harmony', 'bellows_articulated_chords'
        ],
        'advanced': [
            'walking_bass_line', 'countermelody_harmony', 'quartal_voicing',
            'seventh_chord_color', 'chromatic_passing_harmony'
        ],
        'modal': [
            'mixolydian_harmony', 'dorian_harmony', 'aeolian_natural_minor_harmony'
        ],
        'regional': [
            'clare_fuller_harmony', 'donegal_sparse_rhythm', 'sliabh_luachra_sliding_harmony'
        ],
        'context': [
            'session_appropriate_minimal', 'solo_performance_fuller', 'arranged_ensemble_parts'
        ],
        'fiddle': [
            'double_stop_style', 'open_string_drone_equivalent'
        ],
        'accordion': [
            'piano_accordion_vamping', 'button_accordion_bass_chord'
        ],
        'intensity': [
            'establishing_first_time', 'moderate_second_time', 'full_final_time'
        ],
        'special': [
            'percussive_chordal_accents', 'air_button_rests_for_harmony', 'cross_rhythm_harmony'
        ]
    }
    
    if category not in categories:
        raise ValueError(f"Unknown category: {category}. Valid categories: {list(categories.keys())}")
    
    return {name: HARMONY_TRANSFORMATIONS[name] for name in categories[category]}

def get_harmony_for_tune_type(tune_type):
    """
    Get appropriate harmony transformations based on tune type.
    
    Args:
        tune_type: 'reel', 'jig', 'hornpipe', 'polka', 'waltz', 'slip_jig', or 'air'
    
    Returns:
        Dictionary of recommended harmony transformations
    """
    
    tune_mappings = {
        'reel': ['reel_minimal_harmony', 'strategic_bass_notes', 'fifth_drone_bass'],
        'jig': ['jig_dotted_quarter_chords', 'oom_pah_pattern', 'even_beat_emphasis'],
        'hornpipe': ['hornpipe_deliberate_chords', 'oom_pah_pattern', 'root_fifth_power_chords'],
        'polka': ['polka_strong_bass_pattern', 'oom_pah_pattern', 'button_accordion_bass_chord'],
        'waltz': ['waltz_bass_chord_chord', 'long_note_harmony', 'phrase_ending_harmony_only'],
        'slip_jig': ['jig_dotted_quarter_chords', 'sparse_to_dense_progression'],
        'air': ['long_note_harmony', 'walking_bass_line', 'seventh_chord_color', 'countermelody_harmony']
    }
    
    if tune_type not in tune_mappings:
        raise ValueError(f"Unknown tune type: {tune_type}. Valid types: {list(tune_mappings.keys())}")
    
    return {name: HARMONY_TRANSFORMATIONS[name] for name in tune_mappings[tune_type]}

def get_harmony_for_context(context='session', intensity='minimal'):
    """
    Get appropriate harmony based on performance context and intensity level.
    
    Args:
        context: 'session', 'solo', or 'arranged'
        intensity: 'minimal', 'moderate', or 'full'
    
    Returns:
        Recommended harmony transformation name and prompt
    """
    import random
    
    context_intensity_map = {
        'session': {
            'minimal': ['session_appropriate_minimal', 'strategic_bass_notes', 'phrase_ending_harmony_only'],
            'moderate': ['fifth_drone_bass', 'even_beat_emphasis'],
            'full': ['root_fifth_power_chords', 'modal_drone_ambiguity']
        },
        'solo': {
            'minimal': ['strategic_bass_notes', 'long_note_harmony'],
            'moderate': ['oom_pah_pattern', 'root_fifth_power_chords', 'double_stop_style'],
            'full': ['solo_performance_fuller', 'walking_bass_line', 'countermelody_harmony']
        },
        'arranged': {
            'minimal': ['section_contrast_harmony', 'call_response_harmony'],
            'moderate': ['piano_accordion_vamping', 'button_accordion_bass_chord'],
            'full': ['arranged_ensemble_parts', 'quartal_voicing', 'seventh_chord_color']
        }
    }
    
    options = context_intensity_map.get(context, {}).get(intensity, ['fifth_drone_bass'])
    name = random.choice(options)
    return name, HARMONY_TRANSFORMATIONS[name]

def get_progressive_harmony_sequence(num_repeats=4):
    """
    Get a sequence of progressively fuller harmonizations for repeated sections.
    
    Args:
        num_repeats: Number of times section repeats (typically 2-4)
    
    Returns:
        List of (name, prompt) tuples in order of increasing density
    """
    
    progression_sequence = [
        'establishing_first_time',
        'moderate_second_time', 
        'full_final_time',
        'arranged_ensemble_parts'
    ]
    
    # Return appropriate number based on repeats
    selected = progression_sequence[:num_repeats]
    return [(name, HARMONY_TRANSFORMATIONS[name]) for name in selected]

# Example usage
if __name__ == "__main__":
    import random
    
    print("=== ABC Harmony Transformation Prompts ===\n")
    
    # Example 1: Get specific transformation
    print("1. Specific transformation (fifth_drone_bass):")
    print(HARMONY_TRANSFORMATIONS['fifth_drone_bass'])
    
    # Example 2: Random transformation
    print("\n2. Random harmony transformation:")
    name, prompt = get_random_harmony_transformation()
    print(f"Name: {name}")
    print(f"Prompt: {prompt}")
    
    # Example 3: Get transformations by category
    print("\n3. All voicing-based transformations:")
    voicings = get_harmony_by_category('voicing')
    for name in voicings:
        print(f"  - {name}")
    
    # Example 4: Get appropriate harmony for tune type
    print("\n4. Harmony for reel:")
    reel_harmonies = get_harmony_for_tune_type('reel')
    for name in reel_harmonies:
        print(f"  - {name}")
    
    # Example 5: Get harmony for context
    print("\n5. Harmony for solo performance, full intensity:")
    name, prompt = get_harmony_for_context(context='solo', intensity='full')
    print(f"Name: {name}")
    print(f"Prompt: {prompt}")
    
    # Example 6: Progressive sequence
    print("\n6. Progressive harmony sequence for 3 repeats:")
    sequence = get_progressive_harmony_sequence(num_repeats=3)
    for i, (name, prompt) in enumerate(sequence, 1):
        print(f"  Repeat {i}: {name}")
    
    print("\n7. All available categories:")
    categories = ['voicing', 'rhythm', 'drone', 'texture', 'bellows', 
                  'advanced', 'modal', 'regional', 'context', 'fiddle',
                  'accordion', 'intensity', 'special']
    for cat in categories:
        count = len(get_harmony_by_category(cat))
        print(f"  - {cat}: {count} transformations")