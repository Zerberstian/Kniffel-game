"""Gemeinsame Test-Hilfsfunktion: farbiges Logging für Testläufe."""
import logging


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
