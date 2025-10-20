from django.http import JsonResponse
from django.shortcuts import render, redirect

from user.models import TUser
from util.md5Util import MD5Utility

from datetime import datetime

# Create your views here.


def index(request):
    return render(request,'hello2.html')

def Jinja3test(request):
    str = "Jinja3测试"
    myDict = {"tom": '666', 'cat': '999', 'wzw': '333'}

    content_value = {"title": str, "msg2": myDict}
    return render(request, 'test_jinja3.html', context=content_value)

# 处理登录业务
def login(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username is None or username.strip()=='':
            return JsonResponse({'code':404,'info':'用户名不能为空！','error':True})
        if password is None or password.strip()=='':
            return JsonResponse({'code':404,'info':'密码不能为空！','error':True})

        try:
            # 传入密码时，记得解密
            curUser = TUser.objects.get(username=username, password=MD5Utility.encrypt(password))
            request.session["username"]=username    # 在session中保存用户名以便于之后的页面进行访问
            return JsonResponse({'code': 200, 'info': 'ok','success':'True'})
        except Exception as e:
            print(e)
            return JsonResponse({'code':404,'info':'用户名或者密码错误','error':True})


# 处理注册业务
def register(request):
    """
    用户注册
    :param request:
    :return:
    """
    if request.method=='GET':
        return render(request,'register.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if username is None or username.strip() == '':
            return JsonResponse({'code': 404, 'info': '用户名不能为空！', 'error': True})
        if password is None or password.strip() == '':
            return JsonResponse({'code': 404, 'info': '密码不能为空！', 'error': True})
        if password2 is None or password2.strip() == '':
            return JsonResponse({'code': 404, 'info': '确认密码不能为空！', 'error': True})

        curUser = TUser.objects.filter(username=username)
        if len(curUser): # 查询是否存在该用户名
            return JsonResponse({'code': 404, 'info': '用户名已存在', 'error': True})

        try:
            # 传入密码时，记得解密
            add_user=TUser(username=username,password=MD5Utility.encrypt(password),createtime=datetime.now())
            add_user.save()
            return JsonResponse({'code': 200, 'info': 'ok', 'success': 'True'})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 404, 'info': '服务器异常！', 'error': True})


def logout(request):
    """
    安全退出注销
    :param request:
    :return:
    """
    request.session.clear()
    return redirect('/user/login')




