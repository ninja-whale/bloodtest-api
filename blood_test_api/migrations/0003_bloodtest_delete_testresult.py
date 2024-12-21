# Generated by Django 5.0.1 on 2024-12-21 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood_test_api', '0002_testresult_delete_bloodtest_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.IntegerField()),
                ('test_name', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unit', models.CharField(max_length=50)),
                ('test_date', models.DateTimeField()),
                ('is_abnormal', models.BooleanField()),
            ],
        ),
        migrations.DeleteModel(
            name='TestResult',
        ),
    ]