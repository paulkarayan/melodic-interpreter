# Claude Code Build Guide - Irish Tune Variations

## Quick Start

You're building an **Irish tune variation generator** with FastAPI backend.

### Tech Stack
- **Backend**: FastAPI (not Flask!)
- **Frontend**: HTML/JS with ABCJS for notation rendering
- **Processing**: Python for ABC manipulation, harmony, and melodic variations
- **Validation**: Anglo concertina playability checking

---

## File Structure

```
melodic-interpreter/
├── app.py                      # FastAPI backend
├── templates/
│   └── index.html              # Already exists: variations_enhanced.html
├── core/
│   ├── __init__.py
│   ├── abc_utils.py            # ABC parsing & manipulation
│   ├── harmony.py              # Harmony generation
│   ├── melodic.py              # Melodic variations
│   ├── validator.py            # Anglo concertina validation
│   └── session_scraper.py      # The Session scraping
├── docs/
│   ├── ANGLO_CONSTRAINTS.md    # Anglo impossible pairs
│   └── VARIATION_PHILOSOPHY.md # Traditional vs avant-garde
├── FUNCTIONS_NEEDED.md         # What to build (prioritized)
└── requirements.txt
```

---

## Phase 1: Core Backend (START HERE)

### 1. Create `requirements.txt`

```txt
fastapi
uvicorn[standard]
beautifulsoup4
requests
python-multipart
jinja2
```

Install with: `pip install -r requirements.txt`

---

### 2. Create `core/abc_utils.py`

Port these functions from `variations_enhanced.html`:

```python
"""
ABC notation manipulation utilities
"""
import re
from typing import Tuple, List

def parse_abc(abc_string: str) -> Tuple[str, str]:
    """
    Parse ABC into headers and body
    Returns: (headers_string, body_string)
    """
    lines = abc_string.split('\n')
    header_end = next((i for i, l in enumerate(lines) if l.startswith('K:')), -1)

    if header_end == -1:
        raise ValueError("Invalid ABC notation - no K: header found")

    headers = '\n'.join(lines[:header_end + 1])
    body = '\n'.join(lines[header_end + 1:])

    return headers, body


def rebuild_abc(headers: str, body: str) -> str:
    """Rebuild ABC from headers and body"""
    return f"{headers}\n{body}"


def get_bars(body: str, count: int = 1) -> List[str]:
    """Extract N bars from ABC body"""
    bars = [b.strip() for b in body.split('|')
            if b.strip() and not re.match(r'^[\s:12]*$', b)]
    return bars[:count]


def find_lick_occurrences(body: str, lick: str) -> List[dict]:
    """
    Find all occurrences of a lick pattern
    Returns: [{'bar_index': int, 'bar': str}, ...]
    """
    clean_lick = lick.replace(' ', '')
    bars = body.split('|')
    occurrences = []

    for idx, bar in enumerate(bars):
        clean_bar = bar.replace(' ', '')
        if clean_lick in clean_bar:
            occurrences.append({'bar_index': idx, 'bar': bar.strip()})

    return occurrences
```

---

### 3. Create `core/harmony.py`

Port from HTML, but as Python functions:

