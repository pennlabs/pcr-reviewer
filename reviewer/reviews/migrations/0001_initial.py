# Generated by Django 2.0 on 2017-12-24 01:03

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
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=5)),
                ('section', models.CharField(max_length=15)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Comment')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='reviews.Instructor'),
        ),
    ]
