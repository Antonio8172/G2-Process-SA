# Generated by Django 4.1.1 on 2022-09-05 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_usuario', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre_usuario', models.CharField(max_length=50)),
                ('pass_usuario', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'usuario',
                'managed': False,
            },
        ),
    ]