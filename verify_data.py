import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'centroComunitario.settings')
django.setup()

from centrocomuApp.models import Usuario  # Reemplaza con el nombre de tu modelo

def verify_data():
    records = Usuario.objects.all()  # Consulta todos los registros
    print(f"Total de registros en YourModel: {records.count()}")
    for record in records:
        print(record)  # Muestra cada registro

if __name__ == "__main__":
    verify_data()
