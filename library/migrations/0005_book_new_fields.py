from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_signout_expected_return_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='creators',
            field=models.CharField(blank=True, max_length=255, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.CharField(blank=True, max_length=255, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='publish_date',
            field=models.CharField(blank=True, max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='total_copies',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='book',
            name='available_copies',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.RemoveField(
            model_name='book',
            name='available',
        ),
    ]
