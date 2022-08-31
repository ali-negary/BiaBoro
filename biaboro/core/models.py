from django.db import models
from datetime import datetime, timedelta


class ArrivalDeparture(models.Model):
    record_id = models.BigAutoField(primary_key=True)
    record_date = models.DateTimeField(default=datetime.now())
    type = models.CharField(
        max_length=10, choices=[("arrival", "Arrival"), ("departure", "Departure")]
    )
    user_id = models.ForeignKey(to="UserData", on_delete=models.DO_NOTHING)
    description = models.TextField(default="", null=False)

    class Meta:
        managed = False
        db_table = "arrival_departure"


class Credentials(models.Model):
    id = models.BigIntegerField(primary_key=True)
    password = models.CharField(max_length=16)
    active = models.BooleanField()
    user = models.ForeignKey(to="UserData", on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "credentials"


class Logins(models.Model):
    record_id = models.BigAutoField(primary_key=True)
    login_datetime = models.DateField()
    user_id = models.ForeignKey(to="UserData", on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "logins"


class UserData(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=15)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=35)
    national_id_number = models.CharField(max_length=10)
    sign_up_date = models.DateTimeField(default=datetime.now())
    user_type = models.ForeignKey(to="UserType", on_delete=models.DO_NOTHING)
    access_date_limit = models.DateTimeField(
        default=(datetime.now() + timedelta(days=10))
    )
    user_role = models.CharField(max_length=30)
    phone = models.CharField(max_length=13, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "user_data"


class UserType(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = "user_type"
