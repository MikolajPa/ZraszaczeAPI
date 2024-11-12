from rest_framework import serializers
from .models import Todo, Device, Schedule, Moisture, Temperature
from django.core.exceptions import ValidationError

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["task", "completed", "timestamp", "updated", "user"]

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["id", "GUID", "location"]

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ["id", "device", "day_of_week", "time_start", "time_end"]

    def validate(self, attrs):
        # Ensure that time_start is less than time_end
        if attrs['time_start'] >= attrs['time_end']:
            raise serializers.ValidationError("time_start must be less than time_end.")
        return attrs

    def create(self, validated_data):
        # Call clean method of the model for overlap checking
        try:
            return super().create(validated_data)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

    def update(self, instance, validated_data):
        # Call clean method of the model for overlap checking
        try:
            return super().update(instance, validated_data)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

class MoistureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moisture
        fields = ["id", "device", "time", "sensor_number", "read_value"]

class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = ["id", "device", "time", "sensor_number", "read_value"]