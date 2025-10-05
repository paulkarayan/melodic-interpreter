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
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from core import harmony, melodic, session_scraper, melodic_transformations, harmony_transformations, ornamentation_transformations
from core.melodic import _diff_abc_bars

app = FastAPI(title="Irish Tune Variation Generator")

# Mount static files
app.mount("/shared", StaticFiles(directory="shared"), name="shared")

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
    """Serve the main landing page"""
    return FileResponse('index.html')

@app.get("/index.html", response_class=HTMLResponse)
async def index_html():
    """Serve the main landing page"""
    return FileResponse('index.html')

@app.get("/melody.html", response_class=HTMLResponse)
async def melody():
    """Serve melodic variations page"""
    return FileResponse('melody.html')

@app.get("/harmony.html", response_class=HTMLResponse)
async def harmony():
    """Serve harmony page"""
    return FileResponse('harmony.html')

@app.get("/session.html", response_class=HTMLResponse)
async def session():
    """Serve session analysis page"""
    return FileResponse('session.html')

@app.get("/melody-prompt.html", response_class=HTMLResponse)
async def melody_prompt():
    """Serve AI melodic transformations page"""
    return FileResponse('melody-prompt.html')

@app.get("/ornamentation.html", response_class=HTMLResponse)
async def ornamentation_page():
    """Serve ornamentation page"""
    return FileResponse('ornamentation.html')

@app.get("/ornamentation-prompt.html", response_class=HTMLResponse)
async def ornamentation_prompt():
    """Serve AI ornamentation transformations page"""
    return FileResponse('ornamentation-prompt.html')



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


class MelodyTransformRequest(BaseModel):
    abc: str
    transformation: str


class MelodyTransformLuckyRequest(BaseModel):
    abc: str


class SessionVariationAnalysisRequest(BaseModel):
    url: str


class OrnamentationRequest(BaseModel):
    abc: str
    ornamentation_type: str


@app.post("/transform-melody")
async def transform_melody(req: MelodyTransformRequest):
    """Transform melody using AI with specific transformation technique"""

    if not ANTHROPIC_AVAILABLE:
        return {
            'error': 'Anthropic API not available',
            'message': 'Set ANTHROPIC_API_KEY environment variable and install anthropic package'
        }

    if req.transformation not in melodic_transformations.TRANSFORMATIONS:
        return {
            'error': 'Invalid transformation',
            'message': f'Transformation "{req.transformation}" not found'
        }

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        prompt = f"""Given this ABC notation for an Irish tune:

{req.abc}

{melodic_transformations.TRANSFORMATIONS[req.transformation]}

Return your response in this exact JSON format:
{{
  "abc": "the transformed ABC notation here",
  "explanation": "2-3 sentence explanation of what specific musical changes you made (e.g., which notes were altered, which intervals changed, what rhythmic modifications occurred, etc.)"
}}

IMPORTANT: Return ONLY valid JSON, nothing else."""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
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
        result = json.loads(response_text)

        transformed_abc = result.get('abc', '')
        explanation = result.get('explanation', '')

        # Extract description from the prompt (first line)
        description = melodic_transformations.TRANSFORMATIONS[req.transformation].split('\n')[1].replace('Transform this ABC notation by ', '').replace(':', '')

        # Diff to find changed bars
        changed_bars = _diff_abc_bars(req.abc, transformed_abc, 5)

        return {
            'original': req.abc,
            'transformed_abc': transformed_abc,
            'transformation': req.transformation,
            'description': description,
            'explanation': explanation,
            'changed_bars': changed_bars
        }

    except Exception as e:
        return {
            'error': str(e),
            'message': 'Failed to generate melody transformation'
        }


