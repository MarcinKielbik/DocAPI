from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Użytkownik (Pacjent lub Lekarz)
class User(AbstractUser):
    ROLE_CHOICES = (
        ('Patient', 'Pacjent'),
        ('Doctor', 'Lekarz'),
        ('Admin', 'Administrator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Dodaj nową nazwę dla related_name
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Dodaj nową nazwę dla related_name
        blank=True
    )
# Model dla lekarza
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"

# Model dla rezerwacji wizyty
class Appointment(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Oczekująca'),
        ('Confirmed', 'Potwierdzona'),
        ('Cancelled', 'Anulowana'),
    )

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Wizyta: {self.appointment_date} z Dr. {self.doctor.user.last_name}"

# Model dla grafiku lekarzy
class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    available_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"Grafik: {self.available_date} od {self.start_time} do {self.end_time}"
