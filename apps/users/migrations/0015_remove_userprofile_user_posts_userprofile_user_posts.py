# Generated by Django 4.2.4 on 2023-12-05 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_remove_story_is_active_story_viewer_viewers_user'),
        ('users', '0014_remove_userprofile_user_posts_userprofile_user_posts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_posts',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_posts',
            field=models.ManyToManyField(blank=True, related_name='user_posts', to='content.post'),
        ),
    ]