# Generated by Django 4.2.4 on 2023-12-05 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_remove_story_is_active_story_viewer_viewers_user'),
        ('users', '0009_remove_userprofile_posts_userprofile_posts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='posts',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='posts',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_posts', to='content.post'),
        ),
    ]
