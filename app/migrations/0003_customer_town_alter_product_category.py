# Generated by Django 5.1.3 on 2024-11-17 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_product_category_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='town',
            field=models.CharField(choices=[('Kisumu', "K'Ogelo"), ('Malindi', 'Tendawema'), ('Nyeri', 'Mathira'), ('Garissa', 'Kainuk'), ('Thika', 'Kiamaiko'), ('Kitale', 'Kajibroa'), ('Eldoret', 'Moiben'), ('Nakuru', 'Njiru'), ('Nairobi', 'Rongai'), ('Mombasa', 'Nyali')], default='Unknown', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('GH', 'Ghee'), ('LS', 'Lassi'), ('IC', 'Ice-Creams'), ('MS', 'Milkshake'), ('ML', 'Milk'), ('CR', 'Curd'), ('CZ', 'Cheese'), ('PN', 'Paneer')], max_length=2),
        ),
    ]