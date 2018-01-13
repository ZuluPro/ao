from django.http import Http404


def debug(request, url):
    raise Http404(request.body)
