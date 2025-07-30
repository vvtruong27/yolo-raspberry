"""
Logging utility cho hệ thống
"""

import logging
import os
from datetime import datetime
from configs.settings import LOG_LEVEL, LOG_FILE, LOG_FORMAT

class SystemLogger:
    def __init__(self, name="System"):
        self.logger = logging.getLogger(name)
        self.setup_logger()
    
    def setup_logger(self):
        """Thiết lập logger"""
        # Tạo thư mục logs nếu chưa có
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        
        # Thiết lập level
        self.logger.setLevel(getattr(logging, LOG_LEVEL))
        
        # Tạo formatter
        formatter = logging.Formatter(LOG_FORMAT)
        
        # File handler
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        """Log thông tin"""
        self.logger.info(message)
    
    def warning(self, message):
        """Log cảnh báo"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log lỗi"""
        self.logger.error(message)
    
    def debug(self, message):
        """Log debug"""
        self.logger.debug(message)
    
    def critical(self, message):
        """Log lỗi nghiêm trọng"""
        self.logger.critical(message)

# Tạo instance global
system_logger = SystemLogger() 