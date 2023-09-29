# Generated by Django 4.2.5 on 2023-09-29 06:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_remove_book_genre_book_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='unique_id',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, unique=True, verbose_name='unique ID'),
        ),
    ]
