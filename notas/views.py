from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group, Permission, models
from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from notas.forms.formLogin import FormLogin
from notas.forms.formMateria import FormMateria
from notas.forms.formNota import FormNota
from notas.forms.formUsuario import UsersForm
from notas.models import *
from notas.models.materia import Materia
from notas.models.nota import Nota


@login_required(login_url='/login/')
def index(request):
    usuario = User.objects.get(id=request.user.id)
    lista = usuario.groups.all()
    if lista.count() > 0:
        rol = lista.first().id
        if rol == 1:
            lista_materias = Materia.objects.all()
            return render(request, 'administrador/inicio.html', {
                'valor': 'materias',
                'listaMaterias': lista_materias})
        elif rol == 2:
            lista_materias = Materia.objects.filter(docente=request.user.id)
            return render(request, 'docente/inicio.html', {
                'valor': 'materias',
                'listaMaterias': lista_materias})
        elif rol == 3:
            lista_materias_inscritas = Materia.objects.filter(estudiantes__id=request.user.id)
            return render(request, 'estudiante/inicio.html', {
                'valor': 'materias',
                'listaMaterias': lista_materias_inscritas
            })
    else:
        print('es un superadmin')
        return redirect('admin/')


def login(request):
    form = FormLogin()
    return render(request, 'login.html', {'form': form})


@login_required(login_url='/login/')
def logout(request):
    auth_logout(request)
    form = FormLogin()
    return render(request, 'login.html', {'form': form})


def logon(request):
    form = FormLogin()
    user = authenticate(username=request.POST['username'], password=request.POST['password'])

    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'form': form, 'errors': 'Esta cuenta ha sido dado de baja'})
    else:
        return render(request, 'login.html', {'form': form, 'errors': 'El usuario o la contraseña son incorrectos'})


@permission_required('notas.view_materia', login_url='/login/')
def ver_materias(request):
    lista_materias = Materia.objects.all()
    return render(request, 'administrador/inicio.html', {
        'valor': 'materias',
        'listaMaterias': lista_materias})


@permission_required('notas.add_materia', login_url='/login/')
def form_materia(request):
    form = FormMateria()
    if request.method == 'POST':
        formMateria = FormMateria(request.POST)
        if formMateria.is_valid():
            materia_aux = Materia()
            materia_aux.nombre = request.POST['nombre']
            materia_aux.sigla = request.POST['sigla']
            docente = User.objects.get(id=request.POST['docente'])
            materia_aux.docente = docente
            materia_aux.save()
            return redirect('Ver materias')
        else:
            return render(request, 'administrador/formularios/form_materia.html', {
                'form': form
            })

    return render(request, 'administrador/formularios/form_materia.html', {
        'form': form
    })


@permission_required('auth.add_user', login_url='/login/')
def form_docente(request):
    form = UsersForm()
    if request.method == 'POST':
        form_docente = UsersForm(request.POST)
        docente = User()
        docente.username = request.POST['username']
        docente.set_password(request.POST['password'])
        docente.first_name = request.POST['first_name']
        docente.last_name = request.POST['last_name']
        docente.email = request.POST['email']
        form = UsersForm(instance=docente)

        if form_docente.is_valid():
            if(request.POST['password'] == request.POST['confirmPassword']):
                docente.save()
                group = Group.objects.get(id=2)
                docente.groups.add(group)
                return redirect('Ver docentes')
            else:
                return render(request, 'administrador/formularios/form_usuario.html', {
                    'form': form,
                    'type': 'docente'
                })
        else:
            return render(request, 'administrador/formularios/form_usuario.html', {
                'form': form,
                'type': 'docente'
            })

    return render(request, 'administrador/formularios/form_usuario.html', {
        'form': form,
        'type': 'docente'
    })


@permission_required('auth.add_user', login_url='/login/')
def form_estudiante(request):
    form = UsersForm()
    if request.method == 'POST':
        form_estudiante = UsersForm(request.POST)
        estudiante = User()
        estudiante.username = request.POST['username']
        estudiante.set_password(request.POST['password'])
        estudiante.first_name = request.POST['first_name']
        estudiante.last_name = request.POST['last_name']
        estudiante.email = request.POST['email']
        form = UsersForm(instance=estudiante)

        if form_estudiante.is_valid():
            if(request.POST['password'] == request.POST['confirmPassword']):
                estudiante.save()
                group = Group.objects.get(id=3)
                estudiante.groups.add(group)
                return redirect('Ver estudiantes')
            else:
                return render(request, 'administrador/formularios/form_usuario.html', {
                    'form': form,
                    'type': 'estudiante'
                })
        else:
            return render(request, 'administrador/formularios/form_usuario.html', {
                'form': form,
                'type': 'estudiante'
            })

    return render(request, 'administrador/formularios/form_usuario.html', {
        'form': form,
        'type': 'estudiante'
    })