@app.post("/transform-melody-lucky")
async def transform_melody_lucky(req: MelodyTransformLuckyRequest):
    """Generate 5 random melody transformations"""

    if not ANTHROPIC_AVAILABLE:
        return {
            'error': 'Anthropic API not available',
            'message': 'Set ANTHROPIC_API_KEY environment variable and install anthropic package'
        }

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        # Get 5 random transformations
        selected = melodic_transformations.get_random_transformations(5)
        transformations = []

        for transformation_name in selected:
            prompt = f"""Given this ABC notation for an Irish tune:

{req.abc}

{melodic_transformations.TRANSFORMATIONS[transformation_name]}

Return your response in this exact JSON format:
{{
  "abc": "the transformed ABC notation here",
  "explanation": "2-3 sentence explanation of what specific musical changes you made"
}}

IMPORTANT: Return ONLY valid JSON, nothing else."""

            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
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
            result = json.loads(response_text)
            transformed_abc = result.get('abc', '')
            explanation = result.get('explanation', '')

            # Extract description from the prompt
            description = melodic_transformations.TRANSFORMATIONS[transformation_name].split('\n')[1].replace('Transform this ABC notation by ', '').replace(':', '')

            # Diff to find changed bars
            changed_bars = _diff_abc_bars(req.abc, transformed_abc, 5)

            transformations.append({
                'name': transformation_name,
                'abc': transformed_abc,
                'description': description,
                'explanation': explanation,
                'changed_bars': changed_bars
            })

        return {
            'original': req.abc,
            'transformations': transformations
        }

    except Exception as e:
        return {
            'error': str(e),
            'message': 'Failed to generate melody transformations'
        }


@app.post("/analyze-session-variations")
async def analyze_session_variations(req: SessionVariationAnalysisRequest):
    """Analyze variations from The Session and create narrative analysis"""

    if not ANTHROPIC_AVAILABLE:
        return {
            'error': 'Anthropic API not available',
            'message': 'Set ANTHROPIC_API_KEY environment variable and install anthropic package'
        }

    try:
        # Fetch tune data from The Session
        tune_data = session_scraper.fetch_tune_from_session(req.url)

        if not tune_data['settings'] or len(tune_data['settings']) < 2:
            return {
                'error': 'Not enough variations',
                'message': 'This tune needs at least 2 settings for analysis'
            }

        # Get all ABC settings
        settings = tune_data['settings']

        # Build prompt for AI analysis
        prompt = f"""You are analyzing variations of the Irish tune "{tune_data['title']}" ({tune_data['type']} in {tune_data['key']}).

Here are {len(settings)} different settings/versions of this tune from The Session:

"""

        for i, setting in enumerate(settings, 1):
            prompt += f"\n--- Setting {i} ---\n{setting}\n"

        prompt += """
Analyze these variations and write a narrative analysis (3-4 paragraphs) describing:

1. What variation techniques are being used across these settings (e.g., neighbor tones, phrase ending changes, rhythmic variations, octave displacement, intervallic changes, etc.)

2. Specific examples of how musicians vary this tune - point to specific bars or phrases and describe the differences

3. Common patterns - which parts of the tune stay consistent vs. which parts show more variation

4. The overall character and style of variation for this tune

Write in an engaging, educational tone suitable for musicians learning about variation techniques. Be specific and reference actual musical content from the settings.

After your narrative analysis, provide 3-5 musical examples in this exact JSON format:

{
  "narrative": "your narrative text here",
  "examples": [
    {
      "title": "Example 1: Phrase Ending Variation",
      "description": "Brief description of what this example demonstrates",
      "abc": "valid ABC notation showing just the relevant bars"
    }
  ]
}

IMPORTANT: Return ONLY valid JSON, nothing else."""

        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

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
        analysis = json.loads(response_text)

        return {
            'title': tune_data['title'],
            'type': tune_data['type'],
            'key': tune_data['key'],
            'num_settings': len(settings),
            'narrative': analysis.get('narrative', ''),
            'examples': analysis.get('examples', [])
        }

    except Exception as e:
        import traceback
        print(f"[ERROR] {traceback.format_exc()}")
        return {
            'error': str(e),
            'message': 'Failed to analyze session variations'
        }


