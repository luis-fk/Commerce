# Generated by Django 4.2.6 on 2023-10-29 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_remove_comment_listing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listings',
            name='comment',
        ),
        migrations.AddField(
            model_name='listings',
            name='comment',
            field=models.ManyToManyField(blank=True, null=True, related_name='comment', to='auctions.comment'),
        ),
    ]