@permission_required('notas.change_materia', login_url='/login/')
def editar_materia(request, id):
    materia = Materia.objects.get(id_materia=id)
    if request.method == 'POST':
        form = FormMateria(data=request.POST, instance=materia)
        if form.is_valid():

            estudiantes = request.POST.getlist('estudiantes')
            materia.nombre = request.POST['nombre']
            materia.sigla = request.POST['sigla']
            docente = User.objects.get(id=request.POST['docente'])
            materia.docente = docente
            materia.save()
            return redirect('Ver materias')
        else:
            form = FormMateria(instance=materia)
            # docente = materia.docente
            # form.fields['docente'].initial = [docente.id_docente]
            return render(request, 'administrador/formularios/form_materia.html', {
                'form': form,
                'errors': 'Rellene todos los datos'
            })
    else:
        form = FormMateria(instance=materia)
        # docente = materia.docente
        # form.fields['docente'].initial = [docente.id_docente]
        return render(request, 'administrador/formularios/form_materia.html', {
            'form': form
        })


@permission_required('auth.change_user', login_url='/login/')
def editar_docente(request, id):
    docente = User.objects.get(id=id)
    if request.method == 'POST':
        form = UsersForm(data=request.POST, instance=docente)
        if form.is_valid():
            docente.first_name = request.POST['first_name']
            docente.last_name = request.POST['last_name']
            docente.email = request.POST['email']
            docente.username = request.POST['username']
            docente.set_password(request.POST['password'])
            docente.save()
            return redirect('Ver docentes')
        else:
            print(form.errors)
            form = UsersForm(instance=docente)
            return (render(request, 'administrador/formularios/form_usuario.html', {
                'form': form,
                'type': 'docente',
                'errors': 'Rellene todos los datos'
            }))

    else:
        form = UsersForm(instance=docente)
        return (render(request, 'administrador/formularios/form_usuario.html', {
            'form': form,
            'type': 'docente'
        }))


@permission_required('auth.change_user', login_url='/login/')
def editar_estudiante(request, id):
    estudiante = User.objects.get(id=id)
    if request.method == 'POST':
        form = UsersForm(data=request.POST, instance=estudiante)
        if form.is_valid():
            estudiante.first_name = request.POST['first_name']
            estudiante.last_name = request.POST['last_name']
            estudiante.email = request.POST['email']
            estudiante.username = request.POST['username']
            estudiante.set_password(request.POST['password'])
            estudiante.save()
            return redirect('Ver estudiantes')
        else:
            form = UsersForm(instance=estudiante)
            return (render(request, 'administrador/formularios/form_usuario.html', {
                'form': form,
                'type': 'estudiante',
                'errors': 'Rellene todos los datos'
            }))
    else:
        form = UsersForm(instance=estudiante)
        return (render(request, 'administrador/formularios/form_usuario.html', {
            'form': form,
            'type': 'estudiante'
        }))


@permission_required('notas.delete_materia', login_url='/login/')
def eliminar_materia(request, id):
    Materia.objects.filter(id_materia=id).delete()
    return redirect('Ver materias')


@permission_required('auth.delete_user', login_url='/login/')
def eliminar_docente(request, id):
    User.objects.filter(id=id).delete()
    return redirect('Ver docentes')


@permission_required('auth.delete_user', login_url='/login/')
def eliminar_estudiante(request, id):
    User.objects.filter(id=id).delete()
    return redirect('Ver estudiantes')


@permission_required('auth.view_user', login_url='/login/')
def ver_docentes(request):
    lista_docentes = User.objects.filter(groups__name='Docentes')
    return render(request, 'administrador/inicio.html', {
        'valor': 'docentes',
        'listaDocentes': lista_docentes})


