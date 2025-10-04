"""
ABC notation manipulation utilities
Lightweight ABC modification without full parsing
"""
import re
from typing import Tuple, List


def parse_abc(abc_string: str) -> Tuple[str, str]:
    """
    Parse ABC into headers and body

    Args:
        abc_string: Full ABC notation string

    Returns:
        (headers_string, body_string)
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
    """
    Extract N bars from ABC body

    Args:
        body: ABC body (after K: header)
        count: Number of bars to extract

    Returns:
        List of bar strings
    """
    bars = [b.strip() for b in body.split('|')
            if b.strip() and not re.match(r'^[\s:12]*$', b)]
    return bars[:count]


def find_lick_occurrences(body: str, lick: str) -> List[dict]:
    """
    Find all occurrences of a lick pattern in the tune

    Args:
        body: ABC body
        lick: Lick pattern to find (e.g., "eAABcd")

    Returns:
        List of dicts with {'bar_index': int, 'bar': str}
    """
    clean_lick = lick.replace(' ', '').replace('\n', '')
    bars = body.split('|')
    occurrences = []

    for idx, bar in enumerate(bars):
        clean_bar = bar.replace(' ', '').replace('\n', '')
        if clean_lick in clean_bar:
            occurrences.append({'bar_index': idx, 'bar': bar.strip()})

    return occurrences


def validate_abc_syntax(abc_string: str) -> bool:
    """
    Basic ABC syntax validation

    Args:
        abc_string: ABC notation to validate

    Returns:
        True if valid, False otherwise
    """
    required_headers = ['X:', 'T:', 'M:', 'L:', 'K:']

    for header in required_headers:
        if header not in abc_string:
            return False

    return True
