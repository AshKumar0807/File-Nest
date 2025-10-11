"""
Test file for bracket validation functionality
"""

from bracket_validator import isValidBrackets, is_valid_bracket_string


def test_basic_examples():
    """Test with basic bracket examples"""
    # Test individual bracket types
    assert is_valid_bracket_string("()") == True
    assert is_valid_bracket_string("[]") == True
    assert is_valid_bracket_string("{}") == True
    
    # Test nested brackets
    assert is_valid_bracket_string("([])") == True
    assert is_valid_bracket_string("{[()]}") == True
    
    # Test invalid sequences
    assert is_valid_bracket_string("(") == False
    assert is_valid_bracket_string(")") == False
    assert is_valid_bracket_string(")(") == False
    assert is_valid_bracket_string("([)]") == False
    
    print("✓ Basic examples passed")


def test_problem_statement_examples():
    """Test with examples from problem statement"""
    # Based on the problem statement examples (interpreting "0" as brackets)
    # Example 1: "(())" - All brackets correctly matched and nested
    assert is_valid_bracket_string("(())") == True
    
    # Example 2: "(()" - Missing closing bracket
    assert is_valid_bracket_string("(()") == False
    
    # Example 3: "[]" - Properly nested and matched
    assert is_valid_bracket_string("[]") == True
    
    # Example 4: "]()" - Starts with closing bracket without a match
    assert is_valid_bracket_string("]()") == False
    
    print("✓ Problem statement examples passed")


def test_isValidBrackets_function():
    """Test the main function with arrays"""
    # Test case from problem statement interpretation
    queries = ["(())", "(()", "[]", "]()"]
    expected = ["YES", "NO", "YES", "NO"]
    result = isValidBrackets(queries)
    
    assert result == expected, f"Expected {expected}, but got {result}"
    
    # Additional test cases
    queries2 = ["()", "{}", "[]", "([{}])", "([)]", "((", "))", ""]
    expected2 = ["YES", "YES", "YES", "YES", "NO", "NO", "NO", "YES"]
    result2 = isValidBrackets(queries2)
    
    assert result2 == expected2, f"Expected {expected2}, but got {result2}"
    
    print("✓ isValidBrackets function passed")


def test_edge_cases():
    """Test edge cases"""
    # Empty string
    assert is_valid_bracket_string("") == True
    
    # Multiple bracket types
    assert is_valid_bracket_string("()[]{}") == True
    assert is_valid_bracket_string("([{}])") == True
    
    # Complex nested structures
    assert is_valid_bracket_string("(((())))") == True
    assert is_valid_bracket_string("((((())") == False
    
    # Interleaved but valid
    assert is_valid_bracket_string("()()()") == True
    assert is_valid_bracket_string("([])[]{}") == True
    
    # Invalid interleaving
    assert is_valid_bracket_string("([)]") == False
    assert is_valid_bracket_string("{[(])}") == False
    
    print("✓ Edge cases passed")


def test_with_non_bracket_characters():
    """Test strings that might contain non-bracket characters"""
    # Based on problem description, we should only consider brackets
    # For now, testing with just brackets as per problem statement
    pass


if __name__ == "__main__":
    print("Running bracket validation tests...")
    print()
    
    test_basic_examples()
    test_problem_statement_examples()
    test_isValidBrackets_function()
    test_edge_cases()
    
    print()
    print("✓ All tests passed successfully!")