@permission_required('auth.view_user', login_url='/login/')
def ver_estudiantes(request):
    lista_estudiantes = User.objects.filter(groups__name='Estudiantes')
    return render(request, 'administrador/inicio.html', {
        'valor': 'estudiantes',
        'listaEstudiantes': lista_estudiantes})


@permission_required('auth.view_user', login_url='/login/')
def detalle_estudiante(request, id):
    estudiante = User.objects.get(id=id)
    lista_materias_inscritas = Materia.objects.filter(estudiantes__id=id)
    lista_materias_habilitadas = Materia.objects.exclude(estudiantes__id=id)
    return render(request, 'administrador/detalles/detalle_estudiante.html', {
        'estudiante': estudiante,
        'lista_materias_inscritas': lista_materias_inscritas,
        'lista_materias_habilitadas': lista_materias_habilitadas
    })


@permission_required('auth.view_user', login_url='/login/')
def detalle_docente(request, id):
    docente = User.objects.get(id=id)
    lista_materias_inscritas = Materia.objects.filter(docente=id)
    return render(request, 'administrador/detalles/detalle_docente.html', {
        'estudiante': docente,
        'lista_materias_inscritas': lista_materias_inscritas,
    })


@permission_required('notas.view_materia', login_url='/login/')
def detalle_materia(request, id):
    materia = Materia.objects.get(id_materia=id)
    lista_estudiantes = materia.estudiantes.all()
    return render(request, 'docente/detalles/detalle_materia.html', {
        'materia': materia,
        'lista_estudiantes': lista_estudiantes,
        # 'lista_materias_habilitadas': lista_materias_habilitadas
    })


@permission_required('notas.view_materia', login_url='/login/')
def detalle_materia_admin(request, id):
    materia = Materia.objects.get(id_materia=id)
    lista_estudiantes = materia.estudiantes.all()
    lista_estudiantes_habilitados = User.objects.filter(groups__name='Estudiantes')
    return render(request, 'administrador/detalles/detalle_materia.html', {
        'materia': materia,
        'lista_estudiantes': lista_estudiantes,
        'lista_estudiantes_habilitados': lista_estudiantes_habilitados
    })


@permission_required('notas.add_materia', login_url='/login/')
def agregar_materia_estudiante(request, id):
    estudiante = User.objects.get(id=id)
    materia_agregada = Materia.objects.get(id_materia=request.POST['materia'])
    materia_agregada.estudiantes.add(estudiante)
    nota = Nota()
    nota.fk_alumno = estudiante
    nota.fk_materia = materia_agregada
    nota.save()
    return redirect('Detalle estudiante', id=id)


@permission_required('notas.add_materia', login_url='/login/')
def agregar_estudiante_materia(request, id):
    estudiante = User.objects.get(id=request.POST['estudiante'])
    materia_agregada = Materia.objects.get(id_materia=id)
    materia_agregada.estudiantes.add(estudiante)
    nota = Nota()
    nota.fk_alumno = estudiante
    nota.fk_materia = materia_agregada
    nota.save()
    return redirect('Detalle materia admin', id=id)


@permission_required('notas.delete_materia', login_url='/login/')
def eliminar_materia_estudiante(request, id, id_materia):
    estudiante = User.objects.get(id=id)
    materia_eliminada = Materia.objects.get(id_materia=id_materia)
    materia_eliminada.estudiantes.remove(estudiante)
    nota = Nota.objects.filter(fk_alumno=id, fk_materia=id_materia).first()
    if nota is not None:
        nota.delete()
    return redirect('Detalle estudiante', id=id)


@permission_required('notas.delete_materia', login_url='/login/')
def eliminar_materia_estudiante_from_detalle(request, id, id_materia):
    estudiante = User.objects.get(id=id)
    materia_eliminada = Materia.objects.get(id_materia=id_materia)
    materia_eliminada.estudiantes.remove(estudiante)
    nota = Nota.objects.filter(fk_alumno=id, fk_materia=id_materia).first()
    if nota is not None:
        nota.delete()
    return redirect('Detalle materia admin', id=id_materia)


@permission_required('notas.view_materia', login_url='/login/')
def ver_materias_docente(request):
    lista_materias = Materia.objects.filter(docente=request.user.id)
    form_nota = FormNota()
    return render(request, 'docente/inicio.html', {
        'valor': 'materias',
        'listaMaterias': lista_materias,
        'form_nota': form_nota
    })


