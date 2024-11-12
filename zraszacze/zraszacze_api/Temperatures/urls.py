from django.urls import path
from zraszacze_api.views import TemperatureView

app_name = 'devices'

# Device related paths
urlpatterns = [
    path('<str:device_guid>/temperature/', TemperatureView.as_view(), name='device-temperature-list'),  # Temperature readings
    path('<str:device_guid>/temperature/<int:sensor_id>/', TemperatureView.as_view(), name='device-temperature-detail'),  # Temperature by sensor ID
]