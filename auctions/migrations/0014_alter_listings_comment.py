# Generated by Django 4.2.6 on 2023-10-29 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_remove_listings_comment_listings_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='comment',
            field=models.ManyToManyField(blank=True, related_name='comment', to='auctions.comment'),
        ),
    ]