@permission_required('notas.view_materia', login_url='/login/')
def ver_materias_estudiante(request):
    lista_materias_inscritas = Materia.objects.filter(estudiantes__id=request.user.id)
    return render(request, 'estudiante/inicio.html', {
        'valor': 'materias',
        'listaMaterias': lista_materias_inscritas,
    })


@permission_required('notas.view_nota', login_url='/login/')
def ver_notas(request):
    estudiante = User.objects.get(id=request.user.id)
    lista_notas = Nota.objects.filter(fk_alumno=estudiante.id)
    return render(request, 'estudiante/inicio.html', {
        'valor': 'notas',
        'listaNotas': lista_notas
    })


@permission_required('notas.view_nota', login_url='/login/')
def ver_notas_docente(request):
    docente = User.objects.get(id=request.user.id)
    lista_materias = Materia.objects.filter(docente=docente.id)
    # lista_materias2 = Materia.objects.filter(docente=request.user.id)
    # lista_notas = Nota.objects.filter(fk_materia=lista_materias.id_materia)
    array = []
    for materia in lista_materias:
        lista_notas = Nota.objects.filter(fk_materia=materia.id_materia)
        for nota in lista_notas:
            array.append(nota)

    return render(request, 'docente/inicio.html', {
        'valor': 'notas',
        'listaNotas': array
    })


@permission_required('notas.add_nota', login_url='/login/')
def estudiante_nota(request, id_materia, id_estudiante):
    nota = Nota.objects.filter(fk_alumno=id_estudiante, fk_materia=id_materia).first()
    materia_nota = Materia.objects.get(id_materia=id_materia)
    estudiante_nota = User.objects.get(id=id_estudiante)
    if nota is None:
        print('la nota no existia')
        nota = Nota()
        estudiante_aux = User.objects.get(id=id_estudiante)
        materia_aux = Materia.objects.get(id_materia=id_materia)
        nota.fk_alumno = estudiante_aux
        nota.fk_materia = materia_aux
        nota.save()

    form = FormNota(instance=nota)
    if request.method == 'POST':
        nota.primer_parcial = request.POST['primer_parcial'] if request.POST['primer_parcial'] != '' else None
        nota.segundo_parcial = request.POST['segundo_parcial'] if request.POST['segundo_parcial'] != '' else None
        nota.controles = request.POST['controles'] if request.POST['controles'] != '' else None
        nota.practicos = request.POST['practicos'] if request.POST['practicos'] != '' else None
        nota.examen_final = request.POST['examen_final'] if request.POST['examen_final'] != '' else None
        nota.save()
        return redirect('Detalle materia', id=id_materia)
    else:
        return render(request, 'docente/detalles/detalle_nota.html', {
            'form': form,
            'materia': materia_nota,
            'estudiante': estudiante_nota,
        })


@permission_required('notas.add_nota', login_url='/login/')
def estudiante_nota_from_table(request, id_materia, id_estudiante):
    nota = Nota.objects.filter(fk_alumno=id_estudiante, fk_materia=id_materia).first()
    materia_nota = Materia.objects.get(id_materia=id_materia)
    estudiante_nota = User.objects.get(id=id_estudiante)
    if nota is None:
        print('la nota no existia')
        nota = Nota()
        estudiante_aux = User.objects.get(id=id_estudiante)
        materia_aux = Materia.objects.get(id_materia=id_materia)
        nota.fk_alumno = estudiante_aux
        nota.fk_materia = materia_aux
        nota.save()

    form = FormNota(instance=nota)
    if request.method == 'POST':
        nota.primer_parcial = request.POST['primer_parcial'] if request.POST['primer_parcial'] != '' else None
        nota.segundo_parcial = request.POST['segundo_parcial'] if request.POST['segundo_parcial'] != '' else None
        nota.controles = request.POST['controles'] if request.POST['controles'] != '' else None
        nota.practicos = request.POST['practicos'] if request.POST['practicos'] != '' else None
        nota.examen_final = request.POST['examen_final'] if request.POST['examen_final'] != '' else None
        nota.save()
        return redirect('Ver notas docente')
    else:
        return render(request, 'docente/detalles/detalle_nota.html', {
            'form': form,
            'materia': materia_nota,
            'estudiante': estudiante_nota,
            'type': 'from_tabla'
        })