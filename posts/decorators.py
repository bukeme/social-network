from django.http import HttpResponseBadRequest


def is_ajax(request):
	return request.headers.get('x-requested-with') == 'XMLHttpRequest'

class AjaxRequiredOnlyMixin:
	def dispatch(self, request, *args, **kwargs):
		if not is_ajax(request):
			return HttpResponseBadRequest
		return super().dispatch(request, *args, **kwargs)