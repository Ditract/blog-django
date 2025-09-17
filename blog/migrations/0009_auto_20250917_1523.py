from django.db import migrations

def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    username = "admin"
    email = "hgsanez12@gmail.com"
    password = "Ditract890?"

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print("Superusuario creado correctamente.")

def delete_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.filter(username='admin').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0008_alter_profile_avatar'),  # Última migración
    ]

    operations = [
        migrations.RunPython(create_superuser, reverse_code=delete_superuser),
    ]