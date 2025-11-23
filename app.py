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
import re
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from core import harmony, melodic, session_scraper, melodic_transformations, harmony_transformations, ornamentation_transformations, reharmonization, harmoniser, repetition_detector, brenda_variations, abc_transpose, skeletal_analysis
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
    target_repetition: bool = False
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


@app.get("/reharmonize.html", response_class=HTMLResponse)
async def reharmonize_page():
    """Serve reharmonization analysis page"""
    return FileResponse('reharmonize.html')


@app.get("/harmoniser.html", response_class=HTMLResponse)
async def harmoniser_page():
    """Serve Anglo concertina harmoniser page"""
    return FileResponse('harmoniser.html')


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

        # Handle "All of the Above" - apply all variations
        if req.melodic_type == 'all_variations':
            # Handle target repetition for all variations
            lick_to_use = req.lick
            repetition_info = None

            if req.target_repetition and not req.lick:
                print("[API] Using target repetition mode")
                repetition_info = repetition_detector.detect_repetition(req.abc)
                results['repetition_info'] = repetition_info

                if repetition_info['has_repetition']:
                    target_licks = repetition_detector.get_target_licks(req.abc)
                    if target_licks:
                        lick_to_use = target_licks[0]
                        print(f"[API] Auto-detected lick: {lick_to_use}")

            # Apply all melodic variations to the lick
            all_melodic_types = list(melodic.MELODIC_DESCRIPTIONS.keys())
            variations = []
            all_changed_bars = []

            for m_type in all_melodic_types:
                variation_abc, variation_desc, changed_bars = melodic.apply_melodic_multiple(
                    req.abc, m_type, lick_to_use
                )
                variations.append({
                    'abc': variation_abc,
                    'type': m_type,
                    'description': f"{melodic.MELODIC_DESCRIPTIONS[m_type]} - {variation_desc}",
                    'changed_bars': changed_bars
                })
                all_changed_bars.extend(changed_bars)

            # Return all variations
            results['melodic_all_variations'] = variations
            results['melodic_desc'] = f"All variations applied to the repeated lick ({len(variations)} variations)"
            results['melodic_changed_bars'] = all_changed_bars
            print(f"[API] Generated {len(variations)} variations")

        else:
            # Handle target repetition
            lick_to_use = req.lick
            repetition_info = None

            if req.target_repetition and not req.lick:
                print("[API] Using target repetition mode")
                repetition_info = repetition_detector.detect_repetition(req.abc)
                results['repetition_info'] = repetition_info

                if repetition_info['has_repetition']:
                    # Get the best repeated lick to target
                    target_licks = repetition_detector.get_target_licks(req.abc)
                    if target_licks:
                        lick_to_use = target_licks[0]  # Use the most repeated one
                        print(f"[API] Auto-detected lick: {lick_to_use}")

            melodic_abc, melodic_desc, changed_bars = melodic.apply_melodic_multiple(
                req.abc, req.melodic_type, lick_to_use
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
                model="claude-sonnet-4-5-20250929",
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
    lick: Optional[str] = None
    target_repetition: bool = False


class MelodyTransformLuckyRequest(BaseModel):
    abc: str


class SessionVariationAnalysisRequest(BaseModel):
    url: str
    user_abc: Optional[str] = None


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

    # Special handling for "all_variations" - apply all transformations
    if req.transformation == 'all_variations':
        try:
            # Handle target repetition
            repetition_info = None
            lick_to_use = req.lick

            if req.target_repetition and not req.lick:
                repetition_info = repetition_detector.detect_repetition(req.abc)
                if repetition_info['has_repetition']:
                    target_licks = repetition_detector.get_target_licks(req.abc)
                    if target_licks:
                        lick_to_use = target_licks[0]

            # Apply all transformations
            all_variations = []
            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

            for transform_name, transform_prompt in melodic_transformations.TRANSFORMATIONS.items():
                lick_instruction = ""
                if lick_to_use:
                    lick_instruction = f"\nIMPORTANT: Apply this transformation ONLY to this specific pattern: {lick_to_use}\nDo NOT modify other parts of the tune."

                prompt = f"""Given this ABC notation for an Irish tune:

{req.abc}

{transform_prompt}{lick_instruction}

Return your response in this exact JSON format:
{{
  "abc": "the transformed ABC notation here",
  "explanation": "2-3 sentence explanation of what specific musical changes you made"
}}

IMPORTANT: Return ONLY valid JSON, nothing else."""

                message = client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=2000,
                    messages=[{"role": "user", "content": prompt}]
                )

                response_text = message.content[0].text.strip()
                if response_text.startswith('```json'):
                    response_text = response_text.replace('```json', '').replace('```', '').strip()
                elif response_text.startswith('```'):
                    response_text = response_text.replace('```', '').strip()

                import json
                result = json.loads(response_text)

                description = transform_prompt.split('\n')[1].replace('Transform this ABC notation by ', '').replace(':', '')
                changed_bars = _diff_abc_bars(req.abc, result.get('abc', ''), 5)

                all_variations.append({
                    'abc': result.get('abc', ''),
                    'type': transform_name,
                    'description': description,
                    'explanation': result.get('explanation', ''),
                    'changed_bars': changed_bars
                })

            response = {
                'original': req.abc,
                'all_variations': all_variations,
                'transformation': 'all_variations',
                'description': f'All {len(all_variations)} melodic transformations'
            }

            if repetition_info:
                response['repetition_info'] = repetition_info

            return response

        except Exception as e:
            return {
                'error': str(e),
                'message': 'Failed to generate all variations'
            }

    if req.transformation not in melodic_transformations.TRANSFORMATIONS:
        return {
            'error': 'Invalid transformation',
            'message': f'Transformation "{req.transformation}" not found'
        }

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        # Handle target repetition
        repetition_info = None
        lick_instruction = ""

        if req.target_repetition and not req.lick:
            repetition_info = repetition_detector.detect_repetition(req.abc)
            if repetition_info['has_repetition']:
                target_licks = repetition_detector.get_target_licks(req.abc)
                if target_licks:
                    lick_instruction = f"\nIMPORTANT: Apply this transformation ONLY to the following repeated pattern: {target_licks[0]}\nDo NOT modify other parts of the tune."
        elif req.lick:
            lick_instruction = f"\nIMPORTANT: Apply this transformation ONLY to this specific pattern: {req.lick}\nDo NOT modify other parts of the tune."

        prompt = f"""Given this ABC notation for an Irish tune:

{req.abc}

{melodic_transformations.TRANSFORMATIONS[req.transformation]}{lick_instruction}

Return your response in this exact JSON format:
{{
  "abc": "the transformed ABC notation here",
  "explanation": "2-3 sentence explanation of what specific musical changes you made (e.g., which notes were altered, which intervals changed, what rhythmic modifications occurred, etc.)"
}}

IMPORTANT: Return ONLY valid JSON, nothing else."""

        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
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

        response = {
            'original': req.abc,
            'transformed_abc': transformed_abc,
            'transformation': req.transformation,
            'description': description,
            'explanation': explanation,
            'changed_bars': changed_bars
        }

        # Add repetition info if available
        if repetition_info:
            response['repetition_info'] = repetition_info

        return response

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
                model="claude-sonnet-4-5-20250929",
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

        # Transpose all settings to user's key if provided
        user_key = None
        if req.user_abc:
            # Extract key from user ABC
            key_match = re.search(r'K:\s*([^\n]+)', req.user_abc)
            if key_match:
                # Strip whitespace and unprintable characters
                user_key = ''.join(c for c in key_match.group(1).strip() if c.isprintable()).strip()

        # Build prompt for AI analysis
        transpose_note = ""
        if user_key:
            transpose_note = f"""
CRITICAL: The user wants to work in {user_key}.
Before your analysis, transpose ALL {len(settings)} settings above to {user_key}.
Use the transposed versions for your analysis and examples.
"""

        prompt = f"""You are analyzing variations of the Irish tune "{tune_data['title']}" ({tune_data['type']} in {tune_data['key']}).

Here are ALL {len(settings)} different settings/versions of this tune from The Session:

"""

        for i, setting in enumerate(settings, 1):
            prompt += f"\n--- Setting {i} ---\n{setting}\n"

        prompt += f"""
{transpose_note}

Analyze these variations and write a narrative analysis (3-4 paragraphs) describing:

1. What variation techniques are being used across these settings (e.g., neighbor tones, phrase ending changes, rhythmic variations, octave displacement, intervallic changes, etc.)

2. Specific examples of how musicians vary this tune - point to specific bars or phrases and describe the differences

3. Common patterns - which parts of the tune stay consistent vs. which parts show more variation

4. The overall character and style of variation for this tune

Write in an engaging, educational tone suitable for musicians learning about variation techniques. Be specific and reference actual musical content from the settings.

After your narrative analysis, select UP TO 5 of the most interesting and pedagogically valuable settings as examples (choose 5 if available, fewer only if they're too similar):

{{
  "narrative": "your narrative text here",
  "examples": [
    {{
      "title": "Setting 1",
      "description": "Brief description of what variation technique this setting demonstrates",
      "abc": "COPY THE ENTIRE SETTING 1 ABC VERBATIM - every single character exactly as shown above",
      "setting_number": 1,
      "interesting_bars": [1, 3]
    }},
    {{
      "title": "Setting 3",
      "description": "Brief description of what variation technique this setting demonstrates",
      "abc": "COPY THE ENTIRE SETTING 3 ABC VERBATIM - every single character exactly as shown above",
      "setting_number": 3,
      "interesting_bars": [2, 5]
    }}
  ]
}}

CRITICAL REQUIREMENTS - READ CAREFULLY:
- Your examples MUST be literal copies of the settings shown above (Setting 1, Setting 2, Setting 3, etc.)
- For the "abc" field:
  * If user provided a key (e.g., K:Dmaj), transpose the ENTIRE setting to that key
  * Copy the complete transposed ABC notation (the octave will be verified programmatically)
  * If no key was specified, just copy the setting exactly as shown
- For the "title" field: Just use "Setting X" where X is the setting number you copied
- For the "description" field: Explain what variation technique THIS ACTUAL SETTING demonstrates
- For the "interesting_bars" field: List the bar numbers (1-indexed) that contain the most interesting variations worth highlighting. Include 2-4 bar numbers.
- The "setting_number" must match which setting you copied from the list above
- DO NOT create hybrid examples, DO NOT make up new variations
- Select UP TO 5 settings that best illustrate different variation techniques (only use fewer if the variations are too similar to warrant 5 examples)
- Use DOUBLE QUOTES for all strings, never single quotes
- NO trailing commas after the last item in arrays or objects
- Escape special characters in strings (use \\n for newlines in ABC notation)
- Return ONLY valid JSON that can be parsed by JSON.parse(), nothing else before or after
- DO NOT include any explanation, commentary, or text before the JSON object
- DO NOT explain your transposition process - just do it silently and return the JSON
- Your response must start with {{ and end with }}"""

        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=3000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        response_text = message.content[0].text.strip()
        print(f"[SESSION] AI Response length: {len(response_text)}")
        print(f"[SESSION] AI Response preview: {response_text[:200]}...")

        # Check if response is empty
        if not response_text:
            print("[ERROR] Empty response from AI")
            return {
                'error': 'Empty response from AI',
                'message': 'Failed to get AI response - the AI returned no content'
            }

        # Clean up markdown if present
        if '```json' in response_text:
            # Extract JSON from markdown code block
            start = response_text.find('```json') + 7
            end = response_text.find('```', start)
            response_text = response_text[start:end].strip()
        elif '```' in response_text:
            start = response_text.find('```') + 3
            end = response_text.find('```', start)
            response_text = response_text[start:end].strip()

        # If there's text before the JSON, extract just the JSON object
        if not response_text.startswith('{'):
            # Find the first { and extract from there
            json_start = response_text.find('{')
            if json_start != -1:
                response_text = response_text[json_start:]
                print(f"[SESSION] Extracted JSON from position {json_start}")
            else:
                print("[ERROR] No JSON object found in response")
                return {
                    'error': 'No JSON object found in AI response',
                    'message': 'The AI response did not contain valid JSON',
                    'debug_response': response_text[:500]
                }

        # Parse JSON response
        import json
        try:
            # Try to parse as-is first
            analysis = json.loads(response_text)
        except json.JSONDecodeError as je:
            # If it fails due to control characters, try to fix them
            print(f"[SESSION] First parse failed, attempting to fix control characters...")
            # Replace actual newlines in the narrative with escaped newlines
            # This is a bit hacky but handles the common case of unescaped newlines in strings
            # Find the narrative field and escape newlines within it
            response_text_fixed = re.sub(
                r'("narrative":\s*")([^"]*?)"',
                lambda m: m.group(1) + m.group(2).replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t') + '"',
                response_text,
                flags=re.DOTALL
            )
            try:
                analysis = json.loads(response_text_fixed)
                print(f"[SESSION] Successfully parsed after fixing control characters")
            except json.JSONDecodeError as je2:
                print(f"[ERROR] JSON Parse Error after fix attempt: {je2}")
                print(f"[ERROR] Response text (first 1000 chars):\n{response_text[:1000]}...")
                return {
                    'error': f'Invalid JSON format from AI: {str(je2)}',
                    'message': 'Failed to parse AI response',
                    'debug_response': response_text[:500]  # Include for debugging
                }

        # If user specified a key, verify octave register is correct
        examples = analysis.get('examples', [])
        if user_key and user_key != tune_data['key']:
            print(f"[SESSION] Verifying octave register for transposed examples")
            for i, example in enumerate(examples):
                if 'abc' in example and 'setting_number' in example:
                    setting_num = example['setting_number']
                    if 1 <= setting_num <= len(settings):
                        original_setting = settings[setting_num - 1]
                        ai_transposed = example['abc']
                        try:
                            # Correct octave register if AI got it wrong
                            corrected_abc = abc_transpose.correct_octave_register(original_setting, ai_transposed)
                            example['abc'] = corrected_abc
                            print(f"[SESSION] Verified octave for setting {setting_num}")
                        except Exception as e:
                            print(f"[SESSION] Failed to verify octave for setting {setting_num}: {e}")
                            # Keep AI version if correction fails

        return {
            'title': tune_data['title'],
            'type': tune_data['type'],
            'key': tune_data['key'],
            'num_settings': len(settings),
            'num_examples': len(examples),
            'narrative': analysis.get('narrative', ''),
            'examples': examples
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
            model="claude-sonnet-4-5-20250929",
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
                model="claude-sonnet-4-5-20250929",
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
            model="claude-sonnet-4-5-20250929",
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
                model="claude-sonnet-4-5-20250929",
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


@app.post("/reharmonize")
async def reharmonize_tune(req: MelodyTransformRequest):
    """Programmatic reharmonization using music theory"""
    try:
        result = reharmonization.reharmonize_abc(req.abc, num_alternatives=5)

        return {
            'original': req.abc,
            'transformed_abc': result['annotated_abc'],
            'transformation': 'reharmonize',
            'description': 'Programmatic chord analysis and substitution suggestions',
            'explanation': f'Analyzed melody in {result["key"]} and suggested {len(result["bar_analyses"])} chord options per bar',
            'bar_analyses': result['bar_analyses'],
        }

    except Exception as e:
        import traceback
        print(f"[ERROR] {traceback.format_exc()}")
        return {
            'error': str(e)
        }


class HarmoniserRequest(BaseModel):
    abc: str
    harmonic_rhythm: str
    layers: List[str]


@app.post("/harmonise")
async def harmonise_tune(req: HarmoniserRequest):
    """Generate Anglo concertina harmony using hybrid approach"""

    if not ANTHROPIC_AVAILABLE:
        return {
            'error': 'Anthropic API not available. Set ANTHROPIC_API_KEY environment variable.'
        }

    try:
        result = harmoniser.harmonise_abc(
            req.abc,
            harmonic_rhythm=req.harmonic_rhythm,
            layers=req.layers
        )

        return result

    except Exception as e:
        import traceback
        print(f"[ERROR] {traceback.format_exc()}")
        return {
            'error': str(e)
        }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}


