# Generated by Django 3.0.1 on 2021-01-20 06:42

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(default='匿名用户', max_length=50, verbose_name='姓名')),
                ('department1', models.CharField(default='发现部', max_length=50, verbose_name='一级部门')),
                ('department2', models.CharField(default='药物工程部', max_length=50, verbose_name='二级部门')),
                ('department3', models.CharField(default='优化设计部', max_length=50, verbose_name='三级部门')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'permissions': (('del_history', 'can delete history'),),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folder', models.CharField(max_length=300, verbose_name='文件夹名称')),
                ('path', models.CharField(max_length=500, verbose_name='数据路径')),
                ('pubDate', models.DateTimeField(verbose_name='数据分析时间')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='分析人')),
            ],
            options={
                'verbose_name': '历史数据',
                'verbose_name_plural': '历史数据',
                'ordering': ['pubDate'],
            },
        ),
        migrations.CreateModel(
            name='Leader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '项目负责人',
                'verbose_name_plural': '项目负责人',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=20, verbose_name='项目名称')),
                ('release_date', models.DateTimeField(blank=True, verbose_name='开始日期')),
                ('info', models.TextField(default='暂时无相关信息', max_length=2000, verbose_name='相关信息')),
            ],
            options={
                'verbose_name': '项目',
                'verbose_name_plural': '项目',
                'ordering': ['project_name'],
            },
        ),
        migrations.CreateModel(
            name='Unique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seqName', models.CharField(max_length=300, verbose_name='序列名称')),
                ('sequence', models.CharField(max_length=300, verbose_name='序列内容')),
                ('lengthAllCdr', models.IntegerField(default=0, verbose_name='序列长度')),
                ('lengthCdr3', models.IntegerField(default=0, verbose_name='CDR3长度')),
                ('history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_record.History', verbose_name='历史')),
            ],
            options={
                'verbose_name': '新序列',
                'verbose_name_plural': '新序列',
            },
        ),
        migrations.CreateModel(
            name='SerialNum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='分析编号')),
                ('info', models.CharField(max_length=100, verbose_name='描述信息')),
                ('leader', models.ManyToManyField(to='data_record.Leader', verbose_name='分析编号相关leader')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='分析编号相关分析人')),
            ],
            options={
                'verbose_name': '分析编号',
                'verbose_name_plural': '分析编号',
            },
        ),
        migrations.AddField(
            model_name='leader',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_record.Project'),
        ),
        migrations.AddField(
            model_name='leader',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='history',
            name='serialnum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_record.SerialNum', verbose_name='项目名称'),
        ),
    ]
