from django.db import models
from django.contrib.auth.models import User


class ArrivalDeparture(models.Model):
    record_id = models.BigAutoField(primary_key=True)
    record_date = models.DateTimeField()
    action_type = models.CharField(
        max_length=10, choices=[("arrival", "Arrival"), ("departure", "Departure")]
    )
    employee = models.ForeignKey("Employee", on_delete=models.DO_NOTHING)
    description = models.TextField(default="", null=False)
    is_approved = models.BooleanField()

    class Meta:
        managed = False
        db_table = "arrival_departure"


class Employee(models.Model):
    id = models.BigAutoField(primary_key=True)
    national_id = models.CharField(unique=True, max_length=10)
    employee_type = models.ForeignKey("UserType", models.DO_NOTHING)
    access_date_limit = models.DateTimeField()
    employee_role = models.CharField(max_length=20)
    phone = models.CharField(max_length=13, blank=True, null=True)
    contract_type = models.CharField(max_length=9)
    user = models.OneToOneField(User, models.DO_NOTHING)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = "employee"


class LoginLogout(models.Model):
    record_id = models.BigAutoField(primary_key=True)
    record_date = models.DateTimeField()
    record_type = models.CharField(max_length=6)
    user = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "login_logout"


class UserType(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = "user_type"
