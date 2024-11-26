from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
