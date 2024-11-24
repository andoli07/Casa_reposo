from django.contrib import admin
from .models import Residente, Medicamento, AdministracionMedicamento, Personal, Turno

# Register your models here.
admin.site.register(Residente)
admin.site.register(Medicamento)
admin.site.register(AdministracionMedicamento)
admin.site.register(Personal)
admin.site.register(Turno)



