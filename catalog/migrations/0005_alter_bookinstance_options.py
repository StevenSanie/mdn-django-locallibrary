# Generated by Django 4.0.4 on 2022-05-18 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_remove_book_borrower_bookinstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Set book as returned'),)},
        ),
    ]
