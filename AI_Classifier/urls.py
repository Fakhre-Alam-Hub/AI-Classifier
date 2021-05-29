from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.static import serve
from django.conf.urls import url


admin.site.site_header = "AI Classifier Admin"
admin.site.site_title = "AI Classifier Admin Portal"
admin.site.index_title = "Welcome to AI Classifier"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),

    # For heroku
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)