from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from apps.user import views

urlpatterns = [
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^activate/(?P<token>.*)$', views.ActivateView.as_view(), name='activate'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^$', login_required(views.UserCenter.as_view()), name='user'),
    url(r'^order/$', login_required(views.OrderView.as_view()), name='order'),
    url(r'^address/$', login_required(views.AddressView.as_view()), name='address'),
]
