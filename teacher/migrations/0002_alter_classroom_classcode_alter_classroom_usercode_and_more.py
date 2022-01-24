# Generated by Django 4.0.1 on 2022-01-23 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='classCode',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='usercode',
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name='ClassRecordings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usercode', models.CharField(max_length=50)),
                ('date', models.CharField(default=None, max_length=30)),
                ('recordinglink', models.URLField()),
                ('classCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Class_Code', to='teacher.classroom')),
            ],
        ),
        migrations.CreateModel(
            name='ClassNotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usercode', models.CharField(max_length=50)),
                ('date', models.CharField(default=None, max_length=30)),
                ('noteslink', models.URLField()),
                ('classCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ClassCode', to='teacher.classroom')),
            ],
        ),
    ]