"""
Helth styling helpers
"""

from __future__ import annotations
from .theme import is_rich, theme

def style_health_ok(value: str) -> str:
    return theme["success"](value) if is_rich() else value

def style_health_warn(value: str) -> str:
    return theme["warn"](value) if is_rich() else value

def style_health_error(value: str) -> str:
    return theme["error"](value) if is_rich else value