from django.urls import path
from notas import views


urlpatterns = [
    path('', views.index, name='Index'),
    path('login/', views.login, name='Login'),
    path('logout/', views.logout, name='Logout'),
    path('logon/', views.logon, name='Logon'),

    path('form_materia/', views.form_materia, name='Form Materia'),
    path('ver_materias/', views.ver_materias, name='Ver materias'),
    path('detalle_materia/<int:id>', views.detalle_materia, name='Detalle materia'),
    path('detalle_materia_admin/<int:id>', views.detalle_materia_admin, name='Detalle materia admin'),
    path('editar_materia/<int:id>/', views.editar_materia, name='Editar Materia'),
    path('eliminar_materia/<int:id>/', views.eliminar_materia, name='Eliminar Materia'),

    path('form_docente/', views.form_docente, name='Form Docente'),
    path('ver_docentes/', views.ver_docentes, name='Ver docentes'),
    path('detalle_docente/<int:id>', views.detalle_docente, name='Detalle docente'),
    path('editar_docente/<int:id>/', views.editar_docente, name='Editar Docente'),
    path('eliminar_docente/<int:id>/', views.eliminar_docente, name='Eliminar Docente'),

    path('form_estudiante/', views.form_estudiante, name='Form Estudiante'),
    path('ver_estudiantes/', views.ver_estudiantes, name='Ver estudiantes'),
    path('detalle_estudiante/<int:id>', views.detalle_estudiante, name='Detalle estudiante'),
    path('editar_estudiante/<int:id>/', views.editar_estudiante, name='Editar Estudiante'),
    path('eliminar_estudiante/<int:id>/', views.eliminar_estudiante, name='Eliminar Estudiante'),

    path('agregar_materia_estudiante/<int:id>', views.agregar_materia_estudiante, name='Agregar materia estudiante'),
    path('agregar_estudiante_materia/<int:id>', views.agregar_estudiante_materia, name='Agregar estudiante materia'),
    path('eliminar_materia_estudiante/<int:id>/<int:id_materia>/', views.eliminar_materia_estudiante, name='Eliminar materia estudiante'),
    path('eliminar_materia_estudiante_from_detalle/<int:id>/<int:id_materia>/', views.eliminar_materia_estudiante_from_detalle, name='Eliminar materia estudiante from detalle'),

    path('ver_materias_docente/', views.ver_materias_docente, name='Ver materias docente'),
    path('ver_materias_estudiante/', views.ver_materias_estudiante, name='Ver materias estudiante'),
    path('estudiante_nota/<int:id_materia>/<int:id_estudiante>', views.estudiante_nota, name='Estudiante nota'),
    path('estudiante_nota_from_table/<int:id_materia>/<int:id_estudiante>', views.estudiante_nota_from_table, name='Estudiante nota from table'),
    path('ver_notas/', views.ver_notas, name='Ver notas'),
    path('ver_notas_docente', views.ver_notas_docente, name='Ver notas docente')
]
