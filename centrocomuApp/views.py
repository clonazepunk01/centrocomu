from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, DisponibilidadForm, CitaForm, LoginForm
from .models import Usuario, Paciente, Psicologo, CitaPsicologica, Disponibilidad

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            tipo_usuario = form.cleaned_data['tipo_usuario']
            usuario = form.save(commit=False)
            
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()

            # Crear el perfil adicional según el tipo de usuario
            if tipo_usuario == 'psicologo':
                Psicologo.objects.create(usuario=usuario)
            elif tipo_usuario == 'paciente':
                Paciente.objects.create(usuario=usuario)

            messages.success(request, "Usuario registrado exitosamente")
            login(request, usuario)
            if tipo_usuario == 'psicologo':
                return redirect('psicologo_dashboard')
            else:
                return redirect('paciente_dashboard')
    else:
        form = RegistroForm()

    return render(request, 'login.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data['rut']
            password = form.cleaned_data['password']
            try:
                usuario = Usuario.objects.get(rut=rut)
                if check_password(password, usuario.password):
                    login(request, usuario)
                    
                    # Redirigir según el tipo de usuario
                    if usuario.tipo_usuario == 'paciente':
                        return redirect('paciente_dashboard')  # Redirige al dashboard de paciente
                    elif usuario.tipo_usuario == 'psicologo':
                        return redirect('psicologo_dashboard')  # Redirige al dashboard de psicólogo
                    else:
                        messages.error(request, 'Tipo de usuario no reconocido.')
                        return redirect('login')
                else:
                    messages.error(request, 'Contraseña incorrecta')
            except Usuario.DoesNotExist:
                messages.error(request, 'RUT no encontrado')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def cerrar_sesion(request):
    request.session.flush()
    return redirect('login')

@login_required
def psicologo_dashboard(request):
    return render(request, 'psicologo_dashboard.html')

@login_required
def paciente_dashboard(request):
    return render(request, 'paciente_dashboard.html')

@login_required
def agregar_horas(request):
    if request.method == 'POST':
        form = DisponibilidadForm(request.POST)
        if form.is_valid():
            disponibilidad = form.save(commit=False)
            disponibilidad.psicologo = request.user.psicologo
            disponibilidad.save()
            messages.success(request, "Horas disponibles agregadas.")
            return redirect('psicologo_dashboard')
    else:
        form = DisponibilidadForm()
    return render(request, 'agregar_horas.html', {'form': form})

@login_required
def agendar_cita(request):
    form = CitaForm()
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.paciente = request.user.paciente
            cita.save()
            messages.success(request, "Cita agendada.")
            return redirect('paciente_dashboard')
    return render(request, 'agendar_cita.html', {'form': form})

@login_required
def historial_citas(request):
    if request.user.tipo_usuario == 'paciente':
        citas = CitaPsicologica.objects.filter(paciente=request.user.paciente)
    elif request.user.tipo_usuario == 'psicologo':
        citas = CitaPsicologica.objects.filter(psicologo=request.user.psicologo)
    return render(request, 'historial_citas.html', {'citas': citas})
