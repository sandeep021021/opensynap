"""
Prompt styling helpers
"""

from __future__ import annotations
from typing import Optional
from .theme import is_rich, theme

def style_prompt_message(message: str) -> str:
    """Style a prompt message"""
    return theme["accent"](message) if is_rich() else message

def style_prompt_title(title: Optional[str] = None) -> Optional[str]:
    """Style a prompt title (heading)"""
    if not title:
        return title
    return theme["heading"](title) if is_rich() else title

def style_prompt_hint(hint: Optional[str] = None) -> Optional[str]:
    if not hint:
        return hint
    return theme["muted"](hint) if is_rich else hint