"""
SAFE STREAM WRITER
"""

from __future__ import annotations

import errno
import sys
from dataclasses import dataclass
from typing import Callable, Optional, Protocol, TextIO


class WriteStream(Protocol):
    def write(self, s: str) -> int: ...
    def flush(self) -> None: ...


BeforeWrite = Callable[[], None]
OnBrokenPipe = Callable[[BaseException, WriteStream], None]

@dataclass(frozen=True)
class SafeStreamWriterOptions:
    before_write: Optional[BeforeWrite] = None
    on_broken_pipe: Optional[OnBrokenPipe] = None


def _is_broken_pipe_error(err: BaseException) -> bool:
    if isinstance(err, BrokenPipeError):
        return True
    if isinstance(err, OSError):
        return err.errno in (errno.EPIPE, errno.EIO)
    return False


class SafeStreamWriter:
    def __init__(self, options: SafeStreamWriterOptions =SafeStreamWriterOptions()):
        self._options = options
        self._closed = False
        self._notified = False

    def reset(self) -> None:
        self._closed = False
        self._notified = False

    def is_closed(self) -> bool:
        return self._closed
    
    def _note_broken_pipe(self, err: BaseException, stream: WriteStream) -> None:
        if self._notified:
            return
        self._notified = True
        if self._options.on_broken_pipe is not None:
            self._options.on_broken_pipe(err, stream)
    
    def _handle_error(self, err: BaseException, stream: WriteStream) -> bool:
        if not _is_broken_pipe_error(err):
            raise err
        self._closed = True
        self._note_broken_pipe(err, stream)
        return False
    
    def write(self, stream: WriteStream, text: str) -> bool:
        if self._closed:
            return False
        
        # before_write hook
        if self._options.before_write is not None:
            try:
                self._options.before_write()
            except BaseException as err:
                # TS version reports hook errors against stderr stream
                return self._handle_error(err, sys.stderr)
            
        try:
            stream.write(text)
            try:
                stream.flush()
            except Exception:
                # Flush issue usuallu aren't fatal; ignore unless they are broken pipe
                pass
            return not self._closed
        except BaseException as err:
            return self._handle_error(err, stream)
        
    def write_line(self, stream: WriteStream, text: str) -> bool:
        return self.write(stream, f"{text}\n")
    

def create_safe_stream_writer(options: SafeStreamWriterOptions  = SafeStreamWriterOptions()) -> SafeStreamWriter:
    return SafeStreamWriter(options)