# ============================================================================
# BRENDA CASTLES VARIATIONS ENDPOINTS
# ============================================================================

class BrendaDetectRequest(BaseModel):
    abc: str


class BrendaGenerateRequest(BaseModel):
    abc: str
    repetition_info: dict


class BrendaApplyRequest(BaseModel):
    abc: str
    repetition_info: dict
    variations: List[dict]


class SkeletalAnalysisRequest(BaseModel):
    abc: str
    session_url: Optional[str] = None
    complexity_level: int = 1  # 1 (simple), 2 (medium), 3 (complex)
    mir_weights: Optional[dict] = None  # Optional MIR feature weights


class SimpleAnalysisRequest(BaseModel):
    abc: str
    session_url: Optional[str] = None


@app.get("/brenda-variations.html", response_class=HTMLResponse)
async def brenda_variations_page():
    """Serve Brenda Castles variations page"""
    return FileResponse('brenda-variations.html')


@app.get("/skeletal.html", response_class=HTMLResponse)
async def skeletal_page():
    """Serve skeletal note analysis page"""
    return FileResponse('skeletal.html')


@app.get("/simple.html", response_class=HTMLResponse)
async def simple_page():
    """Serve simple skeletal analysis page"""
    return FileResponse('simple.html')


@app.post("/brenda/detect-repetition")
async def brenda_detect_repetition(req: BrendaDetectRequest):
    """Step 1: Detect repeated sections in the tune"""
    try:
        result = repetition_detector.detect_repetition(req.abc)
        return result
    except Exception as e:
        return {'error': str(e)}


