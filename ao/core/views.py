from rest_framework import views


def exception_handler(exc, context):
    response = views.exception_handler(exc, context)
    if response is not None:
        response.data = exc.get_full_details()
    return response
