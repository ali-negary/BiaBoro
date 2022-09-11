from rest_framework import serializers
from .models import Employee, UserType, LoginLogout, ArrivalDeparture
from django.contrib.auth.models import User


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = "__all__"


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class LoginLogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginLogout
        fields = "__all__"


class ArrivalDepartureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArrivalDeparture
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    password_2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = ["username", "password", "password_2"]
        extra_kwargs = {
            "password": {"write_only": True},
            "password_2": {"write_only": True},
        }

    def save(self):
        # overwrite the default save method to approve password match.
        username = self.validated_data["username"]
        password = self.validated_data["password"]
        password_2 = self.validated_data["password_2"]

        if password != password_2:
            raise serializers.ValidationError({"password": "Passwords must match."})

        credentials = User(
            username=username,
            is_active=False,
            is_staff=True,
            email=f"{username}@sample.com",
        )
        credentials.set_password(password)

        credentials.save()
        return credentials
