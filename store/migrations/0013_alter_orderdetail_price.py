# Generated by Django 4.1 on 2022-08-29 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_remove_orderdetail_order_orderdetail_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='price',
            field=models.IntegerField(),
        ),
    ]
