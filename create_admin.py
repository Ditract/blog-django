# create_admin.py
import os
import django
from django.contrib.auth.models import User

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

username = "admin"
email = "hgsanez12@gmail.com"
password = "Ditract890?"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superusuario creado correctamente.")
else:
    print("El superusuario ya existe.")
