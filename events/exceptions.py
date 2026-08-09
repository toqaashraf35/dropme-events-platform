import logging
from rest_framework.views import exception_handler
from .responses import error_response

logger = logging.getLogger('events')


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return error_response(
            message="Request failed",
            errors=response.data,
            status_code=response.status_code,
        )

    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return error_response(
        message="Internal server error",
        errors=None,
        status_code=500,
    )
