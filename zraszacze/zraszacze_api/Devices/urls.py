from django.urls import path
from zraszacze_api.views import DeviceCrud

app_name = 'devices'

# Device related paths
urlpatterns = [
    path('', DeviceCrud.as_view(), name='device-crud'),  # Device CRUD
]