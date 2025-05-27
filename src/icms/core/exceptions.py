"""
Custom exception classes for ICMS framework.

This module defines the exception hierarchy used throughout
the ICMS system for error handling and reporting.
"""


class ICMSException(Exception):
    """Base exception for all ICMS-related errors."""

    def __init__(self, message: str, error_code: str = None):
        super().__init__(message)
        self.error_code = error_code or "ICMS_ERROR"


class ParsingException(ICMSException):
    """Raised when comment parsing fails."""

    def __init__(self, message: str, line_number: int = None):
        super().__init__(message, "PARSE_ERROR")
        self.line_number = line_number


class ValidationException(ICMSException):
    """Raised when comment validation fails."""

    def __init__(self, message: str, rule_name: str = None):
        super().__init__(message, "VALIDATION_ERROR")
        self.rule_name = rule_name


class ConfigurationException(ICMSException):
    """Raised when configuration loading or parsing fails."""

    def __init__(self, message: str, config_path: str = None):
        super().__init__(message, "CONFIG_ERROR")
        self.config_path = config_path