```python
"""
Harmony generation for Irish tunes
"""
import re
from .abc_utils import parse_abc, rebuild_abc, get_bars


def apply_quartal_sparse(abc: str) -> str:
    """Add quartal harmony on beats 1 and 5"""
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    # Add fourths on e and B
    varied = re.sub(r'^e', '[EA]', bars[0])
    varied = re.sub(r'B', '[BE]', varied)

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_quartal_two(abc: str) -> str:
    """Two-note quartal fourths throughout"""
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    varied = re.sub(r'e', '[EA]', bars[0])
    varied = re.sub(r'A', '[AD]', varied)

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_modal_drone(abc: str) -> str:
    """Static A-D drone underneath"""
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    varied = '[AD]3 ' + bars[0]

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_diatonic_thirds(abc: str) -> str:
    """Diatonic thirds harmony"""
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    varied = re.sub(r'e([^a])', r'[ec]\1', bars[0])
    varied = re.sub(r'A', '[Ac]', varied)
    varied = re.sub(r'B', '[Bd]', varied)

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


def apply_open_fifths(abc: str) -> str:
    """Open fifths harmony"""
    headers, body = parse_abc(abc)
    bars = get_bars(body, 2)

    varied = re.sub(r'A', '[AE]', bars[0])
    varied = re.sub(r'd', '[da]', varied)

    result_body = '|' + varied + '|' + (bars[1] if len(bars) > 1 else '') + '|'
    return rebuild_abc(headers, result_body)


# Harmony registry
HARMONY_FUNCTIONS = {
    'quartal_sparse': apply_quartal_sparse,
    'quartal_two': apply_quartal_two,
    'modal_drone': apply_modal_drone,
    'diatonic_thirds': apply_diatonic_thirds,
    'open_fifths': apply_open_fifths,
}

HARMONY_DESCRIPTIONS = {
    'quartal_sparse': "Quartal harmony on beats 1 and 5 - fourth intervals for modern sound",
    'quartal_two': "Two-note quartal fourths throughout - most anglo-friendly approach",
    'modal_drone': "Static A-D drone underneath - emphasizes Dorian mode",
    'diatonic_thirds': "Diatonic thirds harmony - traditional approach",
    'open_fifths': "Open fifths - powerful, traditional sound",
}
```

---

### 4. Create `core/melodic.py`

```python
"""
Melodic variations for Irish tunes
Apply to 2-5 spots or specific lick
"""
import re
import random
from typing import Optional, Tuple
from .abc_utils import parse_abc, rebuild_abc, find_lick_occurrences


def apply_melodic_to_bar(bar: str, variation_type: str) -> str:
    """Apply melodic variation to a single bar"""

    if variation_type == 'chromatic':
        # Add chromatic passing tones
        bar = re.sub(r'eA', 'e^fA', bar)
        bar = re.sub(r'cd', 'c^cd', bar)

    elif variation_type == 'neighbor':
        # Neighbor tone substitution
        bar = re.sub(r'AA', 'AB', bar)
        bar = re.sub(r'ee', 'ed', bar)

    elif variation_type == 'octave_displacement':
        # Move to higher octave
        bar = re.sub(r"e([^a'])", r"e'\1", bar)
        bar = re.sub(r"A(?![a-z'])", "a", bar)

    elif variation_type == 'rhythmic_shift':
        # Add rest at start
        bar = 'z/2 ' + bar[:-2]

    elif variation_type == 'simplification':
        # Remove repeated notes
        bar = re.sub(r'AA', 'A2', bar)
        bar = re.sub(r'ee', 'e2', bar)

    return bar


def apply_melodic_multiple(
    abc: str,
    variation_type: str,
    target_lick: Optional[str] = None
) -> Tuple[str, str]:
    """
    Apply melodic variation to 2-5 spots (or specific lick)
    Returns: (modified_abc, description)
    """
    headers, body = parse_abc(abc)
    bars = [b.strip() for b in body.split('|') if b.strip()]

    modified_bars = bars.copy()
    applied_count = 0

    if target_lick:
        # Apply to specific lick only
        occurrences = find_lick_occurrences(body, target_lick)

        for occ in occurrences:
            idx = occ['bar_index']
            if idx < len(modified_bars):
                modified_bars[idx] = apply_melodic_to_bar(modified_bars[idx], variation_type)
                applied_count += 1

        description = f'Applied to lick "{target_lick}" ({applied_count} occurrences)'

    else:
        # Apply to 2-5 random spots
        num_spots = random.randint(2, min(5, len(bars)))
        indices = random.sample(range(len(bars)), num_spots)

        for idx in indices:
            modified_bars[idx] = apply_melodic_to_bar(modified_bars[idx], variation_type)

        applied_count = num_spots
        description = f'Applied to {applied_count} different locations'

    modified_body = '|' + '|'.join(modified_bars) + '|'
    return rebuild_abc(headers, modified_body), description


# Melodic registry
MELODIC_DESCRIPTIONS = {
    'chromatic': "Chromatic passing tones - bebop-influenced approach",
    'neighbor': "Neighbor tone substitution - traditional variation technique",
    'octave_displacement': "Octave displacement - move phrases up/down an octave",
    'rhythmic_shift': "Rhythmic displacement - shift note positions",
    'simplification': "Simplification - reduce to essential notes",
}
```

