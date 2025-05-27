"""
Core parser implementation for ICMS framework.

This module provides the main parsing functionality for extracting
comments from various source code formats.
"""

import logging
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class BaseParser(ABC):
    """Abstract base class for all parser implementations."""

    @abstractmethod
    def parse(self, content: str) -> List[Dict[str, Any]]:
        """Parse content and extract comments."""
        pass

    @abstractmethod
    def validate(self, comment: Dict[str, Any]) -> bool:
        """Validate a single comment."""
        pass


class CommentParser(BaseParser):
    """
    Main parser implementation for comment extraction.

    Supports multiple programming languages and comment styles.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._compile_patterns()
        logger.info("CommentParser initialized")

    def _compile_patterns(self):
        """Compile regex patterns for different comment styles."""
        self.patterns = {
            "single_line": re.compile(r"(?:#|//|--)\s*(.*)$", re.MULTILINE),
            "multi_line": re.compile(r"/\*\s*(.*?)\s*\*/", re.DOTALL),
            "doc_string": re.compile(r'"""(.*?)"""', re.DOTALL),
        }

    def parse(self, content: str) -> List[Dict[str, Any]]:
        """
        Parse content and extract all comments.

        Args:
            content: Source code content to parse

        Returns:
            List of comment dictionaries with metadata
        """
        if not content:
            return []

        comments = []
        lines = content.split("\n")

        # Process line by line for single-line comments
        for line_num, line in enumerate(lines, 1):
            for pattern_name, pattern in self.patterns.items():
                if pattern_name == "single_line":
                    match = pattern.search(line)
                    if match:
                        comments.append(
                            {
                                "type": "single_line",
                                "content": match.group(1).strip(),
                                "line_number": line_num,
                                "raw": line.strip(),
                            }
                        )

        return comments

    def validate(self, comment: Dict[str, Any]) -> bool:
        """Validate comment structure and content."""
        required_fields = ["type", "content", "line_number"]
        return all(field in comment for field in required_fields)
