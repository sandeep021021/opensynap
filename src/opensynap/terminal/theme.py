"""
Terminal theme utilities
"""

from __future__ import annotations

import os
import sys
from typing import Callable, Dict, Final

from .palette import LOBSTER_PALETTE

StyleFn = Callable[[str], str]

def _truthy_env(name: str) -> bool:
    """Returns True if env var exists and is not empty and not '0'. """
    value = os.getenv(name)
    if value is None:
        return False
    v = value.strip()
    return len(v) > 0 and v != "0"


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert #RRGGBB to (R, G, B)."""
    s = hex_color.strip()
    if s.startswith("#"):
        s = s[1:]
    if len(s) != 6:
        raise ValueError(f"Invalid hex_color: {hex_color!r}")
    r = int(s[0:2], 16)
    g = int(s[2:4], 16)
    b = int(s[4:6], 16)
    return r, g, b

def _supports_rich_output() -> bool:
    """
    Decide whether styling should be enabled.
    """
    if _truthy_env("FORCE_COLOR"):
        return True
    if os.getenv("NO_COLOR") is not None:
        return False
    return bool(sys.stdout.isatty())



def is_rich() -> bool:
    return _supports_rich_output()

def _wrap_ansi(rgb: tuple[int, int, int], text:str, *, bold: bool = False) -> str:
    """ Wrap 'text' with ANSI codes for 24bit foreground color."""
    if not is_rich:
        return text
    r, g, b = rgb
    # 38;2;r;g;b = truecolor foreground
    # 1m = bold
    prefix = "\x1b[1m" if bold else ""
    return f"{prefix}\x1b[38;2;{r};{g};{b}m{text}\x1b[0m"

def hex_style(hex_color: str, bold: bool = False) -> StyleFn:
    """Create a style function based on a hex color."""
    rgb = _hex_to_rgb(hex_color)

    def _style(text: str) -> str:
        return _wrap_ansi(rgb, text, bold=bold)
    
    return _style

#Tmeme mapping: keys
theme: Final[Dict[str, StyleFn]] = {
    "accent": hex_style(LOBSTER_PALETTE["accent"]),
    "accentBright": hex_style(LOBSTER_PALETTE["accentBright"]),
    "accentDim": hex_style(LOBSTER_PALETTE["accentDim"]),
    "info": hex_style(LOBSTER_PALETTE["info"]),
    "success": hex_style(LOBSTER_PALETTE["success"]),
    "warn": hex_style(LOBSTER_PALETTE["warn"]),
    "error": hex_style(LOBSTER_PALETTE["error"]),
    "muted": hex_style(LOBSTER_PALETTE["muted"]),
    "heading": hex_style(LOBSTER_PALETTE["accent"], bold=True),
    "command": hex_style(LOBSTER_PALETTE["accentBright"]),
    "option": hex_style(LOBSTER_PALETTE["warn"]),
}

def colorize(rich: bool, color: StyleFn, value: str) -> str:
    return color(value) if rich else value