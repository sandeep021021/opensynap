"""
Lobster palette tokens for CLI/UI theming.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Final

LOBSTER_PALETTE: Final = MappingProxyType(
    {
        "accent": "#FF5A2D",
        "accentBright": "#FF7A3D",
        "accentDim": "#D14A22",
        "info": "#FF8A5B",
        "success": "#2FBF71",
        "warn": "#FFB020",
        "error": "#E23D2D",
        "muted": "#8B7F77",
    }
)