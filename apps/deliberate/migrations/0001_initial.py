# Generated by Django 3.0.5 on 2020-09-04 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='deliberate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(verbose_name='关联用户id')),
                ('type', models.TextField(verbose_name='问题')),
                ('create_time', models.DateField(verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '日省·问题',
                'verbose_name_plural': '日省·问题',
                'db_table': 'deliberate',
            },
        ),
        migrations.CreateModel(
            name='dlbr_answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(verbose_name='关联用户id')),
                ('ans', models.TextField(verbose_name='回答内容')),
                ('ans_time', models.DateField(verbose_name='回答日期')),
                ('dlbr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dlbr_answer', to='deliberate.deliberate')),
            ],
            options={
                'verbose_name': '日省·回答',
                'verbose_name_plural': '日省·回答',
                'db_table': 'dlbr_answer',
            },
        ),
    ]
