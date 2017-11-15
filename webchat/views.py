from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import ChatLog, FileLog


class Index(generic.TemplateView):
    template_name = 'webchat/index.html'
    model = ChatLog

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['chatlogs'] = self.model.objects.order_by('-pub_date')
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('admin:index') + "login/?next=" + request.path)
        return super(Index, self).dispatch(request, *args, **kwargs)


class Files(generic.TemplateView):
    model = FileLog
    template_name = 'webchat/files.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('admin:index') + "login/?next=" + request.path)
        return super(Files, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Files, self).get_context_data(**kwargs)
        context['filelogs'] = self.model.objects.order_by('-pub_date')
        return context

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file', None)
        if file is None:
            return HttpResponseRedirect(reverse('webchat:index'))
        obj = self.model(user=request.user, pub_date=timezone.now(), file=file)
        obj.save()
        return HttpResponseRedirect(reverse('webchat:files'))


class Transcript(generic.TemplateView):
    model = ChatLog
    template_name = 'webchat/transcript.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('admin:index') + "login/?next=" + request.path)
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
    http_method_names = ['post']
    template_name = 'webchat/success.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('admin:index') + "login/?next=" + request.path)
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
