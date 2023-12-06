# Generated by Django 4.2.4 on 2023-12-05 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_remove_story_is_active_story_viewer_viewers_user'),
        ('users', '0015_remove_userprofile_user_posts_userprofile_user_posts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_posts',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_posts',
            field=models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.CASCADE, related_name='user_posts', to='content.post'),
            preserve_default=False,
        ),
    ]
