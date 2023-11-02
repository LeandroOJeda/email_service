from django.db import models
from apps.person.models import Person


class Message(models.Model):
    id = models.AutoField(primary_key=True, db_column="mensaje_id")
    subject = models.CharField(max_length=200, blank=True, db_column="mensaje_asunto")
    body = models.TextField(blank=True, null=False, db_column="mensaje_texto")
    from_email = models.CharField(max_length=100, null=False, db_column="mensaje_remitente")
    to_email = models.CharField(max_length=100, null=False, db_column="mensaje_destinatario")
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=False, db_column="mensaje_persona")


    class Meta:
        db_table = "mensajes"
