# Generated by Django 2.2 on 2019-04-14 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_auto_20180411_0219'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='comment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='reviews.Comment'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='flag',
            field=models.CharField(choices=[('A', 'Approved'), ('M', 'Not Useful'), ('I', 'Inappropriate')], default=None, max_length=1, null=True),
        ),
        migrations.DeleteModel(
            name='CommentRating',
        ),
    ]
