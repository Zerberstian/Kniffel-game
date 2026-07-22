"""Gemeinsame Test-Hilfsfunktion: farbiges Logging für Testläufe."""
import logging
import tkinter as tk
from typing import Optional


class ColorFormatter(logging.Formatter):
    _COLORS = {
        logging.DEBUG: "\033[90m",
        logging.INFO: "\033[36m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
    }
    _RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        text = super().format(record)
        color = self._COLORS.get(record.levelno, "")
        return f"{color}{text}{self._RESET}" if color else text


def configure_logging() -> None:
    handler = logging.StreamHandler()
    formatter_cls = ColorFormatter if handler.stream.isatty() else logging.Formatter
    handler.setFormatter(formatter_cls("%(levelname)s %(funcName)s: %(message)s"))
    logging.basicConfig(level=logging.INFO, handlers=[handler], force=True)


_shared_root: Optional[tk.Tk] = None


def get_shared_tk_root() -> tk.Tk:
    """Ein einziger Tk-Root für alle GUI-Tests im Prozess.

    Die Tcl/Tk-Installation verkraftet nur ca. 2 tk.Tk()-Erzeugungen pro
    Prozess, danach schlägt das Laden von ttk-Theme-Dateien meist fehl.
    Root bleibt daher unzerstört bis Prozessende (also kein tearDownClass-destroy)
    und wird NICHT withdrawn, da event_generate() ein aktuell gemapptes Fenster braucht.
    """
    global _shared_root
    if _shared_root is None:
        _shared_root = tk.Tk()
    return _shared_root