---

### 5. Create `app.py` (FastAPI)

```python
"""
FastAPI backend for Irish tune variation generator
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import random

from core import harmony, melodic

app = FastAPI(title="Irish Tune Variation Generator")

# Templates
templates = Jinja2Templates(directory=".")


class VariationRequest(BaseModel):
    abc: str
    harmony_type: str = 'none'
    melodic_type: str = 'none'
    lick: Optional[str] = None
    validate_anglo: bool = False


class FeelingLuckyRequest(BaseModel):
    abc: str
    validate_anglo: bool = False


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Serve the main HTML page"""
    with open('variations_enhanced.html') as f:
        return HTMLResponse(content=f.read())


@app.post("/generate")
async def generate_variations(req: VariationRequest):
    """Generate harmony and melodic variations"""

    results = {'original': req.abc}

    # Generate harmony variation
    if req.harmony_type != 'none' and req.harmony_type in harmony.HARMONY_FUNCTIONS:
        harmony_fn = harmony.HARMONY_FUNCTIONS[req.harmony_type]
        results['harmony'] = harmony_fn(req.abc)
        results['harmony_desc'] = harmony.HARMONY_DESCRIPTIONS[req.harmony_type]

    # Generate melodic variation
    if req.melodic_type != 'none':
        melodic_abc, melodic_desc = melodic.apply_melodic_multiple(
            req.abc, req.melodic_type, req.lick
        )
        results['melodic'] = melodic_abc
        results['melodic_desc'] = (
            f"{melodic.MELODIC_DESCRIPTIONS[req.melodic_type]} - {melodic_desc}"
        )

    # Combined variation
    if req.harmony_type != 'none' and req.melodic_type != 'none':
        # Apply harmony first
        combined = harmony.HARMONY_FUNCTIONS[req.harmony_type](req.abc)
        # Then melodic
        combined, melodic_desc = melodic.apply_melodic_multiple(
            combined, req.melodic_type, req.lick
        )
        results['combined'] = combined
        results['combined_desc'] = f"Both harmony and melodic variations applied - {melodic_desc}"

    # TODO: Validate anglo playability if requested

    return results


@app.post("/feeling-lucky")
async def feeling_lucky(req: FeelingLuckyRequest):
    """Generate 5 random variation combinations"""

    harmony_types = list(harmony.HARMONY_FUNCTIONS.keys())
    melodic_types = list(melodic.MELODIC_DESCRIPTIONS.keys())

    variations = []

    for i in range(5):
        h_type = random.choice(harmony_types)
        m_type = random.choice(melodic_types)

        # Apply harmony
        variation = harmony.HARMONY_FUNCTIONS[h_type](req.abc)
        # Apply melodic
        variation, m_desc = melodic.apply_melodic_multiple(variation, m_type, None)

        variations.append({
            'abc': variation,
            'description': (
                f"{harmony.HARMONY_DESCRIPTIONS[h_type]} + "
                f"{melodic.MELODIC_DESCRIPTIONS[m_type]} ({m_desc})"
            )
        })

    return {'variations': variations}


@app.get("/health")
async def health():
    return {"status": "ok"}
```

---

### 6. Update `variations_enhanced.html`

Change the JavaScript to call FastAPI instead of doing everything client-side:

