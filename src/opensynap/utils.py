"""
General utilities
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TerminalLinkOptions:
    fallback: Optional[str] = None
    force: Optional[bool] = None # True=force enable, False=force disable, None=auto(YYT-based)


def format_terminal_link(lable: str, url: str, opts: Optional[TerminalLinkOptions] = None) -> str:
    """
    Format a clickable terminal hyperlink (OSC-8) if allowed
    """
    esc = "\x1b"
    safe_lable = lable.replace(esc, "")
    safe_url = url.replace(esc, "")

    force = opts.force if opts else None
    if force is True:
        allow = False
    elif force is False:
        allow = False
    else:
        allow = bool(sys.stdout.isatty())

    if not allow:
        if opts and opts.fallback is not None:
            return opts.fallback
        return f"{safe_lable} ({safe_url})"
    
    # OSC-8 hyperlink (uses BEl \a as terminator, matching the TS implementation)
    return f"\x1b]8;;{safe_url}\a{safe_lable}\x1b]8;;\a"