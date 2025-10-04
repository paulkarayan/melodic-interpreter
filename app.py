"""
FastAPI backend for Irish tune variation generator
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import random
import os

from core import harmony, melodic, session_scraper

app = FastAPI(title="Irish Tune Variation Generator")

# Check for Anthropic API key
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if ANTHROPIC_API_KEY:
    try:
        import anthropic
        ANTHROPIC_AVAILABLE = True
    except ImportError:
        ANTHROPIC_AVAILABLE = False
else:
    ANTHROPIC_AVAILABLE = False


class VariationRequest(BaseModel):
    abc: str
    harmony_type: str = 'none'
    melodic_type: str = 'none'
    lick: Optional[str] = None
    validate_anglo: bool = False


class FeelingLuckyRequest(BaseModel):
    abc: str
    validate_anglo: bool = False


class SessionRequest(BaseModel):
    url: str


@app.get("/", response_class=HTMLResponse)
async def index():
    """Serve the main HTML page"""
    return FileResponse('variations_enhanced.html')


@app.post("/generate")
async def generate_variations(req: VariationRequest):
    """Generate harmony and melodic variations"""

    print(f"\n[API /generate] Request received:")
    print(f"  - harmony_type: {req.harmony_type}")
    print(f"  - melodic_type: {req.melodic_type}")
    print(f"  - lick: {req.lick}")
    print(f"  - ABC length: {len(req.abc)} chars")

    results = {'original': req.abc}

    # Handle "feeling lucky" for harmony
    if req.harmony_type == 'feeling_lucky':
        harmony_types = list(harmony.HARMONY_FUNCTIONS.keys())
        # Use random.sample to ensure no duplicates
        selected_types = random.sample(harmony_types, min(5, len(harmony_types)))
        variations = []
        for h_type in selected_types:
            variation = harmony.HARMONY_FUNCTIONS[h_type](req.abc)
            variations.append({
                'abc': variation,
                'description': harmony.HARMONY_DESCRIPTIONS[h_type]
            })
        results['harmony_lucky'] = variations
        return results

    # Handle "feeling lucky" for melodic
    if req.melodic_type == 'feeling_lucky':
        melodic_types = list(melodic.MELODIC_DESCRIPTIONS.keys())
        # Use random.sample to ensure no duplicates
        selected_types = random.sample(melodic_types, min(5, len(melodic_types)))
        variations = []
        for m_type in selected_types:
            variation, m_desc, changed_bars = melodic.apply_melodic_multiple(req.abc, m_type, req.lick)
            variations.append({
                'abc': variation,
                'description': f"{melodic.MELODIC_DESCRIPTIONS[m_type]} - {m_desc}",
                'changed_bars': changed_bars
            })
        results['melodic_lucky'] = variations
        return results

    # Generate harmony variation
    if req.harmony_type and req.harmony_type != 'none' and req.harmony_type in harmony.HARMONY_FUNCTIONS:
        print(f"[API] Generating harmony variation: {req.harmony_type}")
        harmony_fn = harmony.HARMONY_FUNCTIONS[req.harmony_type]
        results['harmony'] = harmony_fn(req.abc)
        results['harmony_desc'] = harmony.HARMONY_DESCRIPTIONS[req.harmony_type]
        print(f"[API] Harmony generated: {len(results['harmony'])} chars")

    # Generate melodic variation
    if req.melodic_type and req.melodic_type != 'none':
        print(f"[API] Generating melodic variation: {req.melodic_type}")
        melodic_abc, melodic_desc, changed_bars = melodic.apply_melodic_multiple(
            req.abc, req.melodic_type, req.lick
        )
        results['melodic'] = melodic_abc
        results['melodic_desc'] = (
            f"{melodic.MELODIC_DESCRIPTIONS[req.melodic_type]} - {melodic_desc}"
        )
        results['melodic_changed_bars'] = changed_bars
        print(f"[API] Melodic generated: {len(melodic_abc)} chars, {len(changed_bars)} bars changed")

    # Combined variation
    if (req.harmony_type and req.harmony_type != 'none' and
        req.melodic_type and req.melodic_type != 'none'):
        print(f"[API] Generating combined variation")
        # Apply harmony first
        combined = harmony.HARMONY_FUNCTIONS[req.harmony_type](req.abc)
        # Then melodic
        combined, melodic_desc, combined_changed = melodic.apply_melodic_multiple(
            combined, req.melodic_type, req.lick
        )
        results['combined'] = combined
        results['combined_desc'] = f"{melodic_desc}"
        results['combined_changed_bars'] = combined_changed
        print(f"[API] Combined generated: {len(combined)} chars")

    # TODO: Validate anglo playability if requested

    print(f"[API] Response keys: {list(results.keys())}")
    return results


@app.post("/feeling-lucky")
async def feeling_lucky(req: FeelingLuckyRequest):
    """Generate 5 random variation combinations"""

    harmony_types = list(harmony.HARMONY_FUNCTIONS.keys())
    melodic_types = list(melodic.MELODIC_DESCRIPTIONS.keys())

    variations = []
    used_combinations = set()

    attempts = 0
    max_attempts = 50  # Prevent infinite loop

    while len(variations) < 5 and attempts < max_attempts:
        h_type = random.choice(harmony_types)
        m_type = random.choice(melodic_types)
        combo_key = f"{h_type}:{m_type}"

        # Skip if we've already used this combination
        if combo_key in used_combinations:
            attempts += 1
            continue

        used_combinations.add(combo_key)

        # Apply harmony
        variation = harmony.HARMONY_FUNCTIONS[h_type](req.abc)
        # Apply melodic (with changed bars info)
        variation, m_desc, changed_bars = melodic.apply_melodic_multiple(variation, m_type, None)

        variations.append({
            'abc': variation,
            'description': (
                f"{harmony.HARMONY_DESCRIPTIONS[h_type]} + "
                f"{melodic.MELODIC_DESCRIPTIONS[m_type]} ({m_desc})"
            )
        })
        attempts += 1

    return {'variations': variations}


@app.post("/analyze-session")
async def analyze_session(req: SessionRequest):
    """Analyze variations from The Session"""
    try:
        # Fetch tune data from The Session
        tune_data = session_scraper.fetch_tune_from_session(req.url)

        # Compare variations
        if tune_data['settings']:
            comparison = session_scraper.compare_variations(tune_data['settings'])
        else:
            comparison = {
                'num_variations': 0,
                'message': 'No ABC settings found on this page'
            }

        return {
            'title': tune_data['title'],
            'type': tune_data['type'],
            'key': tune_data['key'],
            'num_settings': tune_data['num_settings'],
            'settings': tune_data['settings'],
            'comparison': comparison
        }

    except Exception as e:
        return {
            'error': str(e),
            'message': 'Failed to analyze Session URL'
        }


class StyleTransformRequest(BaseModel):
    abc: str
    styles: List[str]  # List of style names to generate


@app.post("/transform-styles")
async def transform_styles(req: StyleTransformRequest):
    """Transform tune into different musical styles using LLM"""

    if not ANTHROPIC_AVAILABLE:
        return {
            'error': 'Anthropic API not available',
            'message': 'Set ANTHROPIC_API_KEY environment variable and install anthropic package'
        }

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        # Style transformation prompts
        STYLE_PROMPTS = {
            'drone_minimalist': """Transform this Irish tune into a drone minimalist style:
