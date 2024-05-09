from django.shortcuts import render
from django.urls import re_path, include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from user import views as uview

# Define your custom handler404 and handler500 views
def custom_handler404(request, exception, template_name='404.html'):
    return render(request, template_name, status=404)

def custom_handler500(request, template_name='500.html'):
    return render(request, template_name, status=500)

urlpatterns = [
    re_path(r'^', include('user.urls')),
    re_path(r'^asi/', include('asi.urls')),
    re_path(r'^onsite/', include('onsite.urls')),
    path('admin/', admin.site.urls),
]

# Add your custom 404 and 500 views
handler404 = custom_handler404
handler500 = custom_handler500

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
