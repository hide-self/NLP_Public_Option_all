from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin



class UsernameAuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        white_list = ["/user/login/","/user/register/"]  # 请求白名单(无session时能访问的url)
        path = request.path
        if path not in white_list and not path.startswith("/media") and not path.startswith("/static"):
            print("要进行用户username验证")
            try:
                curUsername=request.session['username']
                print('当前用户为:{0}'.format(curUsername))
            except Exception as e:
                print('未进行登录,返回登录界面')
                return redirect("/user/login/")

        else:
            print("当前为登录/注册/静态文件/媒体文件的url，不进行session验证")
            return None
