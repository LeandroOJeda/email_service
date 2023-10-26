from datetime import datetime
from os import getenv
from rest_framework.exceptions import ValidationError

from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from apps.roles.serializers import RoleSerializer
import logging
from .models import Person


logger = logging.getLogger()

class BriefPersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = "__all__"


class WithRelationsPersonSerializer(serializers.ModelSerializer):

    role = RoleSerializer

    class Meta:
        model = Person
        exclude = ["password", "is_active"]


class CreateUpdatePersonSerializer(serializers.ModelSerializer):
    password = serializers.CharField(default="r2dc41t3c")


    class Meta:
        model = Person
        fields = "__all__"

    def create(self, validated_data):

        person: Person = Person.objects.create_user(**validated_data)
        person.id, default_token_generator.make_token(person)
        logger.info("New user created : %s", person.username)
        return person

    def update(self, instance: Person, validated_data: dict):
        fields = instance._meta.fields
        exclude = ["password"]
        for field in fields:
            field = field.name.split(".")[-1]
            if field in exclude:
                continue
            setattr(
                instance, field, validated_data.get(field, getattr(instance, field))
            )

        instance.save()
        return instance
    
class ChangePasswordPersonSerializer(serializers.Serializer):
    password_old = serializers.CharField(required=True)
    password_new = serializers.CharField(required=True)

    def validate_password_old(self, value):
        usr = self.context["request"].user
        if not usr.check_password(value):
            raise serializers.ValidationError("Wrong password")
        return value

    def validate(self, data):
        if data["password_new"] == data["password_old"]:
            raise serializers.ValidationError("New password must not be the same")
        return data


class PersonRolesSerializer(RoleSerializer):
    role = serializers.IntegerField

    class Meta:
        model = Person
        fields = ["role"]
