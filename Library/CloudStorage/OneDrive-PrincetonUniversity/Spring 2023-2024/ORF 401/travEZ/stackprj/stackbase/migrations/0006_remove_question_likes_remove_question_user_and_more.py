# Generated by Django 4.2.11 on 2024-04-22 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("stackbase", "0005_auto_20211011_2351"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="question",
            name="likes",
        ),
        migrations.RemoveField(
            model_name="question",
            name="user",
        ),
        migrations.DeleteModel(
            name="Comment",
        ),
        migrations.DeleteModel(
            name="Question",
        ),
    ]