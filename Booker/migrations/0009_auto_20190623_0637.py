# Generated by Django 2.1.7 on 2019-06-23 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Booker', '0008_sheets_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sheets',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]