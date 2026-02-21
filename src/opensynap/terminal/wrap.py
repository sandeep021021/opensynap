from __future__ import annotations

import re
import shutil
from typing import Optional

from .ansi import visible_width


_URL_PREFIX_RE = re.compile(r"^(https?://|file://)", re.IGNORECASE)
_WINDOWS_DRIVE_RE = re.compile(r"^[a-zA-Z]:[\\/]")
_FILE_LIKE_RE = re.compile(r"^[a-zA-Z0-9._-]+$")


def split_long_word(word: str, max_len: int) -> list[str]:
    if max_len <= 0:
        return [word]
    chars = list(word)
    return ["".join(chars[i : i + max_len]) for i in range(0, len(chars), max_len)] or [word]


def is_copy_sensitive_token(word: str) -> bool:
    if not word:
        return False
    if _URL_PREFIX_RE.search(word):
        return True
    if word.startswith(("/", "~/", "./", "../")):
        return True
    if _WINDOWS_DRIVE_RE.match(word) or word.startswith("\\\\"):
        return True
    if ("/" in word) or ("\\" in word):
        return True
    return ("_" in word) and bool(_FILE_LIKE_RE.match(word))


def wrap_line(line: str, max_width: int) -> list[str]:
    if line.strip() == "":
        return [""]

    m = re.match(r"^(\s*)([-*\u2022]\s+)?(.*)$", line)
    indent = m.group(1) if m else ""
    bullet = m.group(2) if (m and m.group(2)) else ""
    content = m.group(3) if m else line

    first_prefix = f"{indent}{bullet}"
    next_prefix = f"{indent}{' ' * len(bullet) if bullet else ''}"

    first_width = max(10, max_width - visible_width(first_prefix))
    next_width = max(10, max_width - visible_width(next_prefix))

    words = [w for w in re.split(r"\s+", content) if w]
    out: list[str] = []

    current = ""
    prefix = first_prefix
    available = first_width

    for word in words:
        if not current:
            if visible_width(word) > available:
                if is_copy_sensitive_token(word):
                    current = word
                    continue
                parts = split_long_word(word, available)
                out.append(prefix + parts[0])
                prefix = next_prefix
                available = next_width
                out.extend(prefix + p for p in parts[1:])
                continue
            current = word
            continue

        cand = f"{current} {word}"
        if visible_width(cand) <= available:
            current = cand
            continue

        out.append(prefix + current)
        prefix = next_prefix
        available = next_width

        if visible_width(word) > available:
            if is_copy_sensitive_token(word):
                current = word
                continue
            parts = split_long_word(word, available)
            out.append(prefix + parts[0])
            out.extend(prefix + p for p in parts[1:])
            current = ""
            continue

        current = word

    out.append(prefix + current)
    return out


def wrap_note_message(message: str, *, max_width: Optional[int] = None, columns: Optional[int] = None) -> str:
    term_cols = columns if columns is not None else shutil.get_terminal_size((80, 20)).columns
    width = max_width if max_width is not None else max(42, min(86, term_cols - 12))

    lines: list[str] = []
    for raw in message.split("\n"):
        lines.extend(wrap_line(raw, width))
    return "\n".join(lines)