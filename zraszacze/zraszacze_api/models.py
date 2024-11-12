from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Todo(models.Model):
    task = models.CharField(max_length=180)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    completed = models.BooleanField(default=False, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.task
    

class Device(models.Model):
    id = models.AutoField(primary_key=True)
    GUID = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.GUID
    
class Schedule(models.Model):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    DAYS_OF_WEEK = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    ]

    id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    time_start = models.TimeField()
    time_end = models.TimeField()

    def __str__(self):
        return f"{self.device.GUID} - {self.get_day_of_week_display()} {self.time_start} - {self.time_end}"

    def get_day_of_week_display(self):
        """Returns the human-readable name of the day of the week."""
        return dict(self.DAYS_OF_WEEK).get(self.day_of_week, 'Unknown Day')

    def clean(self):
        overlapping_schedules = Schedule.objects.filter(
            device=self.device,
            day_of_week=self.day_of_week,
            time_start__lt=self.time_end,
            time_end__gt=self.time_start
        )

        if overlapping_schedules.exists():
            raise ValidationError("This schedule overlaps with an existing schedule.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Call clean() to validate before saving
        super().save(*args, **kwargs)

class Moisture(models.Model):
    id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    sensor_number = models.IntegerField()
    read_value = models.FloatField()

    def __str__(self):
        return f"Device: {self.device.GUID}, Time: {self.time}, Sensor: {self.sensor_number}, Moisture: {self.read_value}"


class Temperature(models.Model):
    id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    sensor_number = models.IntegerField()
    read_value = models.FloatField()

    def __str__(self):
        return f"Device: {self.device.GUID}, Time: {self.time}, Sensor: {self.sensor_number}, Temperature: {self.read_value}"