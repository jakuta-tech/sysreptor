# Generated by Django 5.2.1 on 2025-06-04 10:44

import django.db.models.deletion
import sysreptor.utils.crypto.fields
import sysreptor.utils.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pentests', '0063_alter_pentestproject_project_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectExcalidrawData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=sysreptor.utils.models.now, editable=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('elements', sysreptor.utils.crypto.fields.EncryptedField(base_field=models.JSONField(default=list), editable=True)),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pentests.pentestproject')),
            ],
            options={
                'ordering': ['-created'],
                'abstract': False,
            },
        ),
    ]