@app.post("/brenda/generate-variations")
async def brenda_generate_variations(req: BrendaGenerateRequest):
    """Step 2: Generate variation ideas for repeated sections"""
    try:
        print(f"[BRENDA] generate-variations called")
        print(f"[BRENDA] repetition_info: {req.repetition_info}")
        variations = []

        # Generate variation ideas for each repeated phrase (prefer 2-bar, fallback to single measures)
        if req.repetition_info.get('repeated_phrases_2bar') and len(req.repetition_info['repeated_phrases_2bar']) > 0:
            print(f"[BRENDA] Found {len(req.repetition_info['repeated_phrases_2bar'])} 2-bar phrases")
            for phrase in req.repetition_info['repeated_phrases_2bar'][:3]:  # Top 3
                print(f"[BRENDA] Generating variations for: {phrase['original_text']}")
                # Generate all 8 variations (one per technique) for the entire phrase
                all_variations = brenda_variations.generate_variation_ideas(
                    phrase['original_text'],
                    num_ideas=8  # Get all 8 techniques
                )
                print(f"[BRENDA] Generated {len(all_variations)} variations")

                # Format as Option 1, Option 2, etc.
                ideas = []
                for idx, var in enumerate(all_variations):
                    ideas.append({
                        'abc': var['abc'],
                        'description': var['description'],
                        'technique_index': idx  # For re-rolling specific techniques
                    })

                # Format locations
                locations = ', '.join([f"Bar {i+1}" for i in phrase['occurrences']])

                variations.append({
                    'original': phrase['original_text'],
                    'locations': locations,
                    'ideas': ideas
                })
        elif req.repetition_info.get('repeated_measures'):
            # Fallback: use individual repeated measures
            print(f"[BRENDA] No 2-bar phrases found, using repeated measures instead")
            measures = repetition_detector.extract_measures_with_durations(req.abc)

            # Get top 3 most repeated measures
            measure_items = list(req.repetition_info['repeated_measures'].items())
            measure_items.sort(key=lambda x: len(x[1]), reverse=True)  # Sort by occurrence count

            for measure_content, indices in measure_items[:3]:
                # Get the actual measure text (non-normalized)
                original_text = measures[indices[0]]
                print(f"[BRENDA] Generating variations for measure: {original_text}")

                all_variations = brenda_variations.generate_variation_ideas(
                    original_text,
                    num_ideas=8
                )
                print(f"[BRENDA] Generated {len(all_variations)} variations")

                ideas = []
                for idx, var in enumerate(all_variations):
                    ideas.append({
                        'abc': var['abc'],
                        'description': var['description'],
                        'technique_index': idx
                    })

                locations = ', '.join([f"Bar {i+1}" for i in indices])

                variations.append({
                    'original': original_text,
                    'locations': locations,
                    'ideas': ideas
                })
        else:
            print("[BRENDA] No repetition found - no 2-bar phrases or repeated measures")

        return {'variations': variations}

    except Exception as e:
        return {'error': str(e)}


