from rest_framework import serializers
from .models import Employee, UserType, Logins, ArrivalDeparture
from django.contrib.auth.models import User


class UserDataSerializer(serializers.ModelSerializer):
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


class LoginsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logins
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
            password=password,
            is_active=False,
            email=f"{username}@sample.com",
        )
        credentials.save()
        return credentials
