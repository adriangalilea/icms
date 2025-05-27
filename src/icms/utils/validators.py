"""
Validation utilities for ICMS framework.

Provides comprehensive validation functions for comment structures,
metadata compliance, and format verification.
"""

import logging
import re
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


def validate_comment_structure(comment: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Validate the structure of a parsed comment.

    Args:
        comment: Comment dictionary to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ["type", "content", "line_number"]

    for field in required_fields:
        if field not in comment:
            return False, f"Missing required field: {field}"

    if not isinstance(comment.get("line_number"), int):
        return False, "line_number must be an integer"

    if not comment.get("content"):
        return False, "Comment content cannot be empty"

    return True, None


def validate_metadata_tags(tags: List[str]) -> bool:
    """Validate metadata tag format."""
    tag_pattern = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*$")
    return all(tag_pattern.match(tag) for tag in tags)


def validate_encoding(text: str, encoding: str = "utf-8") -> bool:
    """Validate text encoding."""
    try:
        text.encode(encoding)
        return True
    except UnicodeEncodeError:
        return False


def validate_comment_length(comment: str, min_length: int = 1, max_length: int = 1000) -> bool:
    """Validate comment length constraints."""
    return min_length <= len(comment) <= max_length


def validate_pattern_compliance(content: str, patterns: List[str]) -> List[str]:
    """Check content against required patterns."""
    found_patterns = []

    for pattern in patterns:
        if re.search(pattern, content):
            found_patterns.append(pattern)

    return found_patterns


class CommentValidator:
    """Comprehensive comment validation engine."""

    def __init__(self, rules: Optional[Dict[str, Any]] = None):
        self.rules = rules or self._default_rules()

    def _default_rules(self) -> Dict[str, Any]:
        """Return default validation rules."""
        return {
            "min_length": 1,
            "max_length": 1000,
            "required_patterns": [],
            "forbidden_patterns": [],
            "allow_empty": False,
        }

    def validate(self, comment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform full validation on a comment.

        Returns validation results with detailed feedback.
        """
        results = {"valid": True, "errors": [], "warnings": [], "score": 100}

        # Structure validation
        is_valid, error = validate_comment_structure(comment)
        if not is_valid:
            results["valid"] = False
            results["errors"].append(error)
            results["score"] -= 50

        # Content validation
        content = comment.get("content", "")
        if not validate_comment_length(content, self.rules["min_length"], self.rules["max_length"]):
            results["warnings"].append(f"Comment length outside bounds: {len(content)}")
            results["score"] -= 10

        return results
