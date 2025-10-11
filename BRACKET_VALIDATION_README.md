# Bracket Validation Module

## Overview

This module provides functionality to validate bracket sequences in strings. It determines whether brackets in a string are properly matched and nested.

## Problem Statement

Given an array of strings where each string contains bracket characters, determine if each string is valid.

A string is valid if:
1. Every opening bracket has a matching closing bracket of the same type
2. Brackets close in the correct order

## Supported Bracket Types

The validator supports three types of brackets:
- Round brackets: `(` and `)`
- Square brackets: `[` and `]`
- Curly brackets: `{` and `}`

## Usage

### Basic Usage

```python
from bracket_validator import isValidBrackets

# Validate an array of bracket sequences
queries = ["(())", "(()", "[]", "]()"]
results = isValidBrackets(queries)
# Returns: ["YES", "NO", "YES", "NO"]
```

### Single String Validation

```python
from bracket_validator import is_valid_bracket_string

# Validate a single string
is_valid = is_valid_bracket_string("([{}])")
# Returns: True
```

## Examples

### Valid Bracket Sequences

```python
"()"        # Simple pair - YES
"[]"        # Simple pair - YES
"{}"        # Simple pair - YES
"([])"      # Nested - YES
"()[]{}"    # Sequential - YES
"([{}])"    # Complex nesting - YES
"{[()]}"    # Multiple levels - YES
""          # Empty string - YES
```

### Invalid Bracket Sequences

```python
"("         # Missing closing bracket - NO
")"         # Missing opening bracket - NO
"(()"       # Incomplete sequence - NO
"]()["      # Starts with closing bracket - NO
"([)]"      # Wrong nesting order - NO
"((("       # All opening, no closing - NO
")))"       # All closing, no opening - NO
```

## Function Reference

### `isValidBrackets(queries)`

Validates an array of strings containing bracket sequences.

**Parameters:**
- `queries` (list): List of strings where each string contains brackets

**Returns:**
- `list`: List of strings where each element is "YES" if the corresponding input string is valid, or "NO" otherwise

**Example:**
```python
queries = ["(())", "(()", "[]", "]()"]
results = isValidBrackets(queries)
# Output: ["YES", "NO", "YES", "NO"]
```

### `is_valid_bracket_string(s)`

Checks if a single string has a valid bracket sequence.

**Parameters:**
- `s` (str): String containing brackets

**Returns:**
- `bool`: True if brackets are valid, False otherwise

**Example:**
```python
is_valid_bracket_string("([{}])")  # Returns: True
is_valid_bracket_string("([)]")    # Returns: False
```

## Algorithm

The validation uses a stack-based approach:

1. Initialize an empty stack
2. Iterate through each character in the string:
   - If it's an opening bracket `(`, `[`, or `{`: push it onto the stack
   - If it's a closing bracket `)`, `]`, or `}`:
     - Check if the stack is empty (no matching opening bracket) → Invalid
     - Check if the top of the stack matches the closing bracket → Invalid if not matching
     - Pop the matching opening bracket from the stack
3. After processing all characters:
   - If the stack is empty: all brackets were matched → Valid
   - If the stack is not empty: unmatched opening brackets remain → Invalid

**Time Complexity:** O(n) where n is the length of the string  
**Space Complexity:** O(n) for the stack in the worst case

## Running Tests

To run the test suite:

```bash
python test_bracket_validator.py
```

## Running Demo

To see a demonstration of the validator:

```bash
python demo_bracket_validator.py
```

## Files

- `bracket_validator.py` - Main implementation
- `test_bracket_validator.py` - Test suite
- `demo_bracket_validator.py` - Demonstration script
- `BRACKET_VALIDATION_README.md` - This documentation

## Notes

- Empty strings are considered valid (no brackets to match)
- Only bracket characters are considered; other characters in the string would need additional handling if required
- The validator is case-sensitive and only recognizes standard ASCII bracket characters
