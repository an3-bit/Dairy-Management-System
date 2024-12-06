# Generated by Django 5.1.3 on 2024-11-10 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('selling_price', models.FloatField()),
                ('discounted_price', models.FloatField()),
                ('description', models.TextField()),
                ('composition', models.TextField(default='')),
                ('propapp', models.TextField(default='')),
                ('category', models.CharField(choices=[('CR', 'Curd'), ('GH', 'Ghee'), ('CZ', 'Cheese'), ('IC', 'Ice-Creams'), ('PN', 'Paneer'), ('MS', 'Milkshake'), ('LS', 'Lassi'), ('ML', 'Milk')], max_length=2)),
                ('product_image', models.ImageField(upload_to='product')),
            ],
        ),
    ]