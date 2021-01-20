#!/usr/bin/env python 
'''
这个脚本的功能是将数据储存在model的数据库中
'''
import datetime
import os,sys
import django


sys.path.insert(0,"../")
os.environ.setdefault('DJANGO_SETTINGS_MODULE','data_analysis.settings')
django.setup()


#from data_record.models import Project,History
#保存数据到project中
def save_data_project(path_n,file_n):
    os.chdir(path_n)
    from data_record.models import Project
    project_model=Project.objects
    with open(file_n,"r") as content:
        all_lines=content.readlines()
        for line_n in all_lines:
            if line_n.strip("\r\n"):
                #print(line_n,line_n.split("\t"))
                project_name,leader,release_date,info_n=line_n.strip("\r\n").split("\t")
                #格式化时间数据
                release_date=datetime.datetime(int(release_date.split(",")[0]),int(release_date.split(",")[1]),int(release_date.split(",")[2]))
                #利用create命令来创建数据
                project_model.create(project_name=project_name,leader=leader,release_date=release_date,info_n=info_n)


path_n=r"/home/fanxuezhe/files/test_files/model_data"
file_n="model_data"
save_data_project(path_n,file_n)

