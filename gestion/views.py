from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from .models import Residente, Medicamento, AdministracionMedicamento,Personal, Turno
from django.db.models import Sum, ExpressionWrapper, F, DurationField, FloatField
from django.db.models.functions import ExtractSecond, ExtractMinute, ExtractHour
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here
@login_required
def lista_turnos(request):
    turnos = Turno.objects.all()
    return render(request, 'gestion/lista_turnos.html', {'turnos': turnos})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'gestion/dashboard.html')

def lista_residentes(request):
    residentes = Residente.objects.all()
    return render(request, 'gestion/lista_residentes.html', {'residentes': residentes})

def detalle_residente(request, id):
    residente = get_object_or_404(Residente, id=id)
    return render(request, 'gestion/detalle_residente.html', {'residente': residente})

def lista_medicamentos(request):
    medicamentos = Medicamento.objects.all()
    return render(request, 'gestion/lista_medicamentos.html', {'medicamentos': medicamentos})

def detalle_medicamento(request, id):
    medicamento = get_object_or_404(Medicamento, id=id)
    return render(request, 'gestion/detalle_medicamento.html', {'medicamento': medicamento})

def lista_administraciones(request):
    administraciones = AdministracionMedicamento.objects.all()
    return render(request, 'gestion/lista_administraciones.html', {'administraciones': administraciones})

def registrar_administracion(request):
    if request.method == 'POST':
        residente_id = request.POST['residente']
        medicamento_id = request.POST['medicamento']
        responsable = request.POST['responsable']
        observaciones = request.POST.get('observaciones', '')

        AdministracionMedicamento.objects.create(
            residente_id=residente_id,
            medicamento_id=medicamento_id,
            responsable=responsable,
            observaciones=observaciones
        )
        return redirect('lista_administraciones')

    residentes = Residente.objects.all()
    medicamentos = Medicamento.objects.all()
    return render(request, 'gestion/registrar_administracion.html', {'residentes': residentes, 'medicamentos': medicamentos})

#Personal

def lista_personal(request):
    personal = Personal.objects.all()
    return render(request, 'gestion/lista_personal.html', {'personal': personal})

def detalle_personal(request, id):
    persona = get_object_or_404(Personal, id=id)
    return render(request, 'gestion/detalle_personal.html', {'persona': persona})

def registrar_personal(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        rol = request.POST['rol']
        telefono = request.POST['telefono']
        turno = request.POST['turno']

        Personal.objects.create(
            nombre=nombre,
            rol=rol,
            telefono=telefono,
            turno=turno
        )
        return redirect('lista_personal')

    return render(request, 'gestion/registrar_personal.html')

#Turno

def lista_turnos(request):
    turnos = Turno.objects.all()
    return render(request, 'gestion/lista_turnos.html', {'turnos': turnos})

def registrar_turno(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        personal_id = request.POST['personal']

        turno = Turno(
            nombre=nombre,
            descripcion=descripcion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            personal_id=personal_id
        )

        try:
            turno.save()
            return redirect('lista_turnos')
        except ValidationError as e:
            return render(request, 'gestion/registrar_turno.html', {
                'personal': Personal.objects.all(),
                'error': e.messages
            })

    return render(request, 'gestion/registrar_turno.html', {'personal': Personal.objects.all()})

#Reporte

def generar_reporte(request):
    # Filtrar turnos por rango de fechas si se proporcionan
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    if fecha_inicio and fecha_fin:
        turnos = Turno.objects.filter(
            fecha_inicio__gte=fecha_inicio,
            fecha_fin__lte=fecha_fin
        )
    else:
        turnos = Turno.objects.all()

    # Calcular duración en segundos y convertir a horas
    turnos = turnos.annotate(
        duracion_horas=ExpressionWrapper(
            (ExtractHour(F('fecha_fin')) - ExtractHour(F('fecha_inicio'))) +
            (ExtractMinute(F('fecha_fin')) - ExtractMinute(F('fecha_inicio'))) / 60 +
            (ExtractSecond(F('fecha_fin')) - ExtractSecond(F('fecha_inicio'))) / 3600,
            output_field=FloatField()
        )
    )

    # Calcular horas trabajadas por cada empleado
    reporte_horas = turnos.values('personal__nombre').annotate(
        total_horas=Sum('duracion_horas')
    )

    # Preparar datos para el reporte
    reporte = {
        'turnos': turnos,
        'reporte_horas': reporte_horas,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }

    return render(request, 'gestion/reporte.html', reporte)

#login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirigir al dashboard
        else:
            messages.error(request, 'Credenciales incorrectas. Inténtalo de nuevo.')

    return render(request, 'gestion/login.html')