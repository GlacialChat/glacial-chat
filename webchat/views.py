from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse


class Index(generic.TemplateView):
    template_name = 'webchat/index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('wcadmin:index'))
        return super(Index, self).dispatch(request, *args, **kwargs)
