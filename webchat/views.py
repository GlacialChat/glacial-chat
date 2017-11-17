"""
All the webchat views are stored here
"""

from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import ChatLog, FileLog

from functools import wraps
from os.path import extsep


def require_auth(_dispatch):
    """
    Decorate this decorator on dispatch method of a view
    requires the requests user to be authenticated to access the page,
    and redirect use back after login
    """
    @wraps(_dispatch)
    def check_auth(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('admin:index') + "login/?next=" + request.path)
        return _dispatch(self, request, *args, **kwargs)
    return check_auth


class Index(generic.TemplateView):
    """
    Index view of glacial chat
    """
    template_name = 'webchat/index.html'
    model = ChatLog

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['chatlogs'] = self.model.objects.order_by('-pub_date')
        return context

    @require_auth
    def dispatch(self, request, *args, **kwargs):
        return super(Index, self).dispatch(request, *args, **kwargs)


class Files(generic.TemplateView):
    """
    Files view of glacial chat
    """
    model = FileLog
    template_name = 'webchat/files.html'

    @require_auth
    def dispatch(self, request, *args, **kwargs):
        return super(Files, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Files, self).get_context_data(**kwargs)
        context['filelogs'] = self.model.objects.order_by('-pub_date')
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', None)
        file = request.FILES.get('file', None)
        if file is None or name is None:
            return HttpResponseRedirect(reverse('webchat:index'))
        if name != '':
            if not name.strip():
                return HttpResponseRedirect(reverse('webchat:files'))
            if extsep not in name and file.name.split(extsep)[-1]:
                name += "." + file.name.split(extsep)[-1]
            file.name = name
        obj = self.model(user=request.user, pub_date=timezone.now(), file=file)
        obj.save()
        return HttpResponseRedirect(reverse('webchat:files'))


class Transcript(generic.TemplateView):
    """
    Transcript view of glacial chat
    """
    model = ChatLog
    template_name = 'webchat/transcript.html'

    @require_auth
    def dispatch(self, request, *args, **kwargs):
        return super(Transcript, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Transcript, self).get_context_data(**kwargs)
        context['chatlogs'] = self.model.objects.order_by('-pub_date')
        return context

    def post(self, request, *args, **kwargs):
        message = request.POST.get("message", None)
        if message is None:
            return HttpResponseRedirect(reverse('webchat:index'))
        obj = self.model(message=message, user=request.user, pub_date=timezone.now())
        obj.save()
        return HttpResponseRedirect(reverse('webchat:transcript'))


class Success(generic.DetailView):
    """
    Success view of glacial chat
    """
    http_method_names = ['post']
    template_name = 'webchat/success.html'

    @require_auth
    def dispatch(self, request, *args, **kwargs):
        return super(Success, self).dispatch(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('webchat:index'))

    def post(self, request, *args, **kwargs):
        message = request.POST.get("message", None)
        if message is None:
            return HttpResponseRedirect(reverse('webchat:index'))
        chat = ChatLog(message=message, user=request.user, pub_date=timezone.now())
        chat.save()
        return render(request, self.template_name)
