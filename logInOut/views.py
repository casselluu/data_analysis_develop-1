from django.shortcuts import render,redirect
#from .models import MyUser
#from django.contrib.auth.models import User as MyUser
from data_record.models import MyUser
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import  login_required
# Create your views here.
@login_required
#进行用户注册
def register_origin(request):
    title="仓库系统注册"
    pageTile="用户注册"
    confirmPassword=True
    button="注册"
    urlText="用户登录"
    urlName="userLogin"
    #假如是post
    if request.method=="POST":
        u=request.POST.get("username","")
        p=request.POST.get("password","")
        cp=request.POST.get("cp","")
        #检查用户是不是已经存在
        if MyUser.objects.filter(username=u):
            tips="用户已存在"
        elif cp!=p:
            tips="两次密码输入的不一致"
        else:
            d={
                "username":u,"password":p,
                "is_superuser":0,"is_staff":1
            }
            user=MyUser.objects.create(**d)
            user.save()
            tips="注册成功，请登录"
            logout(request)
            return redirect(reverse("userLogin"))
    return render(request,"user.html",locals())
def register(request):
    return HttpResponse("抱歉，目前还不支持自发注册")
#登录界面
def logIn(request):
    title="登录系统"
    pageTitle="用户登录"
    button="登录"
    urlText="用户注册"
    urlName="register"
    if request.method=="POST":
        u=request.POST.get("username","")
        p=request.POST.get("password","")
        if MyUser.objects.filter(username=u):
            user=authenticate(username=u,password=p)
            if user:
                login(request,user)
                kwargs={"id":request.user.id,"page":1}
                #return redirect(reverse("article",kwargs=kwargs))
                #return HttpResponse("这里可以转到详情页首页")
                return HttpResponseRedirect("/data_record/index")
            else:
                tips="账号密码错误，请重新输入"
        else:
            tips="用户不存在，请联系管理员进行注册"

    else:
        if request.user.username:
            kwargs={"id":request.user.id,"page":1}
            #return redirect(reverse("article"))
    return render(request,"user.html",locals())

@login_required()
def changePassword(request):
    #首先检查当前是post还是get
    if request.method=="POST":
        #获取用户名
        u=request.POST.get("username","")
        #获取原密码
        p=request.POST.get("password","")
        #获取新的密码
        n=request.POST.get("newpass","")
        if MyUser.objects.filter(username=u):
            print("uuuuuuuuuuu",u,p)
            user=authenticate(username=u,password=p)
            print("uuuuu22222222",user)
            if user.is_active:
                #d={"username":u,"password":n,"is_superuser":0,"is_staff":1}
                usern=MyUser.objects.get(username=u)
                usern.set_password(n)
                usern.save()
                tips="密码修改成功"
            else:
                tips="密码错误，请重新输入"
        else:
            tips="用户不存在"
        return render(request,"changePassword_msg.html",locals())
    else:
        return render(request,"changePassword.html")


#定义一个退出的function
@login_required
def logoutRequest(request):
    logout(request)
    return HttpResponseRedirect("/user/login.html")


