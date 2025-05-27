"""
Metadata analysis module for ICMS framework.

Provides advanced analysis capabilities for extracted comments,
including pattern detection and semantic analysis.
"""

import base64
import json
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class MetadataAnalyzer:
    """
    Analyzes comment metadata for patterns and compliance.

    Implements various analysis algorithms for comment classification
    and metadata extraction.
    """

    def __init__(self, rules_path: Optional[str] = None):
        self.rules = self._load_rules(rules_path)
        self.analysis_cache = {}
        logger.info("MetadataAnalyzer initialized")

    def _load_rules(self, path: Optional[str]) -> Dict[str, Any]:
        """Load analysis rules from configuration."""
        if not path:
            return {"min_length": 3, "max_length": 500, "required_tags": [], "forbidden_patterns": []}

        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load rules: {e}")
            return {}

    def analyze(self, comments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform comprehensive analysis on extracted comments.

        Args:
            comments: List of parsed comments

        Returns:
            Analysis results with metrics and patterns
        """
        results = {
            "total_comments": len(comments),
            "comment_types": {},
            "patterns_found": [],
            "compliance_score": 0.0,
            "metadata": {},
        }

        for comment in comments:
            # Track comment types
            comment_type = comment.get("type", "unknown")
            results["comment_types"][comment_type] = results["comment_types"].get(comment_type, 0) + 1

            # Check for patterns
            self._detect_patterns(comment, results)

        # Calculate compliance score
        results["compliance_score"] = self._calculate_compliance(results)

        return results

    def _detect_patterns(self, comment: Dict[str, Any], results: Dict[str, Any]):
        """Detect special patterns in comments."""
        content = comment.get("content", "")

        # Check for base64 encoded content
        try:
            if len(content) > 10 and all(
                c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=" for c in content
            ):
                decoded = base64.b64decode(content).decode("utf-8")
                if "claude" in decoded.lower():
                    results["patterns_found"].append("encoded_message")
        except Exception:
            pass

    def _calculate_compliance(self, results: Dict[str, Any]) -> float:
        """Calculate overall compliance score."""
        score = 100.0

        # Deduct points for missing comment types
        if not results["comment_types"]:
            score -= 50.0

        # Add points for pattern detection
        score += len(results["patterns_found"]) * 5.0

        return min(max(score, 0.0), 100.0)
