from django.conf import settings
from django import http
from django.template import Context, loader

def server_500_error(request, template_name='500.html'):
    t = loader.get_template(template_name) # You need to create a 500.html template.
    return http.HttpResponseServerError(t.render(Context({
        'MEDIA_URL': settings.MEDIA_URL
    })))

def server_404_error(request, template_name='404.html'):
    t = loader.get_template(template_name) # You need to create a 404.html template.
    return http.HttpResponseServerError(t.render(Context({
        'MEDIA_URL': settings.MEDIA_URL
    })))
