# Generated by Django 4.0.5 on 2022-07-06 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='description',
            field=models.CharField(default='Tag description.', max_length=255),
        ),
    ]