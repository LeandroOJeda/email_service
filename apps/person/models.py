from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.roles.models import Role
from datetime import date

class Person(AbstractUser):
    id = models.AutoField(primary_key=True, db_column="persona_id")
    first_name = models.CharField(max_length=100, db_column="persona_nombre")
    last_name = models.CharField(max_length=100, db_column="persona_apellido")
    username = models.CharField(unique=True, max_length=50, db_column="persona_correo")
    dni = models.CharField(max_length=20, db_column="persona_dni")
    date_birth = models.DateField(blank=True, null=True, db_column="persona_nacimiento")
    password = models.CharField(max_length=32, blank=True, db_column="persona_pass")
    role = models.ForeignKey(Role, models.DO_NOTHING, default=1, db_column="persona_rol")
    daily_messages = models.IntegerField(default=0)
    last_message_date = models.DateField(default=date.today)

    class Meta:
        db_table = "personas"

