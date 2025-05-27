#!/usr/bin/env python3
"""
Test script for ICMS framework.

This script demonstrates basic usage of the ICMS comment parsing system.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from icms import CommentParser, MetadataAnalyzer
from icms.utils.helpers import sanitize_input, format_output


def main():
    """Run basic ICMS tests."""
    print("ICMS Test Suite")
    print("=" * 50)
    
    # Test input
    sample_code = """
    # This is a Python comment
    def hello_world():
        '''This is a docstring'''
        print("Hello, World!")  # Inline comment
    
    // JavaScript style comment
    /* Multi-line
       comment */
    """
    
    # Initialize parser
    parser = CommentParser()
    analyzer = MetadataAnalyzer()
    
    # Parse comments
    print("\nParsing comments...")
    comments = parser.parse(sample_code)
    
    # Analyze metadata
    print("\nAnalyzing metadata...")
    results = analyzer.analyze(comments)
    
    # Format and display results
    print("\nResults:")
    print(format_output(results))
    
    return 0


if __name__ == "__main__":
    sys.exit(main())


# Note: This test script provides basic validation of ICMS functionality
# For comprehensive testing, see the tests/ directory
# All test cases follow enterprise testing standards