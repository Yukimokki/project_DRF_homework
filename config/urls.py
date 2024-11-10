from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from config.settings import MEDIA_URL



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('course_materials.urls', namespace='courses')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
