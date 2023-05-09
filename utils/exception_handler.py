import re
from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response


def handle_exceptions(exception):
    if isinstance(exception, IntegrityError):
        error_message = str(exception)
        detail_regex = re.compile(r'DETAIL:\s*(.*)$')
        match = detail_regex.search(error_message)
        message = {'detail': f'{match.group(1)}'}
        status_code = status.HTTP_400_BAD_REQUEST
    elif isinstance(exception, KeyError):
        message = {'detail': f'Missing required field: {exception.args[0]}'}
        status_code = status.HTTP_400_BAD_REQUEST
    elif isinstance(exception, ParseError):
        message = {'message': 'Invalid input format.', 'error': str(exception)}
        status_code = status.HTTP_400_BAD_REQUEST
    else:
        message = {'message': 'An error occurred', 'error': str(exception)}
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    return Response(message, status=status_code)