from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

from django.db import models

class Residente(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    historial_medico = models.TextField(blank=True, null=True)
    alergias = models.TextField(blank=True, null=True)
    contacto_emergencia = models.CharField(max_length=100)
    telefono_emergencia = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

class Medicamento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    dosis = models.CharField(max_length=50)
    frecuencia = models.CharField(max_length=50)  # Ejemplo: "Cada 8 horas"
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE, related_name='medicamentos')

    def __str__(self):
        return f"{self.nombre} para {self.residente.nombre}"

class AdministracionMedicamento(models.Model):
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE, related_name='administraciones')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, related_name='administraciones')
    fecha_hora = models.DateTimeField(auto_now_add=True)
    responsable = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.medicamento.nombre} administrado a {self.residente.nombre} por {self.responsable}"

class Personal(models.Model):
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=50)  # Ejemplo: "Enfermera", "Auxiliar"
    telefono = models.CharField(max_length=15)
    turno = models.CharField(max_length=50)  # Ejemplo: "Mañana", "Tarde", "Noche"

    def __str__(self):
        return f"{self.nombre} ({self.rol})"

class Turno(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='turnos')

    def clean(self):
        # Validar que la fecha de inicio sea anterior a la fecha de fin
        if self.fecha_inicio >= self.fecha_fin:
            raise ValidationError("La fecha de inicio debe ser anterior a la fecha de fin.")

        # Validar que el turno no se solape con otros turnos del mismo personal
        turnos_solapados = Turno.objects.filter(
            personal=self.personal,
            fecha_fin__gt=self.fecha_inicio,
            fecha_inicio__lt=self.fecha_fin
        ).exclude(id=self.id)

        if turnos_solapados.exists():
            raise ValidationError("Este turno se solapa con otro turno asignado al mismo personal.")

        # Validar que la duración del turno no exceda las 12 horas
        duracion = self.fecha_fin - self.fecha_inicio
        if duracion.total_seconds() > 12 * 60 * 60:
            raise ValidationError("La duración del turno no puede exceder las 12 horas.")

    def save(self, *args, **kwargs):
        self.clean()  # Ejecutar las validaciones antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - {self.personal.nombre}"