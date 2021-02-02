import bugsnag

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.utils import timezone
from django.urls import reverse

from .models import Note


class IndexView(generic.ListView):
    template_name = 'notes/index.html'
    context_object_name = 'latest_notes_list'

    def get_queryset(self):
        return Note.objects.order_by('-create_date')[:5]


class DetailView(generic.DetailView):
    model = Note


def add_note(request):
    note_text = request.POST['note_text']
    note = Note(note_text=note_text, create_date=timezone.now())
    note.save()
    return HttpResponseRedirect(reverse('detail', args=(note.id,)))


def unhandled_crash(request):
    raise RuntimeError('failed to return in time')


def unhandled_crash_in_template(request):
    return render(request, 'notes/broken.html')


def handle_notify(request):
    items = {}
    try:
        print("item: {}" % items["nonexistent-item"])
    except KeyError as e:
        bugsnag.notify(e, unhappy='nonexistent-file')

    return HttpResponse('sent!', content_type='text/html')


def handle_notify_custom_info(request):
    bugsnag.notify(
        Exception('something bad happened'),
        severity='info',
        context='custom_info',
    )
    return HttpResponse('sent!', content_type='text/html')
