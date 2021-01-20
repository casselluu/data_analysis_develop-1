#coding=utf-8

from django.contrib.admin import AdminSite

class Custom_Site(AdminSite):
    site_header="舒泰神测序数据分析系统"
    site_title="数据分析系统管理后台"
    index_title="首页"
    
custom_site=Custom_Site(name="cus_admin")

