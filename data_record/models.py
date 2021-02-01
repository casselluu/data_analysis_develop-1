from django.db import models
import datetime
from django.utils import timezone
#from account.models import MyUser
from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.models import User
# coding=utf-8
# 定义分析的路径历史，历史包括几个内容（文件夹名称，项目名称，分析日期，分析人）
# 定义一个数据库来储存所有的用户的用户名和密码


class MyUser(AbstractUser):
    name = models.CharField("姓名", max_length=50, default="匿名用户")
    department1 = models.CharField("一级部门", max_length=50, default="发现部")
    department2 = models.CharField("二级部门", max_length=50, default="药物工程部")
    department3 = models.CharField("三级部门", max_length=50, default="优化设计部")
    # 确定每一个人可以进行的数据分析对应的序列号（一对多），一个序列号可以对应多个人
    # serialnum=models.ForeignKey(SerialNum,on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"
        permissions = (("del_history", "can delete history"),)

# Create your models here.
# 定义项目的列表，包括以下内容（项目名称，项目负责人，项目立项时间）


class Project(models.Model):
    # 项目名称（也就是类似于051601这样的项目编号）
    project_name = models.CharField(max_length=20, verbose_name="项目名称")
    # leader=models.ForeignKey(MyUser,on_delete=models.CASCADE,verbose_name="项目负责人")
    release_date = models.DateTimeField(blank=True, verbose_name="开始日期")
    # 相关的信息
    info = models.TextField(
        max_length=2000,
        default="暂时无相关信息",
        verbose_name="相关信息")

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = verbose_name_plural = "项目"
        ordering = ["project_name"]

# 定义项目负责人，每个项目可以有多个项目负责人


class Leader(models.Model):
    # 定义项目负责人对应的username(一对一)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    # 定义项目负责人对应的项目(一对多)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "项目负责人"
        verbose_name_plural = "项目负责人"


# 定义分析编号，每一个分析编号相当于找新序列时所使用的用来找历史序列的编号，每一个项目负责人可以有多个
class SerialNum(models.Model):
    name = models.CharField(max_length=100, verbose_name="分析编号")
    info = models.CharField(max_length=100, verbose_name="描述信息")
    # 定义这个项目可以由哪个项目负责人控制(多对多)，一个项目负责人可以控制多个分析编号，一个序列编号也可以由多个项目负责人控制
    leader = models.ManyToManyField(Leader, verbose_name="分析编号相关leader")
    user = models.ManyToManyField(MyUser, verbose_name="分析编号相关分析人")

    def get_all_leaders(self):
        return "\n".join(
            [leader_n.user.username for leader_n in self.leader.all()])

    def get_all_users(self):
        return "\n".join([user_n.username for user_n in self.user.all()])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "分析编号"
        verbose_name_plural = "分析编号"

# 定义分析的路径历史，历史包括几个内容（文件夹名称，项目名称，分析日期，分析人）


class History(models.Model):
    # 定义分析的文件夹名称
    folder = models.CharField(max_length=300, verbose_name="文件夹名称")
    # 定义分析的路径
    path = models.CharField(max_length=500, verbose_name="数据路径")
    # 定义分析的项目，CASCADE表示级联删除。这样当主表中的数据删除之后副表中的数据也会被删除
    # project_name=models.CharField(max_length=20,default="000000")
    serialnum = models.ForeignKey(
        SerialNum,
        on_delete=models.CASCADE,
        verbose_name="项目名称")
    # 定义分析的时间
    pubDate = models.DateTimeField(verbose_name="数据分析时间")
    # 定义分析的人
    person = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        verbose_name="分析人")

    def __str__(self):
        return self.folder

    class Meta:
        verbose_name = verbose_name_plural = "历史数据"
        ordering = ["pubDate"]

# 新建一个模型，这个模型是一个多对一的数据库，用来储存每一次分析的新出现的序列


class Unique(models.Model):
    # 定义序列的名称
    seqName = models.CharField(max_length=300, verbose_name="序列名称")
    # 定义序列
    sequence = models.CharField(max_length=300, verbose_name="序列内容")
    # 序列的长度
    lengthAllCdr = models.IntegerField(default=0, verbose_name="序列长度")
    lengthCdr3 = models.IntegerField(default=0, verbose_name="CDR3长度")
    # 定义外键（外键对应于历史）
    history = models.ForeignKey(
        History,
        on_delete=models.CASCADE,
        verbose_name="历史")

    def __str__(self):
        return self.seqName

    class Meta:
        # 这里定义的verbose_name,verbose_name_plural指的是单数和复数的形式,这些内容将会在管理界面显示。
        # 假如只是定义了verbose_name那么复数的形式会直接加上s，就如下形式定义为一个就可以了。
        verbose_name = verbose_name_plural = "新序列"

    def analysis_date(self):
        return self.history.pubDate
    # analysis_date.admin_order_field="history"
