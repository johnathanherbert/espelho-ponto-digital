from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app.admin import admin_site
from app.views import create_superuser

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('app.urls')),
    path('createauser/', create_superuser, name='create_superuser'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
