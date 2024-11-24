from django.urls import path
from . import views

urlpatterns = [
    path('residentes/', views.lista_residentes, name='lista_residentes'),
    path('residentes/<int:id>/', views.detalle_residente, name='detalle_residente'),
    path('medicamentos/', views.lista_medicamentos, name='lista_medicamentos'),
    path('medicamentos/<int:id>/', views.detalle_medicamento, name='detalle_medicamento'),
    path('administraciones/', views.lista_administraciones, name='lista_administraciones'),
    path('administraciones/registrar/', views.registrar_administracion, name='registrar_administracion'),
     path('personal/', views.lista_personal, name='lista_personal'),
    path('personal/<int:id>/', views.detalle_personal, name='detalle_personal'),
    path('personal/registrar/', views.registrar_personal, name='registrar_personal'),
    path('turnos/', views.lista_turnos, name='lista_turnos'),
    path('turnos/registrar/', views.registrar_turno, name='registrar_turno'),
    path('reporte/', views.generar_reporte, name='generar_reporte'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
