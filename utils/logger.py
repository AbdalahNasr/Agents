"""
Logging utility for Personal Automation Agents.
Provides structured logging with console and file output.
"""

import logging
import colorlog
import os
from datetime import datetime
from typing import Optional
from config import Config

class AgentLogger:
    """Custom logger for automation agents with color coding and structured output."""
    
    def __init__(self, agent_name: str, log_file: Optional[str] = None):
        """
        Initialize logger for a specific agent.
        
        Args:
            agent_name: Name of the agent (e.g., 'email_agent', 'job_agent')
            log_file: Optional custom log file path
        """
        self.agent_name = agent_name
        self.log_file = log_file or Config.LOG_FILE
        
        # Create logger
        self.logger = logging.getLogger(f"agent.{agent_name}")
        self.logger.setLevel(getattr(logging, Config.LOG_LEVEL))
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup console and file handlers with proper formatting."""
        
        # Console handler with colors
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Color formatter for console
        console_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(console_formatter)
        
        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # File formatter (no colors)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        # Add handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def info(self, message: str, **kwargs):
        """Log info message with optional structured data."""
        if kwargs:
            message = f"{message} | {kwargs}"
        self.logger.info(message)
    
    def warning(self, message: str, **kwargs):
        """Log warning message with optional structured data."""
        if kwargs:
            message = f"{message} | {kwargs}"
        self.logger.warning(message)
    
    def error(self, message: str, error: Optional[Exception] = None, **kwargs):
        """Log error message with optional exception details."""
        if error:
            message = f"{message} | Error: {str(error)}"
        if kwargs:
            message = f"{message} | {kwargs}"
        self.logger.error(message, exc_info=bool(error))
    
    def debug(self, message: str, **kwargs):
        """Log debug message with optional structured data."""
        if kwargs:
            message = f"{message} | {kwargs}"
        self.logger.debug(message)
    
    def success(self, message: str, **kwargs):
        """Log success message with optional structured data."""
        if kwargs:
            message = f"{message} | {kwargs}"
        self.logger.info(message)
    
    def action(self, action: str, target: str = None, status: str = "started", **kwargs):
        """Log agent actions with structured format."""
        message = f"ACTION: {action}"
        if target:
            message += f" | Target: {target}"
        message += f" | Status: {status}"
        if kwargs:
            message += f" | {kwargs}"
        
        self.logger.info(message)
    
    def performance(self, operation: str, duration: float, **kwargs):
        """Log performance metrics."""
        message = f"PERFORMANCE: {operation} | Duration: {duration:.2f}s"
        if kwargs:
            message += f" | {kwargs}"
        
        self.logger.info(message)
