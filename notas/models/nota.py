from django.db import models
from django.contrib.auth.models import User

from notas.models.materia import Materia


class Nota(models.Model):
    id_nota = models.AutoField(primary_key=True)
    primer_parcial = models.IntegerField(null=True)
    segundo_parcial = models.IntegerField(null=True)
    examen_final = models.IntegerField(null=True)
    controles = models.IntegerField(null=True)
    practicos = models.IntegerField(null=True)
    fk_alumno = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Alumno', null=False)
    fk_materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='Materia', null=False)

    class Meta:
        db_table = "notas_notas"

    def __str__(self):
        return 'Materia: ' + self.fk_alumno.username + ' - Alumno: ' + self.fk_materia.nombre
