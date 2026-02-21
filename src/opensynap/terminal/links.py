"""
Terminal hyperlink helpers
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..utils import TerminalLinkOptions, format_terminal_link

DOCS_ROOT: str = "https://docs.openclaw.ai"


@dataclass(frozen=True)
class DocsLinkOptions:
    fallback: Optional[str] = None
    force: Optional[bool] = None

def format_docs_link(path: str, label: Optional[str] =  None, opts: Optional[DocsLinkOptions] = None) -> str:
    trimmed = path.strip()

    if trimmed.startswith("http"):
        url = trimmed
    else:
        if trimmed.startswith("/"):
            url = f"{DOCS_ROOT}{trimmed}"
        else:
            url = F"{DOCS_ROOT}/{trimmed}"
    return format_terminal_link(
        label or url,
        url,
        TerminalLinkOptions(
            fallback=(opts.fallback if opts and opts.fallback is not None else url),
            force=(opts.force if opts else None),
        ),
    )

def format_docs_root_link(label: Optional[str] = None) -> str:
    return format_terminal_link(
        label or DOCS_ROOT,
        DOCS_ROOT,
        TerminalLinkOptions(fallback=DOCS_ROOT),
    )