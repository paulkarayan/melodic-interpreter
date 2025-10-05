"""
The Session scraper - fetch and analyze tune variations
"""
import re
from typing import List, Dict, Optional
try:
    import requests
    from bs4 import BeautifulSoup
    SCRAPING_AVAILABLE = True
except ImportError:
    SCRAPING_AVAILABLE = False


def fetch_tune_from_session(url: str) -> Dict:
    """
    Scrape tune data from The Session

    Args:
        url: The Session tune URL (e.g., https://thesession.org/tunes/1234)

    Returns:
        Dict with tune metadata and all ABC settings
    """
    if not SCRAPING_AVAILABLE:
        raise ImportError("requests and beautifulsoup4 required for session scraping")

    try:
        # Fetch the page
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract tune metadata
        title_elem = soup.find('h1')
        title = title_elem.text.strip() if title_elem else "Unknown"

        # Extract tune type and key from the first ABC notation
        # The Session includes R: (rhythm/type) and K: (key) in ABC headers
        tune_type = "Unknown"
        key = "Unknown"

        # Try to extract from ABC notation in the HTML
        type_match = re.search(r'R:\s*([^\<\n]+)', response.text)
        if type_match:
            tune_type = type_match.group(1).strip()

        key_match = re.search(r'K:\s*([^\<\n]+)', response.text)
        if key_match:
            key = key_match.group(1).strip()

        # Extract all ABC settings
        settings = extract_all_abc_settings(response.text)

        return {
            'title': title,
            'type': tune_type,
            'key': key,
            'settings': settings,
            'num_settings': len(settings)
        }

    except requests.RequestException as e:
        raise Exception(f"Failed to fetch from The Session: {str(e)}")


def extract_all_abc_settings(html: str) -> List[str]:
    """
    Extract all ABC notation settings from Session HTML

    Args:
        html: Raw HTML from Session page

    Returns:
        List of ABC notation strings
    """
    if not SCRAPING_AVAILABLE:
        raise ImportError("beautifulsoup4 required")

    soup = BeautifulSoup(html, 'html.parser')
    abc_notations = []

    # The Session stores ABC in <div class="notes"> inside <div role="tabpanel" class="setting-abc">
    abc_divs = soup.find_all('div', class_='notes')

    for div in abc_divs:
        # Get the HTML content
        abc_html = str(div)

        # Convert <br> tags to newlines
        abc_html = abc_html.replace('<br>', '\n').replace('<br/>', '\n').replace('<br />', '\n')

        # Remove all HTML tags
        abc_text = re.sub(r'<[^>]+>', '', abc_html)

        # Clean up: remove "Title", "Type", etc. labels
        abc_text = re.sub(r'\b(Number|Title|Type|Meter|Length|Key)\b:\s*', '', abc_text)

        # Clean up whitespace
        abc_text = abc_text.strip()

        # Validate it looks like ABC notation
        if abc_text and 'X:' in abc_text and 'K:' in abc_text:
            abc_notations.append(abc_text)

    return abc_notations


def compare_variations(abc_list: List[str]) -> Dict:
    """
    Compare multiple ABC variations to find differences
    Transposes all settings to the same key before comparison

    Args:
        abc_list: List of ABC notation strings

    Returns:
        Dict with comparison analysis
    """
    from .abc_utils import parse_abc

    if len(abc_list) < 2:
        return {
            'num_variations': len(abc_list),
            'differences': [],
            'unique_approaches': [],
            'message': 'Need at least 2 variations to compare'
        }

    # Parse all variations and extract keys
    parsed_variations = []
    keys = []
    for abc in abc_list:
        try:
            headers, body = parse_abc(abc)
            # Extract key from headers
            key_match = re.search(r'K:\s*([^\n]+)', headers)
            key = key_match.group(1).strip() if key_match else 'D'
            keys.append(key)
            bars = [b.strip() for b in body.split('|') if b.strip()]
            parsed_variations.append({'headers': headers, 'bars': bars, 'key': key})
        except:
            continue

    if len(parsed_variations) < 2:
        return {
            'num_variations': len(abc_list),
            'differences': [],
            'unique_approaches': [],
            'message': 'Unable to parse variations'
        }

    # Transpose all to first variation's key
    target_key = parsed_variations[0]['key']
    transposed_variations = []
    for var in parsed_variations:
        if var['key'] != target_key:
            # Note: Actual transposition would require a full ABC transposition library
            # For now, we note the key difference
            transposed_variations.append({
                'bars': var['bars'],
                'original_key': var['key'],
                'transposed_to': target_key
            })
        else:
            transposed_variations.append({
                'bars': var['bars'],
                'original_key': var['key'],
                'transposed_to': target_key
            })

    parsed_variations = transposed_variations

    # Compare bar by bar
    num_bars = min(len(v['bars']) for v in parsed_variations)
    differences = []

    for bar_idx in range(num_bars):
        bars_at_idx = [v['bars'][bar_idx] for v in parsed_variations if bar_idx < len(v['bars'])]
        unique_bars = set(bars_at_idx)

        if len(unique_bars) > 1:
            differences.append({
                'bar_number': bar_idx + 1,
                'num_variations': len(unique_bars),
                'variations': list(unique_bars)
            })

    # Find unique approaches
    unique_approaches = find_unique_approaches(abc_list)

    # Extract concrete musical examples from differences
    example_changes = []
    for diff in differences[:5]:  # Show first 5 examples
        if diff['num_variations'] >= 2:
            vars_list = diff['variations'][:3]  # Show up to 3 variations
            example_changes.append({
                'bar_number': diff['bar_number'],
                'examples': vars_list,
                'description': f"Bar {diff['bar_number']} has {diff['num_variations']} different versions"
            })

    return {
        'num_variations': len(abc_list),
        'num_bars_analyzed': num_bars,
        'differences': differences,
        'unique_approaches': unique_approaches,
        'example_changes': example_changes,
        'stability_score': 1 - (len(differences) / num_bars) if num_bars > 0 else 0
    }


def find_unique_approaches(abc_list: List[str]) -> List[Dict]:
    """
    Identify unique variation techniques across settings

    Args:
        abc_list: List of ABC notation strings

    Returns:
        List of dicts describing unique approaches
    """
    unique_patterns = []

    # Look for chromatic notes (sharps/flats beyond key signature)
    chromatic_users = []
    for idx, abc in enumerate(abc_list):
        if '^' in abc or '_' in abc or '=' in abc:
            chromatic_users.append(idx + 1)

    if chromatic_users:
        unique_patterns.append({
            'technique': 'Chromatic notes',
            'settings': chromatic_users,
            'description': 'Uses sharps/flats beyond key signature'
        })

    # Look for triplets
    triplet_users = []
    for idx, abc in enumerate(abc_list):
        if '(3' in abc:
            triplet_users.append(idx + 1)

    if triplet_users:
        unique_patterns.append({
            'technique': 'Triplets',
            'settings': triplet_users,
            'description': 'Uses triplet ornaments'
        })

    # Look for octave shifts
    octave_users = []
    for idx, abc in enumerate(abc_list):
        if "'" in abc or "," in abc:
            octave_users.append(idx + 1)

    if octave_users:
        unique_patterns.append({
            'technique': 'Octave displacement',
            'settings': octave_users,
            'description': 'Moves phrases to different octaves'
        })

    return unique_patterns
