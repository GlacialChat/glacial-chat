from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import ChatLog


class Index(generic.TemplateView):
    template_name = 'webchat/index.html'
    model = ChatLog

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['chatlogs'] = self.model.objects.order_by('-pub_date')
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('admin:index') + "login/?next=" + reverse('webchat:index'))
        return super(Index, self).dispatch(request, *args, **kwargs)


class Success(generic.DetailView):
    http_method_names = ['post']
    template_name = 'webchat/success.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('admin:index') + "login/?next=" + reverse('webchat:index'))
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
