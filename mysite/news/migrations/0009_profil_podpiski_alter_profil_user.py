# Generated by Django 4.1 on 2022-12-03 08:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0008_alter_news_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='profil',
            name='podpiski',
            field=models.ManyToManyField(blank=True, related_name='podpiski', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profil',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]