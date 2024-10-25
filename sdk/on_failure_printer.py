import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class OnFailurePrinter:
    _current_logger_file = None

    def set_current_logger_file(self, file):
        self._current_logger_file = file

    def print_additional_info(self):
        logger.error(f"Current logger file: {self._current_logger_file}")


on_failure_printer = OnFailurePrinter()