@app.post("/brenda/apply-variations")
async def brenda_apply_variations(req: BrendaApplyRequest):
    """Step 3: Apply variations to the tune (with random selection)"""
    try:
        # Get repeated phrases from repetition info (prefer 2-bar, fallback to measures)
        repeated_phrases = req.repetition_info.get('repeated_phrases_2bar', [])

        # If no 2-bar phrases, construct phrase info from repeated_measures
        if not repeated_phrases and req.repetition_info.get('repeated_measures'):
            print("[BRENDA] No 2-bar phrases in apply, using repeated measures")
            measures = repetition_detector.extract_measures_with_durations(req.abc)
            repeated_phrases = []

            for measure_content, indices in list(req.repetition_info['repeated_measures'].items())[:3]:
                original_text = measures[indices[0]]
                repeated_phrases.append({
                    'original_text': original_text,
                    'occurrences': indices,
                    'length': 1
                })

        # Apply variations
        result = brenda_variations.apply_variations_to_tune(
            req.abc,
            repeated_phrases,
            req.variations
        )

        return result

    except Exception as e:
        return {'error': str(e)}


@app.post("/analyze-skeletal")
async def analyze_skeletal(req: SkeletalAnalysisRequest):
    """
    Analyze skeletal (structural) vs. ornamental notes
    Combines AI analysis of Session variations with algorithmic feature extraction
    """
    try:
        print(f"[SKELETAL] Starting analysis")
        print(f"[SKELETAL] Session URL: {req.session_url or 'None (algorithmic only)'}")

        # Feature B: Algorithmic Analysis with music21 - compute all 3 complexity levels
        print("[SKELETAL] Extracting music21 features for all complexity levels...")
        algo_features_levels = {}
        algo_csvs = {}

        for level in [1, 2, 3]:
            features = skeletal_analysis.extract_music21_features(req.abc, complexity_level=level)
            features = skeletal_analysis.normalize_importance_scores(features)
            algo_features_levels[level] = features
            algo_csvs[level] = skeletal_analysis.features_to_csv(features)

        # Use the requested level as the primary one (default to level 1)
        algo_features = algo_features_levels.get(req.complexity_level, algo_features_levels[1])
        algo_csv = algo_csvs.get(req.complexity_level, algo_csvs[1])

        # Generate algorithmic skeleton (50% threshold)
        algo_skeletal_abc = skeletal_analysis.generate_skeletal_abc(req.abc, algo_features, threshold=0.5)

        # Feature D: MIR Analysis - compute all 3 complexity levels
        print("[SKELETAL] Extracting MIR features for all complexity levels...")
        mir_features_levels = {}
        mir_csvs = {}

        # Map complexity levels to weight configurations
        level_weights = {
            1: {  # Simple: basic features only
                'duration': 1.0, 'metric': 1.0, 'harmonic': 1.0,
                'contour': 0.0, 'scalar': 0.0, 'intervallic': 0.0,
                'phrase': 0.0, 'agogic': 0.0
            },
            2: {  # Medium: add melodic features
                'duration': 1.0, 'metric': 1.0, 'harmonic': 1.0,
                'contour': 1.0, 'scalar': 1.0, 'intervallic': 1.0,
                'phrase': 0.0, 'agogic': 0.0
            },
            3: {  # Complex: all features
                'duration': 1.0, 'metric': 1.0, 'harmonic': 1.0,
                'contour': 1.0, 'scalar': 1.0, 'intervallic': 1.0,
                'phrase': 1.0, 'agogic': 1.0
            }
        }

        for level in [1, 2, 3]:
            weights = req.mir_weights if req.mir_weights else level_weights[level]
            features = skeletal_analysis.extract_mir_features(req.abc, weights=weights)
            mir_features_levels[level] = features
            mir_csvs[level] = skeletal_analysis.mir_features_to_csv(features)

        # Use level 1 as default
        mir_features = mir_features_levels[1]
        mir_csv = mir_csvs[1]

        # Feature A: AI Analysis (if session_url provided)
        ai_skeletal_abc = None
        ai_reasoning = None
        ai_note_scores = None
        num_settings = 0

        if req.session_url and ANTHROPIC_AVAILABLE:
            print("[SKELETAL] Fetching Session variations for AI analysis...")
            try:
                # Fetch variations from The Session (reuse session.html logic)
                tune_data = session_scraper.fetch_tune_from_session(req.session_url)
                settings = tune_data.get('settings', [])
                num_settings = len(settings)

                if num_settings > 0:
                    print(f"[SKELETAL] Found {num_settings} settings, analyzing with AI...")

                    # Transpose all to match user's key
                    user_key_match = re.search(r'K:\s*([A-G][#b]?\s*\w*)', req.abc)
                    user_key = ''.join(c for c in user_key_match.group(1).strip() if c.isprintable()).strip() if user_key_match else None

                    transposed_settings = []
                    for idx, setting_abc in enumerate(settings[:12], 1):  # Limit to 12 for AI analysis
                        try:
                            if user_key:
                                # Extract the key from this setting
                                setting_key_match = re.search(r'K:\s*([A-G][#b]?\s*\w*)', setting_abc)
                                if setting_key_match:
                                    setting_key = ''.join(c for c in setting_key_match.group(1).strip() if c.isprintable()).strip()
                                    transposed_abc = abc_transpose.transpose_abc_tune_music21(setting_abc, setting_key, user_key)
                                else:
                                    transposed_abc = setting_abc
                            else:
                                transposed_abc = setting_abc

                            transposed_settings.append({
                                'setting_number': idx,
                                'abc': transposed_abc
                            })
                        except Exception as e:
                            print(f"[SKELETAL] Transpose failed for setting {idx}: {e}")
                            transposed_settings.append({
                                'setting_number': idx,
                                'abc': setting_abc
                            })

                    # AI prompt to analyze conserved vs. variable notes
                    variations_text = '\n\n'.join([
                        f"Setting {s['setting_number']}:\n{s['abc']}"
                        for s in transposed_settings
                    ])

                    ai_prompt = f"""Analyze these {len(transposed_settings)} variations of the same Irish traditional tune.

Original (user's version):
{req.abc}

Variations from The Session ({len(transposed_settings)} total):
{variations_text}

For each note in the original ABC, count how many of the {len(transposed_settings)} variations have the same note (same pitch + duration) at approximately the same position.

Calculate the conservation percentage: (number of variations with this note / {len(transposed_settings)}) × 100

Return JSON with:
{{
  "skeletal_abc": "ABC notation with only the most conserved notes (appearing in 50%+ of variations)",
  "reasoning": "2-3 sentences explaining what patterns you found (which notes are conserved vs. variable)",
  "note_scores": [
    {{"onset": 0.0, "pitch": 64, "score": 0.9167, "count": 11, "reason": "appears in 11/{len(transposed_settings)} variations"}},
    {{"onset": 0.5, "pitch": 66, "score": 0.1667, "count": 2, "reason": "appears in 2/{len(transposed_settings)} variations - ornamental"}}
  ]
}}

IMPORTANT:
- The "score" field MUST be the exact percentage: count / {len(transposed_settings)}
- The "count" field is how many variations contain this note
- Return ONLY valid JSON, nothing else."""

                    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
                    message = client.messages.create(
                        model="claude-sonnet-4-5-20250929",
                        max_tokens=3000,
                        messages=[{"role": "user", "content": ai_prompt}]
                    )

                    response_text = message.content[0].text.strip()

                    # Clean up markdown if present
                    if response_text.startswith('```json'):
                        response_text = response_text.replace('```json', '').replace('```', '').strip()
                    elif response_text.startswith('```'):
                        response_text = response_text.replace('```', '').strip()

                    # Parse JSON
                    import json
                    ai_result = json.loads(response_text)

                    ai_skeletal_abc = ai_result.get('skeletal_abc', '')
                    ai_reasoning = ai_result.get('reasoning', '')
                    ai_note_scores = ai_result.get('note_scores', [])

                    print(f"[SKELETAL] AI analysis complete")

            except Exception as e:
                print(f"[SKELETAL] AI analysis failed: {e}")
                # Continue with algorithmic only

        # Feature C: Combine AI + Algorithmic + MIR scores
        print("[SKELETAL] Combining scores (AI + Algorithmic + MIR)...")
        combined_scores = []

        for note in algo_features:
            # Find matching AI score by onset
            ai_score = None
            if ai_note_scores:
                # Find closest matching note by onset (within 0.1)
                matches = [s for s in ai_note_scores
                          if abs(s.get('onset', 999) - note['onset']) < 0.1]
                if matches:
                    ai_score = matches[0].get('score', None)

            # Find matching MIR score by onset
            mir_score = None
            for mir_note in mir_features:
                if abs(mir_note['onset'] - note['onset']) < 0.01:
                    mir_score = mir_note['mir_score']
                    break

            # Weighted combination: 40% AI, 30% algorithmic, 30% MIR
            # If AI not available: 50% algorithmic, 50% MIR
            if ai_score is not None:
                combined_score = (0.4 * ai_score) + (0.3 * note['algo_score']) + (0.3 * mir_score)
            else:
                # No AI score - use algorithmic + MIR
                combined_score = (0.5 * note['algo_score']) + (0.5 * mir_score)
                ai_score = note['algo_score']  # Display algo score in AI column for clarity

            combined_scores.append({
                'onset': note['onset'],
                'pitch': note['pitch'],
                'note_name': note['note_name'],
                'duration': note['duration'],
                'ai_score': ai_score,
                'algo_score': note['algo_score'],
                'mir_score': mir_score,
                'combined_score': combined_score
            })

        # Generate combined CSV
        combined_csv = skeletal_analysis.combined_scores_to_csv(combined_scores)

        print("[SKELETAL] Analysis complete!")

        return {
            'original_abc': req.abc,
            'ai_skeletal_abc': ai_skeletal_abc,
            'ai_reasoning': ai_reasoning,
            'ai_note_scores': ai_note_scores,  # Include for AI slider
            'num_settings': num_settings,
            'algo_skeletal_abc': algo_skeletal_abc,
            'algo_features': algo_features,  # Include for frontend slider (current level)
            'algo_features_levels': algo_features_levels,  # All 3 complexity levels
            'algo_csvs': algo_csvs,  # CSVs for all 3 levels
            'algo_csv': algo_csv,
            'mir_features': mir_features,  # Include for MIR slider (level 1)
            'mir_features_levels': mir_features_levels,  # All 3 MIR complexity levels
            'mir_csvs': mir_csvs,  # MIR CSVs for all 3 levels
            'mir_csv': mir_csv,
            'combined_csv': combined_csv,
            'combined_scores': combined_scores
        }

    except Exception as e:
        print(f"[SKELETAL ERROR] {e}")
        import traceback
        traceback.print_exc()
        return {'error': str(e)}


