from django.urls import path
from zraszacze_api.views import MoistureView

app_name = 'devices'

# Device related paths
urlpatterns = [
    # Schedule detail by ID
    path('<str:device_guid>/moisture/', MoistureView.as_view(), name='device-moisture-list'),  # Moisture readings
    path('<str:device_guid>/moisture/<int:sensor_id>/', MoistureView.as_view(), name='device-moisture-detail'),]