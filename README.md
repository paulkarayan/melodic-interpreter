# Irish Tune Variation Generator

A tool for exploring melodic recomposition and harmony for traditional Irish tunes, with special consideration for Anglo concertina playability.

## 🎵 Features

- **5 Harmony Types**: Quartal sparse, Quartal two-note, Modal drone, Diatonic thirds, Open fifths
- **5 Melodic Variations**: Chromatic passing tones, Neighbor tones, Octave displacement, Rhythmic shift, Simplification
- **Multi-spot Application**: Melodic variations apply to 2-5 random locations
- **Lick Targeting**: Specify exact phrase to modify (e.g., "eAABcd")
- **Feeling Lucky**: Generate 5 random variation combinations
- **Session Analysis**: (Coming soon) Analyze variations from thesession.org
- **Anglo Validation**: (Coming soon) Filter impossible note combinations for C/G 30-button Anglo

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

```bash
# Clone or navigate to project
cd melodic-interpreter

# Install dependencies with uv
uv venv
uv pip install -r requirements.txt

# Or with pip
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the Server

**Option 1: Using the start script**
```bash
./START_SERVER.sh
```

**Option 2: Manual start**
```bash
source .venv/bin/activate
uvicorn app:app --reload --port 8000
```

**Option 3: Using uv directly**
```bash
uv run uvicorn app:app --reload --port 8000
```

Then open: **http://localhost:8000**

## 📖 Usage

1. **Paste ABC notation** of an Irish tune (default: Sliabh Russell)
2. **Select harmony type** from dropdown (or "No harmony")
3. **Select melodic variation** from dropdown (or "Keep original melody")
4. **Optional**: Target a specific lick (e.g., "eAABcd")
5. Click **"Generate Variations"**

Or click **"🍀 Feeling Lucky"** for 5 random combinations!

## 🏗️ Project Structure

```
melodic-interpreter/
├── app.py                      # FastAPI backend
├── core/                       # Python modules
│   ├── abc_utils.py           # ABC parsing/manipulation
│   ├── harmony.py             # Harmony generation
│   ├── melodic.py             # Melodic variations
│   ├── validator.py           # Anglo validation (WIP)
│   └── session_scraper.py     # Session scraping (WIP)
├── docs/                       # Resources
│   ├── ANGLO_CONSTRAINTS.md   # Impossible note pairs
│   ├── VARIATION_PHILOSOPHY.md # Trad → Avant-garde spectrum
│   └── transformation_prompts.py # LLM style prompts
├── variations_enhanced.html    # Frontend UI
└── requirements.txt           # Dependencies
```

## 🎼 Example Tune

**Sliabh Russell (jig in A Dorian)**
```abc
X: 1
T: Sliabh Russell
R: jig
M: 6/8
L: 1/8
K: Ador
|:eAA Bcd|eaf ged|edB cBA|BAG ABd|
eAA Bcd|eaf ged|edB cBA|1 BAG A3:|2 BAG ABd||
|:eaa efg|agf gfd|eaa efg|afd e3|
eaa efg|agf gfd|edB cBA|BAG ABd:|
```

## 🔧 API Endpoints

### POST `/generate`
Generate harmony and melodic variations

**Request:**
```json
{
  "abc": "X:1\nT:Test...",
  "harmony_type": "quartal_sparse",
  "melodic_type": "chromatic",
  "lick": "eAABcd",  // optional
  "validate_anglo": false
}
```

**Response:**
```json
{
  "original": "...",
  "harmony": "...",
  "harmony_desc": "...",
  "melodic": "...",
  "melodic_desc": "...",
  "combined": "...",
  "combined_desc": "..."
}
```

### POST `/feeling-lucky`
Generate 5 random variations

**Request:**
```json
{
  "abc": "X:1\nT:Test...",
  "validate_anglo": false
}
```

**Response:**
```json
{
  "variations": [
    {"abc": "...", "description": "..."},
    ...
  ]
}
```

## 🎯 Roadmap

- [x] Basic harmony generation
- [x] Melodic variations with multi-spot application
- [x] Lick targeting
- [x] Feeling Lucky feature
- [ ] **The Session integration** (scrape & analyze variations)
- [ ] **Anglo validation** (filter impossible note combinations)
- [ ] **LLM transformations** (style-based variations)
- [ ] Export to MIDI/PDF

## 📚 Resources

- **ANGLO_CONSTRAINTS.md**: Impossible note combinations for C/G Anglo
- **VARIATION_PHILOSOPHY.md**: Traditional vs. contemporary approaches
- **CLAUDE_CODE_GUIDE.md**: Development guide
- **FUNCTIONS_NEEDED.md**: Feature roadmap

## 🐛 Troubleshooting

**Port already in use:**
```bash
lsof -ti:8000 | xargs kill -9
```

**Module not found:**
```bash
uv pip install -r requirements.txt
```

**Server not responding:**
Check logs in terminal for errors

## 🤝 Contributing

This is a personal project for exploring Irish music recomposition. Feel free to fork and adapt!

## 📝 License

MIT

## 🎶 Acknowledgments

Inspired by:
- Martin Hayes & Dennis Cahill (quartal harmony)
- Caoimhín Ó Raghallaigh (drone minimalism)
- The Gloaming (ambient chamber arrangements)
- thesession.org (Irish tune archive)
