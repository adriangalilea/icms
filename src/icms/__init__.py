"""
ICMS - Issue Comment Management System

A comprehensive framework for standardizing comment parsing across
distributed version control systems.
"""

__version__ = "0.1.0"
__author__ = "ICMS Development Team"

from .core.analyzer import MetadataAnalyzer
from .core.parser import CommentParser

__all__ = ["CommentParser", "MetadataAnalyzer"]
