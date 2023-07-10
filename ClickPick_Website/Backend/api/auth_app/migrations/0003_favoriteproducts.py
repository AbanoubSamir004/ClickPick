# Generated by Django 4.1.9 on 2023-06-28 04:35

import bson.objectid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0002_rename_custid_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteProducts',
            fields=[
                ('id', djongo.models.fields.ObjectIdField(auto_created=True, default=bson.objectid.ObjectId, editable=False, primary_key=True, serialize=False)),
                ('product_ids', models.JSONField(verbose_name=models.CharField(max_length=100))),
                ('user_unique_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'favorite_products',
            },
        ),
    ]