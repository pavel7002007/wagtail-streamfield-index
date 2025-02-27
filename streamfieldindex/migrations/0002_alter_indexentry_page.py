# Generated by Django 4.1.9 on 2024-02-01 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0083_workflowcontenttype"),
        ("streamfieldindex", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="indexentry",
            name="page",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="block_index", to="wagtailcore.page"
            ),
        ),
    ]
