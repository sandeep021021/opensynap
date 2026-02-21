"""
Progress line management

Keeps track of a single acive TTy stream used for progress/spinner output a
nd provides a helper to clear that line 
"""

from __future__ import annotations
from typing import Optional , TextIO

_active_stream: Optional[TextIO] = None

def _is_tty(stream: TextIO) -> bool:
    try:
        return bool(stream.isatty())
    except Exception:
        return False
    

def register_active_progress_line(stream: TextIO, *, force: bool = False) -> None:
    # Register a TTY stream as active progress line
    global _active_stream
    if not force and not _is_tty(stream):
        return
    _active_stream = stream


def clear_active_progress_line() -> None:
    # Clear the active progress line of a TTY stream is registered.
    if _active_stream is None:
        return
    if not _is_tty(_active_stream):
        return
    _active_stream.write("\r\x1b[2K")
    _active_stream.flush()


def unregister_active_progress_line(stream: Optional[TextIO] = None) -> None:
    """Unregister the active progress line stream 
    (optionally only if it matches)
    """
    global _active_stream
    if _active_stream is None:
        return
    if stream is not None and _active_stream is not stream:
        return
    _active_stream = None