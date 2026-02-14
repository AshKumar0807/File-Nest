"""
Optional Flask Integration Example for Bracket Validator

This file demonstrates how the bracket validator could be integrated
into the existing Flask application if needed.
"""

from flask import Flask, request, jsonify
from bracket_validator import isValidBrackets, is_valid_bracket_string

# This is an example of how to add bracket validation endpoints
# to the existing Flask app in app.py

# Example endpoint 1: Validate a single bracket string
# @app.route('/api/validate-bracket', methods=['POST'])
# def validate_single_bracket():
#     """
#     Validates a single bracket string
#     
#     Expected JSON: {"query": "(())"}
#     Returns: {"valid": true, "result": "YES"}
#     """
#     data = request.get_json()
#     query = data.get('query', '')
#     
#     is_valid = is_valid_bracket_string(query)
#     result = "YES" if is_valid else "NO"
#     
#     return jsonify({
#         'query': query,
#         'valid': is_valid,
#         'result': result
#     })


# Example endpoint 2: Validate multiple bracket strings
# @app.route('/api/validate-brackets', methods=['POST'])
# def validate_multiple_brackets():
#     """
#     Validates multiple bracket strings
#     
#     Expected JSON: {"queries": ["(())", "(()", "[]"]}
#     Returns: {"results": ["YES", "NO", "YES"]}
#     """
#     data = request.get_json()
#     queries = data.get('queries', [])
#     
#     if not isinstance(queries, list):
#         return jsonify({'error': 'queries must be an array'}), 400
#     
#     results = isValidBrackets(queries)
#     
#     return jsonify({
#         'queries': queries,
#         'results': results
#     })


# Example usage in code:
def example_usage():
    """
    Example of using bracket validation in the application logic
    """
    # Validate user input
    user_input = "(())"
    if is_valid_bracket_string(user_input):
        print("Valid bracket sequence!")
    else:
        print("Invalid bracket sequence!")
    
    # Batch validation
    queries = ["()", "(()", "[]", "]()"]
    results = isValidBrackets(queries)
    for query, result in zip(queries, results):
        print(f"{query}: {result}")


# To integrate into app.py, simply add the above route definitions
# after the existing routes in app.py and import the bracket_validator functions.
