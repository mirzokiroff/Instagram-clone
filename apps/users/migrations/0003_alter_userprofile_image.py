# Generated by Django 4.2.4 on 2023-11-28 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_userprofile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.FileField(default='https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg', upload_to='profile/'),
        ),
    ]
