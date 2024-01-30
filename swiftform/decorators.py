from flask import request, abort
from functools import wraps

def require_fields(required_fields):
    """
    Decorator to ensure that specific fields are present in a JSON request.

    Args:
    required_fields (list of str): A list of field names that are expected in the request's JSON data.

    Returns:
    function: A wrapper function that decorates the original view function.

    The decorator first checks for the presence of all required fields in the request's JSON data.
    If any field is missing, it constructs an error message with the missing field names and sends
    a 400 Bad Request error response. If all required fields are present, it allows the original view
    function to process the request normally.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            missing_fields = [field for field in required_fields if field not in request.json]
            if missing_fields:
                description = f"Missing required fields: {', '.join(missing_fields)}"
                abort(400, description=description)
            else:
                return func(*args, **kwargs)
            
        return wrapper
    
    return decorator
