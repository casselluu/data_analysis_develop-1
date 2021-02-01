from django.contrib import admin
from .models import History, Project, Unique, Leader, SerialNum, MyUser
from data_analysis.base_admin import BaseOwnerAdmin
from django.utils.html import format_html
from data_analysis.custom_site import custom_site
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin
# Register your models here.

# 这里在register的时候利用site参数直接就决定了将在在那个网址上显示
# 具体的参数在/root/anaconda3/envs/python_3.7_test/lib/python3.7/site-packages/django/contrib/admin/sites.py这里可以设置


@admin.register(Project, site=custom_site)
# class ProjectAdmin(admin.ModelAdmin):
class ProjectAdmin(BaseOwnerAdmin):
    # 这里决定了查看数据时显示的内容,这些双引号中的字符都是模型中的变量名称
    list_display = ("project_name", "release_date", "info")
    # search_fields=("project_name")
    date_hierarchy = "release_date"
    fields = ("project_name", "release_date", "info")
    # raw_id_fields=("project_name",)
# 注册MyUser


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = ("username", "name", "department1", "department2")


# 注册Unique
@admin.register(Unique, site=custom_site)
class UniqueAdmin(BaseOwnerAdmin):
    list_display = ("seqName", "sequence", "lengthAllCdr", "lengthCdr3",)
    list_per_page = 20
    list_filter = ["history__serialnum", "history"]
    search_fields = ["sequence"]

# 注册SerialNum


@admin.register(SerialNum, site=custom_site)
class SerialNumAdmin(BaseOwnerAdmin):
    list_display = ("name", "info", "get_all_leaders", "get_all_users")
    list_per_page = 20

# 注册Leader


@admin.register(Leader, site=custom_site)
class LeaderAdmin(BaseOwnerAdmin):
    list_display = ("user", "project")
    list_per_page = 20


# 注册History
@admin.register(History, site=custom_site)
# class HistoryAdmin(admin.ModelAdmin):
class HistoryAdmin(BaseOwnerAdmin):
    list_display = ("person", "serialnum", "folder", "path", "pubDate")
    raw_id_fields = ("serialnum",)
    search_field = ("serialnum",)
    # 一个括号内的数据表示添加数据时在一列
    # fields=(("project_name","folder_name"),"path_n")
    # 利用field_sets来对界面进行优化，括号中的内容表示在统一行，顺序也就是fields_set中给定的顺序,这些信息是在添加添加信息的时候显示的。
    fieldsets = (
        ("分析人信息", {
            "description": "这里显示的是分析人的相关信息", "fields": (
                "person",)}), ("数据相关信息", {
                    "description": "这里显示的是分析结果相关的信息", "fields": (
                        ("folder", "path"))}), ("项目相关信息", {
                            "description": "这里显示的是项目相关的信息", "fields": (
                                ("serialnum"),)}))
    search_fields = ["serialnum", ]
    # 设置侧边栏过滤器
    list_filter = ["serialnum", "person"]

    # 定义数据展示界面
    actions_on_top = True
    actions_on_bottom = True
    # 这里设置的是保存数据的选项的位置
    save_on_top = True
    # 重写BaseOwnerAdmin中的operator（也就是操作）

    def operator(self, obj):
        # return format_html('<a
        # href="{}">编辑</a>',reverse("admin:",args=(0bj,id)))
        return format_html(
            '<a href="{}">编辑</a>',
            reverse(
                "cus_admin:History",
                args=(
                    obj.id)))
    operator.short_description = "操作11"

    # 这里定义的是新增数据的时候显示的内容，假如不设置的话那么所有的选项都将会出现


# 增加日志文件的记录
@admin.register(LogEntry, site=custom_site)
# class LogEntryAdmin(admin.ModelAdmin):
class LogEntryAdmin(BaseOwnerAdmin):
    list_display = [
        "object_repr",
        "object_id",
        "action_flag",
        "user",
        "change_message"]

    # fields=("person_analysis",)
# admin.site.register(History,HistoryAdmin)
# admin.site.register(Project)
# admin.site.register(Project,ProjectAdmin)
