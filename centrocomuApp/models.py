from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# Administrador personalizado para el modelo Usuario
class UsuarioManager(BaseUserManager):
    def create_user(self, rut, email, password=None, **extra_fields):
        if not rut:
            raise ValueError("El campo RUT es obligatorio")
        if not email:
            raise ValueError("El campo Email es obligatorio")
        
        email = self.normalize_email(email)
        user = self.model(rut=rut, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, rut, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(rut, email, password, **extra_fields)

# Modelo de Usuario General
class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=50)
    rut = models.CharField(max_length=10, unique=True)
    calle = models.CharField(max_length=50, null=True, blank=True)
    numero = models.IntegerField(null=True, blank=True)
    fono = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True)
    tipo_usuario = models.CharField(
        max_length=10,
        choices=[('paciente', 'Paciente'), ('psicologo', 'Psicologo')]
    )

    # Campos adicionales requeridos por AbstractBaseUser y PermissionsMixin
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UsuarioManager()

    USERNAME_FIELD = 'rut'
    REQUIRED_FIELDS = ['email', 'nombre', 'apellido']

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.tipo_usuario})"

# Modelo Psicologo con relación uno-a-uno a Usuario
class Psicologo(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Psicólogo/a {self.usuario.nombre} {self.usuario.apellido}"

# Modelo Paciente con relación uno-a-uno a Usuario
class Paciente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Paciente {self.usuario.nombre} {self.usuario.apellido}"

# Modelo Disponibilidad que referencia a Psicologo
class Disponibilidad(models.Model):
    psicologo = models.ForeignKey(Psicologo, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"Disponibilidad el {self.fecha} de {self.hora_inicio} a {self.hora_fin} - {self.psicologo.usuario.nombre} {self.psicologo.usuario.apellido}"

# Modelo CitaPsicologica que referencia a Paciente y Psicologo
class CitaPsicologica(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    psicologo = models.ForeignKey(Psicologo, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField(null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('Pendiente', 'Pendiente'),
            ('Confirmada', 'Confirmada'),
            ('Cancelada', 'Cancelada'),
            ('Completada', 'Completada'),
        ],
        default='Pendiente'
    )

    def __str__(self):
        return f"Cita de {self.paciente.usuario.nombre} con {self.psicologo.usuario.nombre} el {self.fecha} a las {self.hora} - {self.estado}"
