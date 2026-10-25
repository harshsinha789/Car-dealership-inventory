from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='Vehicle', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('make', models.CharField(max_length=80)), ('model', models.CharField(max_length=100)), ('category', models.CharField(choices=[('sedan','Sedan'),('suv','SUV'),('hatchback','Hatchback'),('coupe','Coupe'),('truck','Truck'),('other','Other')], default='other', max_length=20)), ('price', models.DecimalField(decimal_places=2, max_digits=12)), ('quantity', models.PositiveIntegerField(default=0)), ('created_at', models.DateTimeField(auto_now_add=True)), ('updated_at', models.DateTimeField(auto_now=True))], options={'ordering':['make','model']}),
        migrations.CreateModel(name='Purchase', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('quantity', models.PositiveIntegerField(default=1)), ('purchased_at', models.DateTimeField(auto_now_add=True)), ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)), ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.vehicle'))]),
    ]
