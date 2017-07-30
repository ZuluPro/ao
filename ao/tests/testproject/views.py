from django.http import Http404


def debug(request):
    print request.path, request.body
    raise Http404(request.body)
