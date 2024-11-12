from django.contrib import admin
from django.urls import path, include
from zraszacze_api import urls as zraszacze_urls
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('zraszaczes/', include(zraszacze_urls)),


    path('api/devices/', include('zraszacze_api.Devices.urls', namespace='devices')),
    path('api/schedules/', include('zraszacze_api.Schedules.urls', namespace='devices')),
    path('api/temperature/', include('zraszacze_api.Temperatures.urls', namespace='devices')),
    path('api/moisture/', include('zraszacze_api.Moistures.urls', namespace='devices')),

    # Djoser authentication and JWT URLs combined under one path
    path('auth/', include([
        path('', include('djoser.urls')),
        path('', include('djoser.urls.jwt')),
    ])),

    # Schema and Swagger/Redoc documentation URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
