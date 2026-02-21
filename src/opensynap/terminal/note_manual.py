from __future__ import annotations

import shutil
from typing import Optional

from .ansi import visible_width
from .theme import is_rich, theme
from .wrap import wrap_note_message # reuse wrapping logic


def _repeat(ch: str, n: int) -> str:
    return ch * max(0, n)


def note_manual(message: str, title: Optional[str] = None) -> None:
    """
    Manual clack-like note box using unicode borders.
    No rich dependency. Uses our theme for dim/bold/accent.
    """
    cols = shutil.get_terminal_size((80, 20)).columns
    width = max(42, min(86, cols - 12))

    content = wrap_note_message(message, max_width=width)
    lines = content.split("\n")

    # Layout knobs (tune these to match clack visually)
    pad_x = 2
    pad_y = 1

    # Compute inner width from longest visible line
    inner_content_width = max((visible_width(l) for l in lines), default=0)
    inner_width = min(width, max(20, inner_content_width + pad_x * 2))

    # Border chars (rounded look)
    tl, tr, bl, br = "╭", "╮", "╰", "╯"
    hz, vt = "─", "│"

    # Title line (subtle)
    t = title or "Note"
    if is_rich():
        t = theme["heading"](t)  # bold-ish
    title_text = f" {t} "

    # top border with title embedded (like a label)
    # We'll place title after tl and one hz. Keep it simple & pretty.
    top_available = inner_width
    title_len = visible_width(title_text)
    # ensure title fits; if too long, just omit label
    if title_len + 2 <= top_available:
        left_hz = 1
        right_hz = top_available - left_hz - title_len
        top = tl + _repeat(hz, left_hz) + title_text + _repeat(hz, right_hz) + tr
    else:
        top = tl + _repeat(hz, top_available) + tr

    # body
    body_lines = []
    dim_prefix = theme["muted"] if is_rich() else (lambda x: x)

    # vertical padding top
    for _ in range(pad_y):
        body_lines.append(vt + _repeat(" ", inner_width) + vt)

    # content lines
    for l in lines:
        vis = visible_width(l)
        right_spaces = inner_width - (pad_x + vis)
        body_lines.append(
            vt
            + _repeat(" ", pad_x)
            + dim_prefix(l)
            + _repeat(" ", max(0, right_spaces))
            + vt
        )

    # vertical padding bottom
    for _ in range(pad_y):
        body_lines.append(vt + _repeat(" ", inner_width) + vt)

    bottom = bl + _repeat(hz, inner_width) + br

    print()
    print(top)
    for bln in body_lines:
        print(bln)
    print(bottom)
    print()