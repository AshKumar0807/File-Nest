"""
Bracket Validation Module

This module provides functionality to validate bracket sequences in strings.
A string is valid if:
1. Every opening bracket has a matching closing bracket of the same type
2. Brackets close in the correct order
"""


def isValidBrackets(queries):
    """
    Validates an array of strings containing bracket sequences.
    
    Args:
        queries: List of strings where each string contains brackets
        
    Returns:
        List of strings where each element is "YES" if the corresponding 
        input string is valid, or "NO" otherwise.
        
    Example:
        >>> isValidBrackets(["()", "((", "[]", "[(])"])
        ["YES", "NO", "YES", "NO"]
    """
    results = []
    
    for query in queries:
        if is_valid_bracket_string(query):
            results.append("YES")
        else:
            results.append("NO")
    
    return results


def is_valid_bracket_string(s):
    """
    Checks if a single string has valid bracket sequence.
    
    Args:
        s: String containing brackets
        
    Returns:
        True if brackets are valid, False otherwise
    """
    # Stack to keep track of opening brackets
    stack = []
    
    # Mapping of closing brackets to their corresponding opening brackets
    bracket_map = {
        ')': '(',
        ']': '[',
        '}': '{'
    }
    
    for char in s:
        # If it's an opening bracket, push to stack
        if char in '([{':
            stack.append(char)
        # If it's a closing bracket
        elif char in ')]}':
            # Check if stack is empty (no matching opening bracket)
            if not stack:
                return False
            # Check if the top of stack matches the closing bracket
            if stack[-1] != bracket_map[char]:
                return False
            # Pop the matching opening bracket
            stack.pop()
    
    # If stack is empty, all brackets were matched
    return len(stack) == 0
