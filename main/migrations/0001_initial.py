# Generated by Django 2.2 on 2021-07-19 18:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='name')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='boards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Доска',
                'verbose_name_plural': 'Доски',
            },
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='name')),
                ('board', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='main.Board')),
            ],
            options={
                'verbose_name': 'Колонка',
                'verbose_name_plural': 'Колонки',
            },
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='name')),
                ('column', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='main.Column')),
            ],
            options={
                'verbose_name': 'Карточка',
                'verbose_name_plural': 'Корточки',
            },
        ),
    ]
