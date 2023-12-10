# Generated by Django 4.2.4 on 2023-12-06 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_remove_story_is_active_story_viewer_viewers_user'),
        ('users', '0021_userprofile_user_reels'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user_highlight',
            field=models.ManyToManyField(blank=True, null=True, related_name='users_highlights', to='content.highlight'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_stories',
            field=models.ManyToManyField(blank=True, null=True, related_name='users_stories', to='content.story'),
        ),
    ]