@app.post("/transform-harmony")
async def transform_harmony(req: MelodyTransformRequest):
    """Transform harmony using AI with specific harmony technique"""

    if not ANTHROPIC_AVAILABLE:
        return {
            'error': 'Anthropic API not available. Set ANTHROPIC_API_KEY environment variable.'
        }

    if req.transformation not in harmony_transformations.HARMONY_TRANSFORMATIONS:
        return {
            'error': f'Transformation "{req.transformation}" not found'
        }

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        prompt = f"""Given this ABC notation for an Irish tune:

{req.abc}

{harmony_transformations.HARMONY_TRANSFORMATIONS[req.transformation]}

Return your response in this exact JSON format:
{{
  "abc": "the transformed ABC notation with harmonic accompaniment here",
  "explanation": "2-3 sentence explanation of what specific harmonic changes you made (e.g., which harmony notes were added, what voicings used, what rhythmic placement, etc.)"
}}

IMPORTANT: Return ONLY valid JSON, nothing else."""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
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
        result = json.loads(response_text)

        transformed_abc = result.get('abc', '')
        explanation = result.get('explanation', '')

        # Extract description from the prompt (first line)
        prompt_lines = harmony_transformations.HARMONY_TRANSFORMATIONS[req.transformation].split('\n')
        description = prompt_lines[1] if len(prompt_lines) > 1 else req.transformation.replace('_', ' ').title()
        description = description.replace('Transform this ABC notation by ', '').replace(':', '')

        # Diff to find changed bars
        changed_bars = _diff_abc_bars(req.abc, transformed_abc, 5)

        return {
            'original': req.abc,
            'transformed_abc': transformed_abc,
            'transformation': req.transformation,
            'description': description,
            'explanation': explanation,
            'changed_bars': changed_bars
        }

    except Exception as e:
        return {
            'error': str(e)
        }


@app.post("/transform-harmony-lucky")
async def transform_harmony_lucky(req: MelodyTransformLuckyRequest):
    """Generate 5 random harmony transformations"""

    if not ANTHROPIC_AVAILABLE:
        return {
            'error': 'Anthropic API not available. Set ANTHROPIC_API_KEY environment variable.'
        }

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        # Get 5 random harmony transformations
        transformation_names = harmony_transformations.get_all_harmony_transformation_names()
        selected = random.sample(transformation_names, min(5, len(transformation_names)))
        transformations = []

        for transformation_name in selected:
            prompt = f"""Given this ABC notation for an Irish tune:

{req.abc}

{harmony_transformations.HARMONY_TRANSFORMATIONS[transformation_name]}

Return your response in this exact JSON format:
{{
  "abc": "the transformed ABC notation with harmonic accompaniment here",
  "explanation": "2-3 sentence explanation of what specific harmonic changes you made"
}}

IMPORTANT: Return ONLY valid JSON, nothing else."""

            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
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
            result = json.loads(response_text)
            transformed_abc = result.get('abc', '')
            explanation = result.get('explanation', '')

            # Extract description from the prompt
            prompt_lines = harmony_transformations.HARMONY_TRANSFORMATIONS[transformation_name].split('\n')
            description = prompt_lines[1] if len(prompt_lines) > 1 else transformation_name.replace('_', ' ').title()
            description = description.replace('Transform this ABC notation by ', '').replace(':', '')

            # Diff to find changed bars
            changed_bars = _diff_abc_bars(req.abc, transformed_abc, 5)

            transformations.append({
                'name': transformation_name,
                'abc': transformed_abc,
                'description': description,
                'explanation': explanation,
                'changed_bars': changed_bars
            })

        return {
            'original': req.abc,
            'transformations': transformations
        }

    except Exception as e:
        return {
            'error': str(e)
        }


