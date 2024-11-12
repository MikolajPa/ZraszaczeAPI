from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Todo, Device, Schedule, Temperature, Moisture
from .serializers import TodoSerializer, DeviceSerializer, ScheduleSerializer, MoistureSerializer, TemperatureSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

class TodoListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self, todo_id, user_id):
        try:
            return Todo.objects.get(id=todo_id, user = user_id)
        except Todo.DoesNotExist:
            return None

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        todos = Todo.objects.filter(user = request.user.id)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class TodoListApiViewDetailed(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self, todo_id, user_id):
        try:
            return Todo.objects.get(id=todo_id, user = user_id)
        except Todo.DoesNotExist:
            return None
        
    def get(self, request, todo_id, *args, **kwargs):
        '''
        Retrieves the Todo with given todo_id
        '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, todo_id, *args, **kwargs):
        '''
        Updates the todo item with given todo_id if exists
        '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = TodoSerializer(instance = todo_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, todo_id, *args, **kwargs):

        '''
        Deletes the todo item with given todo_id if exists
        '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
    

class DeviceCrud(APIView):
    @swagger_auto_schema(tags=["Devices"], operation_summary="List all devices")
    def get(self, request, *args, **kwargs):
        devices = Device.objects
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Devices"], operation_summary="Create a new device")
    def post(self, request, *args, **kwargs):
        data = {
            'GUID': request.data.get('GUID'),
            'location': request.data.get('location'),
        }
        serializer = DeviceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScheduleDeviceView(APIView):
    @swagger_auto_schema(tags=["Schedules"], operation_summary="List schedules for a device")
    def get(self, request, device_guid, *args, **kwargs):
        try:
            device = Device.objects.get(GUID=device_guid)
            schedules = Schedule.objects.filter(device=device)
            serializer = ScheduleSerializer(schedules, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return Response({"detail": "Device not found."}, status=status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(tags=["Schedules"], operation_summary="Create a new schedule for a device")
    def post(self, request, device_guid, *args, **kwargs):
        try:
            device = Device.objects.get(GUID=device_guid)
            data = {
                'device': device.id,
                'day_of_week': request.data.get('day_of_week'),
                'time_start': request.data.get('time_start'),
                'time_end': request.data.get('time_end'),
            }
            serializer = ScheduleSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Device.DoesNotExist:
            return Response({"detail": "Device not found."}, status=status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(tags=["Schedules"], operation_summary="List schedules for a device")
    def get(self, request, device_guid, *args, **kwargs):
        try:
            device = Device.objects.get(GUID=device_guid)
            schedules = Schedule.objects.filter(device=device)
            serializer = ScheduleSerializer(schedules, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return Response({"detail": "Device not found."}, status=status.HTTP_404_NOT_FOUND)
        
class ScheduleDetailView(APIView):
    @swagger_auto_schema(tags=["Schedules"], operation_summary="Update a schedule for a device")
    def put(self, request, device_guid, schedule_id, *args, **kwargs):
        try:
            device = Device.objects.get(GUID=device_guid)
            schedule_instance = Schedule.objects.get(id=schedule_id, device=device)
            data = {
                'day_of_week': request.data.get('day_of_week', schedule_instance.day_of_week),
                'time_start': request.data.get('time_start', schedule_instance.time_start),
                'time_end': request.data.get('time_end', schedule_instance.time_end),
            }
            serializer = ScheduleSerializer(instance=schedule_instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Device.DoesNotExist:
            return Response({"detail": "Device not found."}, status=status.HTTP_404_NOT_FOUND)
        except Schedule.DoesNotExist:
            return Response({"detail": "Schedule not found."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(tags=["Schedules"], operation_summary="Delete a schedule for a device")
    def delete(self, request, device_guid, schedule_id, *args, **kwargs):
        try:
            device = Device.objects.get(GUID=device_guid)
            schedule_instance = Schedule.objects.get(id=schedule_id, device=device)
            schedule_instance.delete()
            return Response({"res": "Schedule deleted!"}, status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return Response({"detail": "Device not found."}, status=status.HTTP_404_NOT_FOUND)
        except Schedule.DoesNotExist:
            return Response({"detail": "Schedule not found."}, status=status.HTTP_404_NOT_FOUND)
        
class MoistureView(APIView):
    def get_object(self, device_guid, sensor_id, *args, **kwargs):
        try:
            device = Device.objects.get(GUID=device_guid)
            return Moisture.objects.get(device=device, sensor_number=sensor_id)
        except Moisture.DoesNotExist:
            return None
        except Device.DoesNotExist:
            return None

    def get(self, request, device_guid, sensor_id=None, *args, **kwargs):
        if sensor_id is None:
            return self.get_all_moistures(request, device_guid)
        else:
            return self.get_moisture_by_sensor_id(request, device_guid, sensor_id)
        
    def get_objects(self, device_guid, sensor_id):
        try:
            device = Device.objects.get(GUID=device_guid)
            return Moisture.objects.filter(device=device, sensor_number=sensor_id)
        except Moisture.DoesNotExist:
            return None
        except Device.DoesNotExist:
            return None

    def get_all_moistures(self, request, device_guid):
        try:
            device = Device.objects.get(GUID=device_guid)
            moistures = Moisture.objects.filter(device=device)
            serializer = MoistureSerializer(moistures, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return Response({"detail": "Device not found."}, status=status.HTTP_404_NOT_FOUND)

    def get_moisture_by_sensor_id(self, request, device_guid, sensor_id):
        moisture_instances = self.get_objects(device_guid, sensor_id)
        if not moisture_instances:
            return Response({"detail": "Moisture readings not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MoistureSerializer(moisture_instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, device_guid, *args, **kwargs):
        try:
            device = Device.objects.get(GUID=device_guid)
            data = {
                'device': device.id,
                'sensor_number': request.data.get('sensor_number'),
                'read_value': request.data.get('read_value'),
            }
            serializer = MoistureSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Device.DoesNotExist:
            return Response({"detail": "Device not found."}, status=status.HTTP_404_NOT_FOUND)

class TemperatureView(APIView):
    def get_object(self, device_guid, sensor_id, *args, **kwargs):
        try:
            device = Device.objects.get(GUID=device_guid)
            return Temperature.objects.get(device=device, sensor_number=sensor_id)
        except Temperature.DoesNotExist:
            return None
        except Device.DoesNotExist:
            return None
        
    def get_objects(self, device_guid, sensor_id):
        try:
            device = Device.objects.get(GUID=device_guid)
            return Temperature.objects.filter(device=device, sensor_number=sensor_id)
        except Temperature.DoesNotExist:
            return None
        except Device.DoesNotExist:
            return None

    def get(self, request, device_guid, sensor_id=None, *args, **kwargs):
        if sensor_id is None:
            return self.get_all_temperatures(request, device_guid)
        else:
            return self.get_temperature_by_sensor_id(request, device_guid, sensor_id)

    def get_all_temperatures(self, request, device_guid):
        try:
            device = Device.objects.get(GUID=device_guid)
            temperatures = Temperature.objects.filter(device=device)
            serializer = TemperatureSerializer(temperatures, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return Response({"detail": "Device not found."}, status=status.HTTP_404_NOT_FOUND)

    def get_temperature_by_sensor_id(self, request, device_guid, sensor_id):
        temperature_instances = self.get_objects(device_guid, sensor_id)
        if not temperature_instances:
            return Response({"detail": "Temperature readings not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TemperatureSerializer(temperature_instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, device_guid, *args, **kwargs):
        try:
            device = Device.objects.get(GUID=device_guid)
            data = {
                'device': device.id,
                'sensor_number': request.data.get('sensor_number'),
                'read_value': request.data.get('read_value'),
            }
            serializer = TemperatureSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Device.DoesNotExist:
            return Response({"detail": "Device not found."}, status=status.HTTP_404_NOT_FOUND)