import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class CustomFormatter(logging.Formatter):
    """Custom formatter with colors and detailed information"""
    
    grey = "\x1b[38;20m"
    blue = "\x1b[34;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    
    FORMATS = {
        logging.DEBUG: grey + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset,
        logging.INFO: blue + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset,
        logging.WARNING: yellow + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset,
        logging.ERROR: red + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset,
        logging.CRITICAL: bold_red + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance
    
    def _initialize_logger(self):
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # Create logger
        self.logger = logging.getLogger('locust_framework')
        self.logger.setLevel(logging.DEBUG)
        
        # Create handlers
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(CustomFormatter())
        
        # File handler with rotation
        file_handler = RotatingFileHandler(
            filename=f'logs/locust_framework_{datetime.now().strftime("%Y%m%d")}.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        
        # Add handlers to logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def debug(self, message, **kwargs):
        self.logger.debug(self._format_message(message, **kwargs))
    
    def info(self, message, **kwargs):
        self.logger.info(self._format_message(message, **kwargs))
    
    def warning(self, message, **kwargs):
        self.logger.warning(self._format_message(message, **kwargs))
    
    def error(self, message, **kwargs):
        self.logger.error(self._format_message(message, **kwargs))
    
    def critical(self, message, **kwargs):
        self.logger.critical(self._format_message(message, **kwargs))
    
    def _format_message(self, message, **kwargs):
        """Format message with additional context"""
        if kwargs:
            context = ' '.join(f'{k}={v}' for k, v in kwargs.items())
            return f'{message} | {context}'
        return message

# Create a singleton instance
logger = Logger() 