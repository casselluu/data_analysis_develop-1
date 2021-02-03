import time

from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, Http404, FileResponse, HttpResponseRedirect
from django.template import loader
import datetime
from data_record.form import ContactForms, RangeForm
# Create your views here.
from .models import History, Project, Unique, SerialNum
import os
import re
import pandas as pd
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
# from multi_tools.hmmer_parser import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.contrib.auth.models import User
from .models import MyUser


# 定义一个登陆的界面


def log_in(request):
    if request:
        request.session.set_test_cookie()
        return render(request, "data_record/login.html", {"error": ""})


@login_required
def logoutRequest(request):
    logout(request)
    return HttpResponseRedirect("/")


# 定义一个function，该function的功能是指定数据分析的界面


def data_analysis(request):
    render(request, "data_record/data_analysis.html", )


# 展示历史数据


def display(request):
    historys = History.objects.order_by("folder_name")
    history_values = historys.values()
    char_list = []
    [[char_list.append("\t".join([key_n, str(value_n)]))
      for key_n, value_n in dict_n.items()] for dict_n in history_values]
    return render(request,
                  "data_record/show_record.html",
                  {"display_data": char_list})


# 定义登陆之后的索引界面


@login_required
def index(request):
    # 根据当前用户的权限决定显示的内容
    user_n = request.user
    print("uuuuuuuuuuuuu", user_n)
    if user_n.has_perm("user.del_history"):
        del_his = True
    else:
        del_his = False
    print("dddddddddddddddd", del_his)
    return render(request, "base.html", locals())


@login_required
def del_his(request):
    user = request.user
    if request.method == "post":
        # 获取到需要删除的history的ID
        id_to_rm = request.POST.get("ID")
        print("iiiiiiiiiiiiiiiiiii", id_to_rm)
        if History.objects.get(id=id_to_rm):
            History.objects.get(id_to_rm).delete()
            print("ddddddddddddeeeeelllllllleeeetttttteeeeedddd")
    all_history = History.objects.filter(person=user)
    return render(request, "data_record/del_history.html", locals())


@login_required
# 定义一个homepage的视图,这里显示的是本人的所有的抗体的序列
def cdr_info(request, page, order_type):
    #
    username = request.user.username
    rangeForm = RangeForm()
    if request.method == "GET":
        # 获取数据库中所有的数据
        all_cdr_data = Unique.objects.filter(
            history__person__username=username).order_by(order_type)
        paginator = Paginator(all_cdr_data, 20)
        try:
            pageinfo = paginator.page(page)
        except PageNotAnInteger:
            pageinfo = paginator.page(1)
        except EmptyPage:
            pageinfo = paginator.page(1)
        return render(request, "CDR_info.html", locals())
    elif request.method == "POST":
        # 提取排序的类型
        range_n = RangeForm(data=request.POST)
        print("rrrrrrrrrrrrrrrr", range_n)
        if range_n.is_valid():
            type_n = range_n.cleaned_data["rangeInfo"]
            print("ttttttttttttttttttttttttttt", type_n)
        else:
            error_msg = range_n.errors.as_json()
            print(error_msg)
        # 获取数据库中所有的数据
        all_cdr_data = Unique.objects.filter(
            history__person__username=username).order_by(type_n)

        paginator = Paginator(all_cdr_data, 20)
        order_type = type_n
        try:
            pageinfo = paginator.page(page)
        except PageNotAnInteger:
            pageinfo = paginator.page(1)
        except EmptyPage:
            pageinfo = paginator.page(1)
        return render(request, "CDR_info.html", locals())


