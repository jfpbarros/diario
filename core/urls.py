from django.contrib import admin
from django.urls import path, include #incluir na url o novo app.
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect


urlpatterns = [
    path('admin/', admin.site.urls),
    path('diario/', include('diario.urls')),
    path('', lambda request: redirect('home')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
