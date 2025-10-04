# Functions and Resources Needed

## Summary
This document outlines all the functions and resources needed to build the full Irish tune variation generator with FastAPI backend.

---

## 1. Core ABC Manipulation (`core/abc_utils.py`)

### ✅ Already Working (from HTML)
- `parse_abc(abc_string)` - Parse headers and body
- `rebuild_abc(headers, body)` - Reconstruct ABC notation
- `get_bars(body, count)` - Extract specific bars

### 🔧 Need to Implement
- `find_lick_in_tune(body, lick_pattern)` - Find all occurrences of a specific lick
- `validate_abc_syntax(abc_string)` - Basic ABC syntax validation
- `transpose_abc(abc_string, semitones)` - Transpose to different key

---

## 2. Harmony Generation (`core/harmony.py`)

### ✅ Already Working (from HTML)
- `apply_quartal_sparse(abc)` - Quartal harmony on beats 1 & 5
- `apply_quartal_two(abc)` - Two-note quartal fourths
- `apply_modal_drone(abc)` - Static drone underneath
- `apply_diatonic_thirds(abc)` - Traditional thirds harmony
- `apply_open_fifths(abc)` - Open fifth intervals

### 🔧 Need to Implement
- `validate_harmony_playability(chords)` - Check against Anglo impossible pairs
- `suggest_alternative_voicing(chord)` - If unplayable, suggest alternative
- `apply_harmony_to_full_tune(abc, harmony_type)` - Apply to entire tune, not just first bar

---

## 3. Melodic Variations (`core/melodic.py`)

### ✅ Already Working (from HTML)
- `apply_chromatic_passing(bar)` - Add chromatic notes
- `apply_neighbor_tones(bar)` - Neighbor tone substitution
- `apply_octave_displacement(bar)` - Move to different octave
- `apply_rhythmic_shift(bar)` - Rhythmic displacement
- `apply_simplification(bar)` - Reduce notes

### 🔧 Need to Implement
- `apply_melodic_multiple(abc, variation_type, lick=None, num_spots=None)` - Apply to 2-5 places
- `identify_variation_candidates(abc)` - Find good spots for variation
- `apply_to_specific_lick(abc, lick_pattern, variation_type)` - Target specific lick

---

## 4. Anglo Concertina Validation (`core/validator.py`)

### 🔧 Need to Implement (CRITICAL)
- `load_impossible_pairs()` - Load the impossible note combinations from ANGLO_CONSTRAINTS.md
- `validate_chord(notes)` - Check if chord is playable
- `validate_abc_playability(abc_string)` - Check entire tune
- `get_impossible_pairs_in_chord(notes)` - Return which pairs are impossible
- `suggest_playable_alternative(notes)` - Suggest closest playable chord

---

## 5. The Session Integration (`core/session_scraper.py`)

### 🔧 Need to Implement (CRITICAL)
- `fetch_tune_from_session(url)` - Scrape The Session page
- `extract_all_abc_settings(html)` - Get all ABC variations from page
- `extract_tune_metadata(html)` - Get title, key, meter, etc.
- `compare_variations(abc_list)` - Identify differences between settings
- `find_unique_approaches(abc_list)` - Find novel variation techniques
- `generate_variation_heatmap(abc_list)` - Show which bars vary most

---

## 6. Transformation Prompts (`core/transformations.py`)

### 🔧 Need to Implement (OPTIONAL - for later)
- `load_transformation_prompts()` - Load from transformation_prompts.py
- `apply_llm_transformation(abc, style_prompt)` - Call LLM API for style transformation
- `parse_llm_response(response)` - Extract ABC from LLM response

---

## 7. FastAPI Backend (`app.py`)

### 🔧 Need to Implement
```python
# Endpoints needed:

POST /generate
- Input: abc, harmony_type, melodic_type, lick, validate_anglo
- Output: original, harmony, melodic, combined (all as ABC strings)

POST /feeling-lucky
- Input: abc, validate_anglo
- Output: 5 random variation combinations

POST /session-analyze
- Input: session_url
- Output: all ABC settings, comparison data, suggested variations

GET /health
- Health check endpoint
```

---

## 8. HTML/Frontend (`templates/index.html`)

### ✅ Already Complete
- variations_enhanced.html has all UI features working

---

## Priority Order for Implementation

### 🟢 **Phase 1: Get Basic Backend Working**
1. `core/abc_utils.py` - Core ABC manipulation
2. `core/harmony.py` - Harmony generation (port from HTML)
3. `core/melodic.py` - Melodic variations (port from HTML)
4. `app.py` - FastAPI with `/generate` endpoint
5. Test with existing HTML frontend

### 🟡 **Phase 2: Add Advanced Features**
6. `core/validator.py` - Anglo playability validation
7. Update `core/harmony.py` to use validator
8. Add `/feeling-lucky` endpoint
9. Implement multi-spot melodic variations

### 🔴 **Phase 3: Session Integration**
10. `core/session_scraper.py` - The Session scraping
11. Add `/session-analyze` endpoint
12. Update frontend to display Session analysis

### 🟣 **Phase 4: LLM Transformations (Optional)**
13. `core/transformations.py` - Style transformation with LLM
14. Add transformation endpoints

---

## Which Functions Should We Build First?

**Recommend starting with Phase 1:**

1. Create `core/abc_utils.py` with basic functions
2. Port harmony functions from HTML to Python (`core/harmony.py`)
3. Port melodic functions from HTML to Python (`core/melodic.py`)
4. Create FastAPI app with `/generate` endpoint
5. Test with the existing `variations_enhanced.html`

**This gives you a working end-to-end system quickly.**

Then we can add:
- Anglo validation (Phase 2)
- Session scraping (Phase 3)
- LLM transformations (Phase 4)

**What do you want to tackle first?**
