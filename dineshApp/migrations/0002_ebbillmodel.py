# Generated by Django 3.1 on 2020-08-28 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dineshApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EBBillModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house', models.CharField(max_length=30)),
                ('date', models.DateField()),
                ('eb_no', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('yes_no', models.CharField(max_length=20)),
            ],
        ),
    ]
