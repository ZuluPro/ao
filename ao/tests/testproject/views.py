from django.http import Http404


def debug(request):
    raise Http404(request.body)
