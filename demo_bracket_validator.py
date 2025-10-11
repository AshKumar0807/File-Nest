"""
Demonstration of bracket validation functionality

This script demonstrates the bracket validation function with examples
similar to those in the problem statement.
"""

from bracket_validator import isValidBrackets


def main():
    print("=" * 60)
    print("Bracket Validation Demonstration")
    print("=" * 60)
    print()
    
    # Example from problem statement (interpreted)
    print("Example 1: Basic bracket validation")
    print("-" * 60)
    
    queries = ["(())", "(()", "[]", "]()"]
    results = isValidBrackets(queries)
    
    print(f"Input queries: {queries}")
    print(f"Results:       {results}")
    print()
    
    # Detailed analysis
    print("Analysis:")
    analyses = [
        '"(())" → All brackets are correctly matched and nested.',
        '"(()" → Missing closing bracket for "("',
        '"[]" → Brackets are properly nested and matched.',
        '"]()\" → Starts with closing bracket "]" without a match.'
    ]
    
    for i, (query, result, analysis) in enumerate(zip(queries, results, analyses), 1):
        print(f"{i}. {analysis}")
        print(f"   Result: {result}")
    
    print()
    print("=" * 60)
    
    # Additional examples
    print("Example 2: More complex bracket sequences")
    print("-" * 60)
    
    queries2 = [
        "()",
        "()[]{}",
        "([{}])",
        "([)]",
        "{[()]}",
        "(((",
        ")))",
        ""
    ]
    results2 = isValidBrackets(queries2)
    
    print(f"{'Query':<15} {'Result'}")
    print("-" * 25)
    for query, result in zip(queries2, results2):
        display_query = f'"{query}"' if query else '(empty string)'
        print(f"{display_query:<15} {result}")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
