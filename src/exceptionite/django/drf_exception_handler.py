from .ExceptioniteReporter import ExceptioniteReporter


def drf_exception_handler(exc, context):
    from rest_framework.views import exception_handler

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data["status_code"] = response.status_code

    # Handle exceptions from drf with exceptionite
    request = context["request"]
    content_type = request.accepted_renderer.media_type
    reporter = ExceptioniteReporter(request, None, exc, None)
    if content_type == "text/html":
        return reporter.get_traceback_html()
    elif content_type == "application/json":
        return reporter.get_traceback_json()

    return response
