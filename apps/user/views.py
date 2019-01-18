from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
from django.conf import settings
from django.views.generic import View
from django.core.urlresolvers import reverse
import re
from user.models import User
from utils.mixin import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail


class Register(View):
    """
    注册视图
    """

    def get(self, request):
        return render(request, 'user/register.html')

    def post(self, request):
        """
        user_name mark
        pwd happy2018
        cpwd happy2018
        email sdf
        allow on
        """
        # 接收参数
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        cpassword = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 校验参数

        # 用all()函数校验是不是每个参数都有值
        if not all([username, password, cpassword, email, allow]):
            return render(request, 'user/register.html', {'errmsg': '数据不完整'})

        if not password == cpassword:
            return render(request, 'user/register.html', {'errmsg': '两次输入的密码不一致'})

        # 用户名校验
        try:
            user = User.objects.get(username=username)
            print(user.username)
        except User.DoesNotExist:
            user = None

        # 用户名已经存在
        if user:
            return render(request, 'user/register.html', {'errmsg': '用户名已经存在'})

        # -------------------------邮箱校验------------------------
        ret = re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email)
        if not ret:
            return render(request, 'user/register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 业务逻辑处理
        # User继承Abstarct user  可以使用create_user方法
        user = User.objects.create_user(username, email, password)
        # 设置为未激活状态
        user.is_active = 0
        user.save()

        # 激活邮件
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)
        to_email_list = ['154268875@qq.com']

        # 使用celery发邮件
        from celery_tasks.tasks import send_register_activate_email
        send_register_activate_email.delay(to_email_list, token.decode(), user.username)
        # self.send(token.decode(), user.username)
        # 响应
        return redirect(reverse('goods:index'))

    def patch(self, request, *args, **kwargs):
        print("patch 请求方式")
        # from django.http import HttpRequest as req

    def send(self, token, username):
        _subject = '天天生鲜网注册激活'
        _message = ''
        _from = settings.EMAIL_FROM
        _to = ['154268875@qq.com']
        _msg = '{},您好！欢迎注册天天生鲜网会员，<a href="http://127.0.0.1:8000/user/activate/{}" ' \
               'target="_blank">&lt点击激活&gt</a>&nbsp&nbsp&nbsp，此链接1小时内有效。'.format(username, token)
        send_mail(subject=_subject, message=_message, from_email=_from, recipient_list=_to, html_message=_msg)


# /user/activate/token
class ActivateView(View):
    '''激活'''

    def get(self, request, token):

        serializer = Serializer(settings.SECRET_KEY, 3600)

        try:
            info = serializer.loads(token)
            print(info)
            user = User.objects.get(id=info.get('confirm'))
            user.is_active = 1
            user.save()

            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse('激活链接已失效')


# /user/login/
class LoginView(View):
    """ 登录  """

    def get(self, request):
        """ 去登录页面 """
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        return render(request, 'user/login.html', {'username': username, 'checked': checked})

    def post(self, request):
        """ 登录业务 """

        username = request.POST.get('username')
        password = request.POST.get('pwd')

        if not all([username, password]):
            return render(request, 'user/login.html', {'errmsg': '数据不完整'})

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                next_url = request.GET.get('next', reverse('goods:index'))

                response = redirect(next_url)

                remember = request.POST.get('remember')

                if remember == 'on':
                    response.set_cookie('username', username, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie('username')
                return response
            else:
                return render(request, 'user/login.html', {'errmsg': '账号未激活'})
        else:
            return render(request, 'user/login.html', {'errmsg': '用户名或密码不正确'})
        # try:
        #     user = User.objects.get(username=username, password=password)
        # except User.DoesNotExist as e:
        #     return render(request, 'user/login.html', {'errmsg': '用户名或密码不正确'})
        #
        # if user:
        #     return HttpResponse('login ok')


# /user/user
class UserCenter(LoginRequiredMixin, View):
    def get(self, request):
        context = {'page': 'user'}
        return render(request, 'user/user_center_info.html', context)


# /user/order
class OrderView(LoginRequiredMixin, View):
    """ 用户中心 订单 """

    def get(self, request):
        context = {'page': 'order'}
        return render(request, 'user/user_center_order.html', context)


# /user/address
class AddressView(LoginRequiredMixin, View):
    """ 用户中心 地址 """

    def get(self, request):
        context = {'page': 'address'}
        return render(request, 'user/user_center_site.html', context)
