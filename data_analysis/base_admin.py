# coding=utf-8
from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    用来过滤非该用户的数据显示
    """
    exclude = ("owner",)

    def save_model(self, request, obj, form, change):
        obj.person_analysis = request.user
        return super(
            BaseOwnerAdmin,
            self).save_model(
            request,
            obj,
            form,
            change)

    def queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
