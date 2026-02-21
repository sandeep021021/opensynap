"""
ANSI utilities 
"""

from __future__ import annotations

import re
from typing import Final

# Matches ANSI SGR sequences like: ECS [1m, ECS [ 0m, etc.
_ANSI_SGR_PATTERN: Final[str] = r"\x1b\[[0-9;]*m"

# Matches OSC-8 hyperlinks:
# ECS ] 8 ; ; url ST ... ESC ] 8 ; ; ST
# ST can be ESC \ (String terminator) in many terminals.
_OSC8_PATTERN: Final[str] = r"\x1b\]8;;.*?\x1b\\|\x1b\]8;;\x1b\\"

_ANSI_REGEX: Final[re.Pattern[str]] = re.compile(_ANSI_SGR_PATTERN)
_OSC8_REGEX: Final[re.Pattern[str]] = re.compile(_OSC8_PATTERN)


def strip_ansi(text: str) -> str:
    "Remove OSC-8 hyperlinks and ANSI SGR styling codes from text."
    return _ANSI_REGEX.sub("", _OSC8_REGEX.sub("", text))

def visible_width(text: str) -> int:
    """Return the visible charactor width of text (after stripping ANSI/OCS-8)"""
    return len(strip_ansi(text))