```javascript
// Replace generateVariations() with:
async function generateVariations() {
    try {
        const abc = document.getElementById('abc-input').value;
        const harmonyType = document.getElementById('harmony-select').value;
        const melodicType = document.getElementById('melodic-select').value;
        const targetLick = document.getElementById('lick-input').value.trim();

        // Validate Session URL if needed
        if (currentTab === 'session') {
            const sessionUrl = document.getElementById('session-url').value;
            if (!sessionUrl) {
                alert('Please provide a Session URL when using Session Variations');
                return;
            }
        }

        // Call backend API
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                abc: abc,
                harmony_type: harmonyType,
                melodic_type: melodicType,
                lick: targetLick || null,
                validate_anglo: false
            })
        });

        const data = await response.json();

        // Hide lucky output
        document.getElementById('lucky-output').style.display = 'none';

        // Render original
        ABCJS.renderAbc('original-notation', data.original, { responsive: 'resize' });

        // Render harmony variation
        if (data.harmony) {
            document.getElementById('harmony-desc').textContent = data.harmony_desc;
            ABCJS.renderAbc('harmony-notation', data.harmony, { responsive: 'resize' });
            document.getElementById('harmony-output').style.display = 'block';
        } else {
            document.getElementById('harmony-output').style.display = 'none';
        }

        // Render melodic variation
        if (data.melodic) {
            document.getElementById('melodic-desc').textContent = data.melodic_desc;
            ABCJS.renderAbc('melodic-notation', data.melodic, { responsive: 'resize' });
            document.getElementById('melodic-output').style.display = 'block';
        } else {
            document.getElementById('melodic-output').style.display = 'none';
        }

        // Render combined variation
        if (data.combined) {
            document.getElementById('combined-desc').textContent = data.combined_desc;
            ABCJS.renderAbc('combined-notation', data.combined, { responsive: 'resize' });
            document.getElementById('combined-output').style.display = 'block';
        } else {
            document.getElementById('combined-output').style.display = 'none';
        }

        // Show output
        document.getElementById('output').style.display = 'block';

    } catch (error) {
        console.error('Error generating variations:', error);
        document.getElementById('output').innerHTML = `
            <div class="error">
                Error generating variations: ${error.message}
                <br>Check console for details.
            </div>
        `;
        document.getElementById('output').style.display = 'block';
    }
}

// Replace feelingLucky() with:
async function feelingLucky() {
    const abc = document.getElementById('abc-input').value;

    try {
        const response = await fetch('/feeling-lucky', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                abc: abc,
                validate_anglo: false
            })
        });

        const data = await response.json();

        // Hide other outputs
        document.getElementById('harmony-output').style.display = 'none';
        document.getElementById('melodic-output').style.display = 'none';
        document.getElementById('combined-output').style.display = 'none';
        document.getElementById('session-output').style.display = 'none';

        // Render original
        ABCJS.renderAbc('original-notation', abc, { responsive: 'resize' });

        // Render lucky variations
        let luckyHTML = '';
        data.variations.forEach((v, i) => {
            luckyHTML += `
                <div class="variation lucky-variation">
                    <div class="description">
                        <strong>Variation ${i + 1}:</strong> ${v.description}
                    </div>
                    <div id="lucky-${i}" class="notation"></div>
                </div>
            `;
        });

        document.getElementById('lucky-variations').innerHTML = luckyHTML;
        document.getElementById('lucky-output').style.display = 'block';

        // Render all
        data.variations.forEach((v, i) => {
            ABCJS.renderAbc('lucky-' + i, v.abc, { responsive: 'resize' });
        });

        document.getElementById('output').style.display = 'block';

    } catch (error) {
        console.error('Error generating lucky variations:', error);
        alert('Error generating variations');
    }
}
```

---

## Running the App

```bash
# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn app:app --reload --port 8000

# Open browser to:
http://localhost:8000
```

---

## Phase 2: Add Anglo Validation

See `FUNCTIONS_NEEDED.md` for `core/validator.py` implementation.

---

## Phase 3: Add Session Scraping

See `session_scraper.py` - already stubbed out for you.

---

## What You Have Now

✅ **Enhanced HTML** (`variations_enhanced.html`)
- Multiple melodic variation spots (2-5)
- Specific lick targeting
- Session URL validation
- Feeling Lucky button

✅ **Function Map** (`FUNCTIONS_NEEDED.md`)
- Prioritized list of what to build
- Clear phase breakdown

✅ **This Guide**
- FastAPI backend structure
- Core functions ready to copy
- API endpoints defined

---

## Next Steps

1. **Copy code from this guide into files**
2. **Test locally** with `uvicorn app:app --reload`
3. **Verify HTML works with backend**
4. **Add validation** (Phase 2)
5. **Add Session scraping** (Phase 3)

Start with Phase 1 - get the basic backend working first!
