from django.contrib.auth.models import User
from django.db import models


class Materia(models.Model):
    id_materia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=300)
    sigla = models.CharField(max_length=5)
    estudiantes = models.ManyToManyField(User, related_name='Estudiantes')
    docente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Docente', default=1)

    class Meta:
        db_table = "notas_materias"

    def __str__(self):
        return self.sigla + ' - ' + self.nombre