def contact(request):
    if request.method == "POST":
        form = ContactForms(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # send_email(cd["subject"],cd["message"],cd.get["email","noreply@example.com"],["siteowner@example.com"])
            # return HttpResponseRedirect("search-form/")
            return HttpResponse("another website")
    else:
        form = ContactForms(initial={"subject": "I love your site!"})
    return render(request, "data_record/contact_form.html", {"form": form})


# 定义一个下载数据的view


@login_required
def download_data(request):
    # 假如method是POST，那么根据POST中给出的id提取数据
    username = request.user.username
    if request.method == "POST":
        if True:
            try:
                analysis_id = request.POST.get("idN")
                his_n = History.objects.get(id=analysis_id)
            except BaseException:
                return HttpResponse("sorry the data not in the database")
            else:
                path_n = his_n.path
                folder_n = his_n.folder
                # 确认含有result.tar.gz的文件夹
                result_path = os.sep.join(path_n.split(os.sep)[:-1])
                os.chdir(result_path)
                result_tar = "%s_result.tar.gz" % (folder_n.split(".zip")[0])
                if not os.path.exists(os.path.join(result_path, result_tar)):
                    os.system(
                        "tar -czvf %s %s" %
                        (result_tar, folder_n.split(".zip")[0]))
                result_file = os.path.join(result_path, result_tar)
                # result_file=os.path.join(result_path,"all_result.tar.gz")
                file_result = open(result_file, "rb")
                response = FileResponse(file_result)
                response["Content-Type"] = "application/octet-stream"
                response["Content-Disposition"] = 'attachment;filename="%s"' % result_tar
                return response
    # 假如method是GET那么就把所有的数据都提取出来，展示在界面上
    else:
        all_history = History.objects.filter(
            person=MyUser.objects.get(
                username=username)).order_by("-pubDate")

        return render(request,
                      "data_record/download_data.html",
                      {"all_data": all_history})


# 读取分析结果
def Creat_analysis_result(path):
    info_dict = {'name': '文件名字', 'time': '文件提交时间', 'seqn': '接受序列数量', 'rseq': 3, 'wseq': '错误序列数',
                 'rate': '正确率', 'dmn': '设计突变位点数', 'mn': '正确突变位点数', 'umn': '未突变位点数'}
    list1 = []
    list2 = []
    list3 = []
    files = []
    for root, dir, file in os.walk(path):
        files = file

    os.path.join(root, files[0])
    mtime = os.stat(os.path.join(root, files[0])).st_mtime
    info_dict['name'] = files[0].split('_')[0] + '_' + files[0].split('_')[1]
    info_dict['time'] = time.strftime('%Y-%m-%d', time.localtime(mtime))
    data1 = pd.read_csv(path + files[0], sep='\t', header=None, names=['id', 'num'])
    info_dict['seqn'] = data1.num[:-1].sum(axis=0)
    info_dict['wseq'] = data1.num.iloc[-2]
    info_dict['rseq'] = data1.num[:-2].sum(axis=0)
    info_dict['rate'] = info_dict['rseq']/info_dict['seqn']
    for i in range(len(data1) - 1):
        list1.append((data1.id[i], data1.num[i]))
    data2 = pd.read_csv(path + files[1], sep='\t').append(pd.read_csv(path + files[2], sep='\t'), ignore_index=True)
    data2.columns = ['CDR', 'position', 'wt', 'Mutations', 'Frequency']
    info_dict['dmn'] = len(data2)
    umn = 0
    for i in range(info_dict['dmn'] - 1):
        list2.append((data2.CDR[i], 'NNK', data2.wt[i], data2.Mutations[i], data2.Frequency[i]))
        if data2.wt[i] == data2.Mutations[i]:
            umn += 1
    info_dict['umn'] = umn
    info_dict['mn'] = len(data2) - umn
    data3 = pd.read_csv(path + files[3], sep='\t')
    for i in range(len(data3) - 1):
        if len(data3.Mutations[i].split('/')) >= 5:
            list3.append((data3.ID[i], data3.Mutations[i], 1))
        else:
            list3.append((data3.ID[i], data3.Mutations[i], 0))
    return info_dict, list1, list2, list3


@login_required
# 读取分析结果
def AnalysisResult(request):
    info_dict, table1, table2, table3 = Creat_analysis_result('C:/Users/Casselluu/Desktop/code/Python/data_analysis_develop-1/result/')
    page = "data_record/AnalysisResult.html"
    username = request.user.username
    return render(request, page, {'result': info_dict, 'list1': table1, 'list2': table2,'list3': table3})


def time_add(request, num_n):
    # num_n=100
    time_now = datetime.datetime.now()
    try:
        int_num = int(num_n)
    except BaseException:
        raise Http404
    else:
        time_add = time_now + datetime.timedelta(hours=int_num)
        html = '<html><body> this is time %s </body></html>' % time_add
        return HttpResponse(html)


# 新建一个小程序用来新建文件夹，假如这个文件夹已经存在那么就添加new字符然后重新创建
class new_path:
    def __init__(self, path_n, char_n):
        self.path = path_n
        self.char = char_n

    def __next__(self):
        path_n = self.path
        char_n = self.char
        # if os.path.exists(os.path.join(path_n,char_n))
        path_check = os.path.join(path_n, char_n)
        self.char = char_n + "_new"
        return (os.path.exists(path_check), path_check)

    def __iter__(self):
        return self


def mk_new_dir(path_n, char_n):
    new_dirs = new_path(path_n, char_n)
    for status_n, path_x in new_dirs:
        if not status_n:
            os.mkdir(path_x)
            return path_x


# 定义该function用来记录异常序列的数量
def record_abnormal(
        path_n,
        abnormal_file,
        scfv_files,
        common_files,
        unique_files):
    os.chdir(path_n)
    abnormal_file_num = 0
    print(
        "cheeeeeeeeeeeeeeeeeeeeeee",
        abnormal_file,
        scfv_files,
        common_files,
        unique_files)
    if os.path.exists(abnormal_file):
        with open(abnormal_file, "r") as content:
            all_lines = content.readlines()
            for line_n in all_lines:
                if line_n.startswith(">"):
                    name_n = line_n.split("abnormal_FR4")[0].strip("\r\n>\t")
                    print(
                        "nnnnnnnnnnnnnnnnnnn",
                        name_n,
                        "xxxx",
                        scfv_files,
                        common_files,
                        unique_files,
                        common_files.count(name_n),
                        type(name_n))
                    if (scfv_files + common_files).count(name_n) > 0:
                        abnormal_file_num += 2
                    # for scfv_n in scfv_files+common_files:
                    # if scfv_n.find(name_n)!=-1:
                    #    abnormal_file_num+=2
                    #    print("222222222222222222222222222222",scfv_n)

                    if unique_files.count(name_n) > 0:
                        abnormal_file_num += 1
                    # for unique_n in unique_files:
                    #    if unique_n.find(name_n)!=-1:
                    #        abnormal_file_num+=1
                    #        print("1111111111111111111111",unique_n)
    return abnormal_file_num


# 定义该function用来对给定的fasta文件计算其中所有的序列的数量
def get_fasta_num(path_n, fasta_n):
    os.chdir(path_n)
    seq_count = 0
    # print("ppppppppppppppaaaaaaaaaa",path_n,fasta_n)
    with open(fasta_n, "r") as content:
        all_lines = content.readlines()
        for line_n in all_lines:
            if line_n.startswith(">"):
                seq_count += 1
                # print("ccccccccccccooooooooooouuuuuuuuuuunnnnnnn",line_n,seq_count)
                # print(path_n,fasta_n)
    return seq_count


# 定义该function是用来对原始数据文件夹中的seq进行计数,scfv_char指的是标志SCFV的字符，fab_char表示轻链和重链的标志字符，是一个列表，列表的内容是元组，元组有两个字符串，第一个字符是vl的标志字符，第二个字符为vh的标志字符
def count_seq(path_n, scfv_char, fab_chars):
    os.chdir(path_n)
    seq_num = 0
    all_files = os.listdir(path_n)
    scfv_file = []
    vl_files = {}
    vh_files = {}
    for file_n in all_files:
        # scfv序列算两条序列，fab序列算是一条序列
        # print("fffffffffffffffffffffff",file_n)
        if file_n.endswith(".seq"):
            # scfv_file=[]
            # 检查有无scfv的字符
            if re.search(scfv_char, file_n, re.I):
                scfv_file.append(file_n.split(".seq")[0])
            else:
                # vh_files={}
                # vl_files={}
                for vl_char, vh_char in fab_chars:
                    match_vl = re.search(vl_char, file_n, re.I)
                    match_vh = re.search(vh_char, file_n, re.I)

                    if match_vl:
                        file_name = file_n[:match_vl.start()]
                        vl_files[file_name] = file_n
                        # print("lllllllllllllllllllllllllllllllllll",file_name)
                    elif match_vh:
                        file_name = file_n[:match_vh.start()]
                        vh_files[file_name] = file_n
    # 提取scfv，fab中vh/vl同时出现和只出现一个的id
    scfv_ids = scfv_file
    common_ids = list(set(vh_files.keys()) & set(vl_files.keys()))
    unique_ids = list(set(vh_files.keys()) - set(vl_files.keys())) + \
        list(set(vl_files.keys()) - set(vh_files.keys()))
    # print("cccccccccccccccccccccccccc",common_ids,unique_ids)
    return scfv_ids, common_ids, unique_ids


# 定义该function用来检查分析完的结果中的序列数量（正常序列和异常序列总和）是否和原始序列的数量是否一致,给定的路径是文件解压后seq文件所在的路径
def check_num(path_n, scfv_char, fab_chars):
    # 利用路径信息提取文件夹的名字和所在路径的信息
    path_origin, folder_name = os.path.split(path_n)
    result_path = os.path.join(path_origin, "result", folder_name)
    # 首先获取原始数据的数量
    # print("sssccccccccfffvvvvvvvvcccccccccchhhhhhhhharrrrrrrrrrrr",scfv_char,fab_chars)
    scfv_files, common_ids, unique_ids = count_seq(
        path_n, scfv_char, fab_chars)
    # print("iiiiiiiiiiiidddddddddddddddssssssssss",scfv_files,common_ids,unique_ids)
    # 将SCFV看做两条序列，这样就可以从最后得到的轻重链的氨基酸序列和异常序列来对比
    total_seqs = len(scfv_files) * 2 + len(common_ids) * 2 + len(unique_ids)
    # 获取正常序列的轻链和重链序列的总数
    # 正常序列所在路径以及轻链和重链序列的文件名称以及其中的序列的数量
    path_aa = os.path.join(result_path, "AA_sequences")
    vl_fasta = folder_name + "_sequences_VH.fasta"
    vh_fasta = folder_name + "_sequences_VL.fasta"
    # print("pppppppppppppppppppppp",path_aa)
    vl_num = get_fasta_num(path_aa, vl_fasta)
    vh_num = get_fasta_num(path_aa, vh_fasta)
    # 计算异常的序列的数量
    path_abnormal = os.path.join(result_path, "abnormal_seq")
    abnormal_fasta = folder_name + "_abnormal.fasta"
    abnormal_num = record_abnormal(
        path_abnormal,
        abnormal_fasta,
        scfv_files,
        common_ids,
        unique_ids)
    # print("TTTTTTTTTTTTTTTTTTTTTTTTTT",total_seqs,abnormal_num,vh_num,vl_num)
    assert total_seqs == (abnormal_num + vh_num + vl_num)


# 定义修改密码的函数
@login_required
def chagepasswd(request):
    if request.method == "GET":
        username = request.user.username
        return render(request, "data_record/chagepasswd.html", locals())
    elif request.method == "POST":
        username = request.user.username
        origin_password = request.POST.get("origin_passwd")
        new_password = request.POST.get("new_passwd")
        # 检查原密码是否正常
        # print(username,origin_password)
        user = authenticate(username=username, password=origin_password)
        # print("uuuuuuuuuuu",user)
        if user:
            # 修改密码
            user.set_password(new_password)
            user.save()
            error_info = "密码修改成功！"
            return HttpResponseRedirect("/")
        else:
            error_info = "密码输入错误,请重新输入!"
            return render(request, "data_record/chagepasswd.html", locals())


@login_required
def upload(request):
    if request.method == "POST":
        # 检查所有的历史文件夹，用来进行新序列的提取
        # print("cccccccccccccccccccccchhhhhhhhhhhhhhhhhhhheeeeeeeeeeeckkkkkkkkkkk")
        # 假如会利用到多个项目，那么在输入时可以考虑以分号符为分隔，对多个项目进行对比
        serial_name = request.POST["serial_name"]
        scfv_char = request.POST.get("scfv_char")
        # print("sssssssssscccccccffffffffvvvvvvvvvv111111111111111",scfv_char)
        if not scfv_char:
            scfv_char = "scfv"
        fab_h = request.POST.get("fab_h")
        fab_l = request.POST.get("fab_l")
        check_list = request.POST.getlist("construct_or_not")

        if True:
            serialNum_all = SerialNum.objects.all()
            serial_n = serialNum_all.get(name=serial_name)
            # 获取给定的项目对应的路径
            all_cores_history = serial_n.history_set.all()
            path_olds = []
            for hist_n in all_cores_history:
                path_olds.append(hist_n.path)
            # print(path_olds)
        # except:
        #  return HttpResponse("please check,the given project name is invalid")
        # 获取当前的分析人和分析的日期，根据这个来创建文件夹储存文件
        username = request.user.username
        # 定义文件储存的目录(根据当前的日期自行新建)
        # 获取当前的日期
        date_today = datetime.datetime.today().strftime("%Y_%m_%d")
        # dir_store=r"/home/fanxuezhe/files/test_files/django_download"
        dir_store = r"/home/fanxuezhe/files/data_analysis"
        # 为每一个分析人都新建一个单独的分析路径
        dir_store = os.path.join(dir_store, username)
        if not os.path.exists(dir_store):
            os.mkdir(dir_store)
        # target_dir=os.path.join(dir_store,date_today)

        target_dir = mk_new_dir(dir_store, date_today)
        # print("tttttttttttttttttttttt",target_dir)
        # 获取post中的文件
        myFile = request.FILES.get("myfile")
        # project_name=request.POST["project_name"]
        person_analysis = MyUser.objects.get(username=username)
        # print("xxxxxxxxxxxxxxxxxx",target_dir,myFile.name,project_name,person_analysis)
        if myFile:
            # return HttpResponse(myFile.name)
            # print("yyyyyyyyyyyyyyyyyyyy",myFile.name)
            copied_file = os.path.join(target_dir, myFile.name)
            with open(copied_file, "wb") as f:
                for content_n in myFile.chunks():
                    f.write(content_n)

            # 接下来解压文件并且进行分析,target_dir是指解压后的文件夹所在的路径
            os.chdir(target_dir)
            all_files = os.listdir(target_dir)
            # 解压上传的文件
            os.system("unzip %s >>log_file" % myFile.name)
            # 首先检查解压之后有没有文件在里面，假如没有文件，那么就返回一个界面
            all_files = os.listdir(
                os.path.join(
                    target_dir,
                    myFile.name.split(".zip")[0]))
            seq_num = 0
            for file_n in all_files:
                if file_n.endswith(".seq"):
                    seq_num += 1
            if seq_num == 0:
                return HttpResponse("上传的zip文件不含有seq文件")
            # print("sssssssssssccccccccccccffffffffffffvvvvvvvv2222222222222",scfv_char)
            # 这里暂时不进行序列的分析
            if not (
                    scfv_char.strip("\r\n")) and not (
                    fab_h.strip()) and not (
                    fab_l.strip()):
                # os.system("multi_tools FGS .")
                pass
            elif (scfv_char.strip("\r\n")) and not (fab_h.strip()) and not (fab_l.strip()):
                # os.system("multi_tools FGS . --scfv %s" %scfv_char)
                pass
            elif (scfv_char.strip("\r\n")) and (fab_h.strip()) and (fab_l.strip()):
                # os.system("multi_tools FGS . --scfv %s -d  %s %s"%(scfv_char,fab_l.strip(),fab_h.strip()))
                pass
            # os.chdir(os.path.join(target_dir,myFile.name.strip(".zip")))
            os.chdir(target_dir)
            # 检查分析完的序列和原始的序列数量是否对应
            seq_path = os.path.join(target_dir, myFile.name.strip(".zip"))
            # scfv_char="scfv"
            # 假如没有给定fab的H/L的字符，则用默认的字符
            if not (fab_l and fab_h):
                fab_chars = [("T7", "T2A"), ("PFAB", "T2A"), ("YD", "CH1"), ("p2a-R",
                                                                             "p2a-F"), ("3X-F", "3X-R"), ("SeqSE", "SeqSR"), ("SeqSE", "RB-R84")]
            else:
                fab_chars = [(fab_l, fab_h)]
            # check_num(seq_path,scfv_char,fab_chars)
            # 定义分析结果所在的路径
            target_result_path = os.path.join(
                target_dir, "result", myFile.name.split(".zip")[0])
            # 接下来进行查找新序列的操作
            # 首先获取当前分析的结果所在的文件夹
            # 从history的model中获取该项目的分析历史路径
            # 运行命令查找新的序列
            # print("ppppppppppppppppppppppp",path_olds)
            # if path_olds:
            #    get_new_excel(path_olds,target_result_path,True)
            # else:
            #    os.chdir(target_result_path)
            #    os.system("combined_seq_cdr_FGS")
            # 判断是否需要进行是否构建的状态分析
            # print("cccccccccccccccccccccccccccccccc",check_list)
            # if check_list:
            #    os.chdir(target_result_path)
            #    if not path_olds:
            #
            #        os.system("touch empty_file")
            #        os.system("get_new_cdr_dna_info -o empty_file")
            #        print("ssssssssssttttttttttttaaaaaaaaaaaarrrrrrrrrrttttttttttttgermline")
            #        os.system("get_germline_info_excel.py")
            #    else:
            #        print("ooooooooorrrrrrrrrrriiiiiiiiiggggggggggiiiiiiiiiinnnnn")
            #        get_all_construct_cdr(target_result_path,path_olds)
            #        os.chdir(target_result_path)
            #        os.system("get_new_cdr_dna_info -o origin_cdr")
            #        print("sssssssssstttttttttttttttaaaaaaaaaaaaaarrrrrrrrrtttttggggggggggermline")
            #        os.system("get_germline_info_excel.py")

            # 将所有的结果进行压缩
            # os.chdir(os.path.join(target_dir,"result"))
            # os.system("tar -czvf %s_result.tar.gz %s"%(myFile.name.split(".zip")[0],myFile.name.split(".zip")[0]))

            # os.system("compress_result .")

            # 数据分析完之后将数据储存在数据库中
            # his_obj=History.objects
            # serial_obj=SerialNum.objects
            # 外键的话需要是该数据的实例
            # serial_n=serial_obj.get(name=serial_name)
            # print("zzzzzzzzzzzzzzzzzzz",dir(project_name))
            # 分析新的序列

            # his_obj.create(folder=myFile.name,path=target_result_path,serialnum=serial_n,pubDate=datetime.datetime.today(),person=person_analysis)
            # 将新序列储存在数据库中
            # os.chdir(target_result_path)
            # other_freq_file=myFile.name.split(".zip")[0]+"_CDR_info_unique.txt"
            # first_freq_file=myFile.name.split(".zip")[0]+"_CDR_info.txt"
            # unique_obj=Unique.objects
            # if os.path.exists(other_freq_file):
            #    unique_file=other_freq_file
            # elif os.path.exists(first_freq_file):
            #    unique_file=first_freq_file
            # else:
            #    return HttpResponse("analysis not success")
            # with open(unique_file,"r") as content:
            #    all_lines=content.readlines()[1:-1]
            #    #total_number=all_lines[-1].strip("\r\n")
            #    if len(all_lines)>0:
            #        for line_n in all_lines:
            #            id_n,folder_n,aa_n,dna_n,repeats=line_n.strip("\r\n").split("\t")
            #            #将每一个序列都存入进去,CDR长度减5是因为中间有五个空格需要减去
            #            unique_obj.create(seqName=id_n,sequence=aa_n,lengthAllCdr=len(aa_n)-5,lengthCdr3=len(aa_n.split(" ")[-1]),history=his_obj.get(path=target_result_path))

            # 接下来将数据分析之后的结果保存在url中方便下载，另外自动将分析的相关信息储存在数据库
            # file_response=FileResponse(result_file)
            # file_response["content_type"]="application/octet_stream"
            # file_response["Content-Disposition"]='attachment;file=result_file'
            # return HttpResponse("all over")
            # return HttpResponse("您好，数据分析完成！请下载！")

            url = reverse("data_record:download")
            return HttpResponseRedirect(url)

        else:
            # url=reverse("data_record:download")
            # return HttpResponseRedirect(url)
            return HttpResponse("请确认文件是否正常")
        # 假如method不是post
    else:
        # 假如目前要提交数据，那么这里可以显示目前分析人当前所可以进行分析的序列号
        serialnum_all = SerialNum.objects.filter(
            user__username=request.user.username)
        print("xxxxxxxxxxxxxxxxxxx", serialnum_all, len(serialnum_all))
        # print(projects_all)
        # projects_all=["a","n"]
        return render(request, "upload.html", locals())


def search_form(request):
    if request.GET:
        if "q" in request.GET and request.GET["q"]:
            # message="ok,%s is found"%request.GET["q"]
            try:
                project = Project.objects.filter(project_name=request.GET["q"])
                message = project.project_name
            except BaseException:
                message = "sorry,nnnnnnn not found"
            return HttpResponse(message)
        else:
            return render(request,
                          "data_record/search_form.html",
                          {"Search": "This is another search",
                           "warnings": "can not find or input in empty please check"})
    return render(request, "data_record/search_form.html",
                  {"Search": "This is search", "warnings": "the origin"})


def search(request):
    if "q" in request.GET and request.GET["q"]:
        # message="ok,%s is found"%request.GET["q"]
        try:
            project = Project.objects.filter(project_name=request.GET["q"])
            message = project.project_name
        except BaseException:
            message = "sorry,nnnnnnn not found"
        return HttpResponse(message)
    else:
        return render(request,
                      "data_record/search_form.html",
                      {"Search": "This is another search",
                       "warnings": "can not find or input in empty please check"})


def detail(request, History_id):
    analysis = get_object_or_404(History, pk=History_id)
    return render(request, "data_record/detail.html", {"History": analysis})


# def detail(request,History_id):
#    return HttpResponse("hello you are checking detail of %s"%History_id)

# def detail(request,History_id):
#    try:
#        analysis=History.objects.get(pk=History_id)
#    except History.DoesNotExist:
#        raise Http404("There is no id called %d"%History_id)
#    return render(request,"data_record/detail.html",{"History":analysis})
# return HttpResponse("hello you are checking detail of %s"%History_id)


def result(request, History_id):
    return HttpResponse("hello you are checking result of %s" % History_id)


def vote(request, History_id):
    return HttpResponse("hello you are checking vote of %s" % History_id)
