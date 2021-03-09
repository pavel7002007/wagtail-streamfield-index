# Generated by Django 3.1.7 on 2021-03-09 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0060_fix_workflow_unique_constraint'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block_name', models.CharField(max_length=255)),
                ('block_type', models.IntegerField(choices=[(0, 'Other'), (1, 'Struct'), (2, 'Stream')])),
                ('block_value', models.TextField(blank=True)),
                ('block_path', models.TextField()),
                ('field_name', models.CharField(max_length=255)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.page')),
            ],
            options={
                'verbose_name_plural': 'Index Entries',
            },
        ),
    ]
