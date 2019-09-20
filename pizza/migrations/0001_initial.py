# Generated by Django 2.2.5 on 2019-09-19 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('delivery_status', models.CharField(choices=[('not_started', 'not_started'), ('out_for_delivery', 'out_for_delivery'), ('delivered', 'delivered')], default='not_started', max_length=50)),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('address_line_1', models.CharField(blank=True, max_length=250)),
                ('address_line_2', models.CharField(blank=True, max_length=250)),
                ('postal_code', models.CharField(blank=True, max_length=5)),
                ('city', models.CharField(blank=True, max_length=250)),
                ('country', models.CharField(blank=True, max_length=250)),
                ('phone_number', models.CharField(max_length=25)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('flavor', models.CharField(choices=[('salami', 'salami'), ('cheese', 'cheese'), ('margarita', 'margarita'), ('vegan', 'vegan'), ('vegetables', 'vegetables'), ('macaroni', 'macaroni')], max_length=50)),
                ('size', models.CharField(choices=[('small', 'small'), ('medium', 'medium'), ('large', 'large')], max_length=50)),
                ('count', models.PositiveIntegerField(default=0)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pizza', to='pizza.Order')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
