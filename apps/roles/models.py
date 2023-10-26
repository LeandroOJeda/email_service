from django.db import models


class Role(models.Model):
    id = models.AutoField(primary_key=True, db_column="rol_id")
    name = models.CharField(max_length=50, db_column="rol_nombre")
    level_of_access = models.IntegerField(blank=True, null=True, db_column="rol_nivel_acceso")

    class Meta:
        db_table = "roles"
