from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from app.admin import admin_site
from app.views import create_superuser, serve_pdf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('createauser/', create_superuser, name='create_superuser'),
    re_path(r'^media/(?P<path>.*)$', serve_pdf),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
