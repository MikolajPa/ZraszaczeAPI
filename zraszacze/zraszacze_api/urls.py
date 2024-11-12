from django.urls import path, include
from .views import (
    TodoListApiView,
    TodoListApiViewDetailed,
    DeviceCrud,
    ScheduleDetailView,
    ScheduleDeviceView,
    MoistureView,
    TemperatureView,
)
from rest_framework import routers

# URL Patterns with better structure
urlpatterns = [
    # Todo related paths
    path('api/todos/', TodoListApiView.as_view(), name='todo-list'),  # GET / POST
    path('api/todos/<int:todo_id>/', TodoListApiViewDetailed.as_view(), name='todo-detail'),  # GET / PUT / DELETE

    # Device related paths
    path('api/devices/', DeviceCrud.as_view(), name='device-crud'),  # Device CRUD
    path('api/devices/<str:device_guid>/schedules/', ScheduleDeviceView.as_view(), name='device-schedule-list'),  # GET / POST
    path('api/devices/<str:device_guid>/schedules/<int:schedule_id>/', ScheduleDetailView.as_view(), name='device-schedule-detail'),  # Schedule detail by ID
    path('api/devices/<str:device_guid>/moisture/', MoistureView.as_view(), name='device-moisture-list'),  # Moisture readings
    path('api/devices/<str:device_guid>/temperature/', TemperatureView.as_view(), name='device-temperature-list'),  # Temperature readings
    path('api/devices/<str:device_guid>/moisture/<int:sensor_id>/', MoistureView.as_view(), name='device-moisture-detail'),  # Moisture by sensor ID
    path('api/devices/<str:device_guid>/temperature/<int:sensor_id>/', TemperatureView.as_view(), name='device-temperature-detail'),  # Temperature by sensor ID
]


