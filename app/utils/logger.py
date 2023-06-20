import logging.handlers
import os


class Logger:
    """
    Environment Variables:
        PROJECT__NAME
        LOGFILE__LOCATION
        LOGGER__LEVEL
    """

    Logger = None

    def initialize(self, enable_notifications=True):
        # Logger setup
        self.logging_service = os.getenv("PROJECT__NAME", "my-project")
        self.default_location = "logs/"
        self.Logger = logging.getLogger(f"{self.logging_service}_logger")
        self.Logger.setLevel(logging.DEBUG)
        self.Logger.propagate = False
        self.formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.logger_to_file()
        self.logging_to_console()

    def logger_to_file(self):
        os.makedirs(os.getenv("LOGFILE__LOCATION", self.default_location), exist_ok=True)
        fh = logging.FileHandler(os.path.join(os.getenv("LOGFILE__LOCATION", self.default_location), f"{self.logging_service}.log"))
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.Logger.addHandler(fh)

    def logging_to_console(self):
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(self.formatter)
        self.Logger.addHandler(ch)

    def log(self, message, level=os.getenv("LOGGER__LEVEL", "info"), notification=True):
        if level == "info":
            self.Logger.info(message)
        elif level == "warning":
            self.Logger.warning(message)
        elif level == "error":
            self.Logger.error(message)
        elif level == "debug":
            self.Logger.debug(message)

    def info(self, message, notification=True):
        self.log(message, "info", notification)

    def warning(self, message, notification=True):
        self.log(message, "warning", notification)

    def error(self, message, notification=True):
        self.log(message, "error", notification)

    def debug(self, message, notification=False):
        self.log(message, "debug", notification)


logger = Logger()