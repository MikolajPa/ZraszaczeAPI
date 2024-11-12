from django.urls import path
from zraszacze_api.views import DeviceCrud, ScheduleDeviceView,ScheduleDetailView, MoistureView, TemperatureView

app_name = 'devices'

# Device related paths
urlpatterns = [
    path('<str:device_guid>/schedules/', ScheduleDeviceView.as_view(), name='device-schedule-list'),  # GET / POST
    path('<str:device_guid>/schedules/<int:schedule_id>/', ScheduleDetailView.as_view(), name='device-schedule-detail'),  # Schedule detail by ID
]