@app.post("/transform-ornamentation")
async def transform_ornamentation(req: MelodyTransformRequest):
    """Transform by adding ornamentation using AI with specific technique"""

    if not ANTHROPIC_AVAILABLE:
        return {
            'error': 'Anthropic API not available. Set ANTHROPIC_API_KEY environment variable.'
        }

    if req.transformation not in ornamentation_transformations.ORNAMENTATION_TRANSFORMATIONS:
        return {
            'error': f'Transformation "{req.transformation}" not found'
        }

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        prompt = f"""Given this ABC notation for an Irish tune:

{req.abc}

{ornamentation_transformations.ORNAMENTATION_TRANSFORMATIONS[req.transformation]}

Return your response in this exact JSON format:
{{
  "abc": "the transformed ABC notation with ornamentation added here",
  "explanation": "2-3 sentence explanation of what specific ornamentation you added (e.g., which ornament types, where placed, what musical effect created, etc.)"
}}

IMPORTANT: Return ONLY valid JSON, nothing else."""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
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
        result = json.loads(response_text)

        transformed_abc = result.get('abc', '')
        explanation = result.get('explanation', '')

        # Extract description from the prompt (first line)
        prompt_lines = ornamentation_transformations.ORNAMENTATION_TRANSFORMATIONS[req.transformation].split('\n')
        description = prompt_lines[1] if len(prompt_lines) > 1 else req.transformation.replace('_', ' ').title()
        description = description.replace('Transform this ABC notation by ', '').replace(':', '')

        # Diff to find changed bars
        changed_bars = _diff_abc_bars(req.abc, transformed_abc, 5)

        return {
            'original': req.abc,
            'transformed_abc': transformed_abc,
            'transformation': req.transformation,
            'description': description,
            'explanation': explanation,
            'changed_bars': changed_bars
        }

    except Exception as e:
        return {
            'error': str(e)
        }


@app.post("/transform-ornamentation-lucky")
async def transform_ornamentation_lucky(req: MelodyTransformLuckyRequest):
    """Generate 5 random ornamentation transformations"""

    if not ANTHROPIC_AVAILABLE:
        return {
            'error': 'Anthropic API not available. Set ANTHROPIC_API_KEY environment variable.'
        }

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        # Get 5 random ornamentation transformations
        transformation_names = ornamentation_transformations.get_all_ornamentation_transformation_names()
        selected = random.sample(transformation_names, min(5, len(transformation_names)))
        transformations = []

        for transformation_name in selected:
            prompt = f"""Given this ABC notation for an Irish tune:

{req.abc}

{ornamentation_transformations.ORNAMENTATION_TRANSFORMATIONS[transformation_name]}

Return your response in this exact JSON format:
{{
  "abc": "the transformed ABC notation with ornamentation added here",
  "explanation": "2-3 sentence explanation of what specific ornamentation you added"
}}

IMPORTANT: Return ONLY valid JSON, nothing else."""

            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
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
            result = json.loads(response_text)
            transformed_abc = result.get('abc', '')
            explanation = result.get('explanation', '')

            # Extract description from the prompt
            prompt_lines = ornamentation_transformations.ORNAMENTATION_TRANSFORMATIONS[transformation_name].split('\n')
            description = prompt_lines[1] if len(prompt_lines) > 1 else transformation_name.replace('_', ' ').title()
            description = description.replace('Transform this ABC notation by ', '').replace(':', '')

            # Diff to find changed bars
            changed_bars = _diff_abc_bars(req.abc, transformed_abc, 5)

            transformations.append({
                'name': transformation_name,
                'abc': transformed_abc,
                'description': description,
                'explanation': explanation,
                'changed_bars': changed_bars
            })

        return {
            'original': req.abc,
            'transformations': transformations
        }

    except Exception as e:
        return {
            'error': str(e)
        }


@app.post("/add-ornamentation")
async def add_ornamentation(req: OrnamentationRequest):
    """Add ornamentation to ABC notation (placeholder for future implementation)"""

    # TODO: Implement ornamentation logic
    # For now, return the original ABC unchanged
    return {
        'original': req.abc,
        'ornamented': req.abc,
        'description': f'{req.ornamentation_type}: Ornamentation will be added here',
        'changed_bars': []
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
