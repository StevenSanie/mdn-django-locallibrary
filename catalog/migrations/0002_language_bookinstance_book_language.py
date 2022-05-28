# Generated by Django 4.0.4 on 2022-05-07 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(blank=True, choices=[('eng', 'English'), ('far', 'Farsi')], default='eng', help_text='Select book language', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='bookinstance',
            name='book_language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.language'),
        ),
    ]