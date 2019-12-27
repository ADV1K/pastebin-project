from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse

from .models import Paste


def index(request):
	return render(request, 'pastebin/index.html')


def details(request, paste_id):
	paste = get_object_or_404(Paste, pk=paste_id)
	return render(request, 'pastebin/details.html', {'paste': paste})


def raw(request, paste_id):
	paste = get_object_or_404(Paste, pk=paste_id)
	return HttpResponse(paste.paste_code, content_type='text/plain')


def latest(request, n=20):
	latest_paste_list = Paste.objects.order_by('-pub_date')[:n]
	return render(request, 'pastebin/latest.html', {'latest_paste_list': latest_paste_list})


def create(request):
	try:
		paste_title = request.POST.get('paste_title', 'Untitled')
		paste_format = request.POST.get('paste_format', 'Plain Text')
		paste_code = request.POST['paste_code']
		if len(paste_code) == 0:
			raise ValueError
	except (KeyError, ValueError):
		# Redisplay the index page with error message.
		return render(request, 'pastebin/index.html', {
			'error_message': "Empty paste are not allowed.",
		})
	else:
		paste = Paste(paste_title=paste_title, paste_code=paste_code, paste_format=paste_format, pub_date=timezone.now())
		paste.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('pastebin:details', args=(paste.id,)))


def download(request, paste_id):
	# https://stackoverflow.com/questions/1156246/having-django-serve-downloadable-files
	# https://stackoverflow.com/questions/36392510/django-download-a-file
	paste = get_object_or_404(Paste, pk=paste_id)
	response = HttpResponse(paste.paste_code, content_type='application/force-download')
	response['Content-Disposition'] = 'inline; filename=%s.txt' % paste.paste_title
	response['Content-Length'] = len(paste.paste_code)
	return response
