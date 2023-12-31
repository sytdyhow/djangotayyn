# Generated by Django 4.2.6 on 2023-11-20 12:27

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
            name='Hostnames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=150)),
                ('ipaddress', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Logroles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('severity_in', models.CharField(max_length=50)),
                ('application', models.CharField(max_length=100)),
                ('index_number', models.CharField(blank=True, max_length=10, null=True)),
                ('split_character', models.CharField(max_length=10)),
                ('start_message', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('severity_out', models.CharField(max_length=10)),
                ('own_text', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PairsList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Systems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('url', models.CharField(blank=True, max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('active', models.BooleanField(default=True)),
                ('icon', models.CharField(blank=True, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Userperimision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='UsersSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='alertlog.systems')),
                ('users_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UsersRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='alertlog.rule')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mess', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('usersperimission', models.ManyToManyField(to='alertlog.userperimision')),
            ],
        ),
        migrations.CreateModel(
            name='Filterlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=150)),
                ('severity', models.CharField(max_length=50)),
                ('facility', models.CharField(max_length=50)),
                ('application', models.CharField(max_length=70)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('role', models.CharField(max_length=350)),
                ('is_know', models.BooleanField(default=False)),
                ('text_message', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Baglansyk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logroles', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='alertlog.logroles')),
                ('pairname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alertlog.pairslist')),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