- Add sustained drone notes (A and D pedal tones)
- Simplify melody to essential notes only
- Stretch out rhythm (longer note values)
- Remove ornamentation
- Create meditative, spacious feel
Return only the modified ABC notation.""",

            'groove_fusion': """Transform this Irish tune into a groove fusion style:
- Add syncopated rhythms
- Include chromatic passing tones
- Add jazz-influenced harmony (quartal chords)
- Emphasize strong beats with double stops
- Make it groovier and funkier
Return only the modified ABC notation.""",

            'ambient_chamber': """Transform this Irish tune into an ambient chamber style:
- Add lush harmonic thirds and sixths throughout
- Use wide intervals and open voicings
- Add countermelody in contrary motion
- Create textural depth with multiple voices
- Ethereal and atmospheric
Return only the modified ABC notation.""",

            'bebop_jazz': """Transform this Irish tune into a bebop jazz style:
- Add chromatic approach notes
- Use rhythmic displacement and syncopation
- Include altered notes (chromatic passing tones)
- Add jazz articulation
- Swing feel
Return only the modified ABC notation.""",

            'baroque': """Transform this Irish tune into a baroque style:
- Add counterpoint and imitative voices
- Use baroque ornamentation (trills, mordents)
- Create harmonic sequences
- Add bass line with walking motion
- Classical elegance
Return only the modified ABC notation."""
        }

        transformations = []

        for style in req.styles:
            if style not in STYLE_PROMPTS:
                continue

            prompt = f"""Given this ABC notation for an Irish tune:

{req.abc}

{STYLE_PROMPTS[style]}

Important: Return ONLY valid ABC notation, nothing else. Keep the same headers (X:, T:, M:, L:, R:, K:) and only modify the musical content."""

            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            transformed_abc = message.content[0].text.strip()

            # Clean up any markdown code blocks if present
            if transformed_abc.startswith('```'):
                lines = transformed_abc.split('\n')
                transformed_abc = '\n'.join(lines[1:-1]) if len(lines) > 2 else transformed_abc

            transformations.append({
                'style': style,
                'abc': transformed_abc,
                'description': STYLE_PROMPTS[style].split('\n')[0].replace('Transform this Irish tune into a ', '').replace(':', '')
            })

        return {
            'original': req.abc,
            'transformations': transformations
        }

    except Exception as e:
        return {
            'error': str(e),
            'message': 'Failed to generate style transformations'
        }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