@app.post("/analyze-simple")
async def analyze_simple(req: SimpleAnalysisRequest):
    """
    Simple skeletal analysis using 5 practical methods
    """
    try:
        print("[SIMPLE] Starting simple analysis...")

        # Extract features once for reuse
        algo_features = skeletal_analysis.extract_music21_features(req.abc, complexity_level=3)
        algo_features = skeletal_analysis.normalize_importance_scores(algo_features)

        # Method 1: Metric × Duration Rule
        method1_notes = []
        for note in algo_features:
            score = note['duration'] * note['beatStrength']
            if score >= 0.5:  # Threshold for strong+long notes
                method1_notes.append(note)

        method1_abc = skeletal_analysis.generate_skeletal_abc(req.abc, method1_notes, threshold=0)
        method1_explanation = f"Selected {len(method1_notes)} notes with metric×duration ≥ 0.5"

        # Method 2: One Note Per Measure
        # Group notes by measure and pick the one with highest metric×duration
        measure_notes = {}
        for note in algo_features:
            measure = int(note['onset'] // 3)  # Assuming 6/8 time, 3 beats per measure
            score = note['duration'] * note['beatStrength']
            if measure not in measure_notes or score > measure_notes[measure][1]:
                measure_notes[measure] = (note, score)

        method2_notes = [note for note, score in measure_notes.values()]
        method2_abc = skeletal_analysis.generate_skeletal_abc(req.abc, method2_notes, threshold=0)
        method2_explanation = f"Selected 1 note per measure ({len(method2_notes)} total)"

        # Method 3: Melodic Contour (peaks, valleys, direction changes)
        method3_notes = []
        for note in algo_features:
            if note.get('isContourPeak') or note.get('isContourValley'):
                method3_notes.append(note)

        method3_abc = skeletal_analysis.generate_skeletal_abc(req.abc, method3_notes, threshold=0)
        method3_explanation = f"Selected {len(method3_notes)} contour points (peaks & valleys)"

        # Method 4: Chord Tones on Strong Beats
        method4_notes = []
        for note in algo_features:
            if note.get('isChordTone') and note['beatStrength'] >= 0.5:
                method4_notes.append(note)

        method4_abc = skeletal_analysis.generate_skeletal_abc(req.abc, method4_notes, threshold=0)
        method4_explanation = f"Selected {len(method4_notes)} chord tones on strong beats"

        # Method 5: Variation Analysis (if Session URL provided)
        method5_notes = []
        method5_explanation = "No Session URL provided"
        num_variations = 0

        if req.session_url and ANTHROPIC_AVAILABLE:
            try:
                tune_data = session_scraper.fetch_tune_from_session(req.session_url)
                settings = tune_data.get('settings', [])
                num_variations = len(settings)

                if num_variations > 0:
                    # Use the AI analysis we already have
                    user_key_match = re.search(r'K:\s*([A-G][#b]?\s*\w*)', req.abc)
                    user_key = ''.join(c for c in user_key_match.group(1).strip() if c.isprintable()).strip() if user_key_match else None

                    transposed_settings = []
                    for idx, setting_abc in enumerate(settings[:12], 1):
                        try:
                            if user_key:
                                setting_key_match = re.search(r'K:\s*([A-G][#b]?\s*\w*)', setting_abc)
                                if setting_key_match:
                                    setting_key = ''.join(c for c in setting_key_match.group(1).strip() if c.isprintable()).strip()
                                    transposed_abc = abc_transpose.transpose_abc_tune_music21(setting_abc, setting_key, user_key)
                                else:
                                    transposed_abc = setting_abc
                            else:
                                transposed_abc = setting_abc

                            transposed_settings.append({'setting_number': idx, 'abc': transposed_abc})
                        except:
                            transposed_settings.append({'setting_number': idx, 'abc': setting_abc})

                    # AI analysis for conserved notes
                    variations_text = '\n\n'.join([f"Setting {s['setting_number']}:\n{s['abc']}" for s in transposed_settings])

                    ai_prompt = f"""Analyze these {len(transposed_settings)} variations. Return notes that appear in 50%+ of variations.

Original: {req.abc}

Variations: {variations_text}

Return JSON: {{"note_scores": [{{"onset": 0.0, "pitch": 64, "score": 0.75}}]}}"""

                    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
                    message = client.messages.create(
                        model="claude-sonnet-4-5-20250929",
                        max_tokens=2000,
                        messages=[{"role": "user", "content": ai_prompt}]
                    )

                    response_text = message.content[0].text.strip()
                    if response_text.startswith('```json'):
                        response_text = response_text.replace('```json', '').replace('```', '').strip()

                    ai_result = json.loads(response_text)
                    ai_note_scores = ai_result.get('note_scores', [])

                    # Match AI scores to our notes
                    for note in algo_features:
                        for ai_note in ai_note_scores:
                            if abs(ai_note.get('onset', 999) - note['onset']) < 0.1:
                                if ai_note.get('score', 0) >= 0.5:
                                    method5_notes.append(note)
                                break

                    method5_explanation = f"Selected {len(method5_notes)} notes conserved across {num_variations} variations"
            except Exception as e:
                print(f"[SIMPLE] Method 5 failed: {e}")
                method5_explanation = f"Variation analysis failed: {str(e)}"

        method5_abc = skeletal_analysis.generate_skeletal_abc(req.abc, method5_notes, threshold=0) if method5_notes else req.abc

        # Final Combined: Use consensus (notes appearing in 3+ methods)
        note_votes = {}
        for note in algo_features:
            onset = note['onset']
            note_votes[onset] = 0

            if note in method1_notes:
                note_votes[onset] += 1
            if note in method2_notes:
                note_votes[onset] += 1
            if note in method3_notes:
                note_votes[onset] += 1
            if note in method4_notes:
                note_votes[onset] += 1
            if note in method5_notes:
                note_votes[onset] += 1

        # Require 2+ votes (appearing in at least 2 methods)
        final_notes = [note for note in algo_features if note_votes.get(note['onset'], 0) >= 2]
        final_abc = skeletal_analysis.generate_skeletal_abc(req.abc, final_notes, threshold=0)

        # Generate narrative with AI
        narrative = "Analysis complete."
        if ANTHROPIC_AVAILABLE:
            try:
                narrative_prompt = f"""Analyze these 5 skeletal reduction methods for an Irish tune:

Method 1 (Metric×Duration): {len(method1_notes)} notes
Method 2 (One per measure): {len(method2_notes)} notes
Method 3 (Contour): {len(method3_notes)} notes
Method 4 (Chord tones): {len(method4_notes)} notes
Method 5 (Variations): {len(method5_notes)} notes ({method5_explanation})

Final skeleton: {len(final_notes)} notes (requires 2+ method agreement)

Write a 3-4 sentence narrative assessment comparing these methods and explaining which seem most reliable for this tune."""

                client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
                message = client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=500,
                    messages=[{"role": "user", "content": narrative_prompt}]
                )

                narrative = message.content[0].text.strip()
            except:
                pass

        return {
            'original_abc': req.abc,
            'method1': {'abc': method1_abc, 'explanation': method1_explanation},
            'method2': {'abc': method2_abc, 'explanation': method2_explanation},
            'method3': {'abc': method3_abc, 'explanation': method3_explanation},
            'method4': {'abc': method4_abc, 'explanation': method4_explanation},
            'method5': {'abc': method5_abc, 'explanation': method5_explanation},
            'final_abc': final_abc,
            'narrative': narrative
        }

    except Exception as e:
        print(f"[SIMPLE ERROR] {e}")
        import traceback
        traceback.print_exc()
        return {'error': str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8017)
