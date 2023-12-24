from flask import request, jsonify

# returns a standardized API error response.
def handle_api_exception(e, custom_message=None):
    # Log the error, capturing the path of the request and the exception message
    print(f"Error in {request.path}: {str(e)}")
    
    default_error_message = "An error occurred while processing your request. Please try again later."
    
    return jsonify({
        "error": custom_message or default_error_message
    }), 500