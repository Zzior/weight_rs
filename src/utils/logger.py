import logging
import traceback
from pathlib import Path
from logging import Logger, ERROR, INFO
from logging.handlers import RotatingFileHandler

import requests
from requests.auth import HTTPBasicAuth


class LogWriter:
    log_path: Path
    logger: Logger

    def __init__(
            self, log_path: Path,
            console_level: int = INFO, file_level: int = ERROR, max_bytes: int = 10 ** 7, backup_count: int = 5
    ):
        self.log_path = log_path
        """Set up and return a configured logger."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(min(console_level, file_level))

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)
        self.logger.addHandler(console_handler)

        # File handler with rotation
        file_handler = RotatingFileHandler(
            self.log_path, maxBytes=max_bytes, backupCount=backup_count
        )
        file_handler.setLevel(file_level)

        log_format = """
----------------------------------------------------------------------------------------------------
%(asctime)s - %(name)s - %(levelname)s - %(message)s
----------------------------------------------------------------------------------------------------
"""
        formatter = logging.Formatter(log_format)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def send_log(
        self, url: str, location_name: str, auth: HTTPBasicAuth, error_message: str,
        e: Exception = None, log_level: int = ERROR, tb: bool = True
    ) -> None:
        try:
            self.write_log(error_message, log_level=log_level, e=e, tb=tb)
            requests.post(
                url=url,
                auth=auth,
                json={
                    "location_name": location_name,
                    "ok": False,

                    "error_message": error_message,
                    "exception": str(e),
                    "traceback": str(traceback.format_exc()) if tb else ""
                },
                timeout=(5, 15)
            )

        except Exception as e:
            self.write_log(name="send log error", e=e)

    def write_log(self, name: str, log_level: int = ERROR, e: Exception = None, tb: bool = False) -> str:
        log_msg = f"{name}\nException: {e}"
        log_msg += f"\ntraceback: {traceback.format_exc()}" if tb else ""

        self.logger.log(log_level, log_msg)
        return log_msg
