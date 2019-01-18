# import Celery
from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
import time

# create an instance Celery
celery_obj = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/3')

'''
# ------------------------------
import os
import django

#  添加配置文件到环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')
# 初始化django
django.setup()

# -------------------
'''


# define task function
@celery_obj.task
def send_register_activate_email(to_email_list, token, username):
    _subject = '天天生鲜网注册激活'
    _message = ''
    _from = settings.EMAIL_FROM
    _to = to_email_list
    _msg = '{},您好！欢迎注册天天生鲜网会员，<a href="http://127.0.0.1:8000/user/activate/{}" ' \
           'target="_blank">&lt点击激活&gt</a>&nbsp&nbsp&nbsp，此链接1小时内有效。'.format(username, token)
    send_mail(subject=_subject, message=_message, from_email=_from, recipient_list=_to, html_message=_msg)
    # time.sleep(5)


'''
启动worker
celery -A celery_tasks.tasks worker -l info
'''
