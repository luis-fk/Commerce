# Generated by Django 4.2.6 on 2023-10-29 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_remove_category_artandcollectibles_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='listings',
            field=models.ManyToManyField(blank=True, related_name='categories', to='auctions.listings'),
        ),
    ]
