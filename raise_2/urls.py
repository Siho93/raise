from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'), #from raise_2/.....
    path('mein_konto/', views.mein_konto, name='mein_konto'),
    path('favoriten/', views.favoriten, name='favoriten'),
    path('market/', views.market, name='market'),
    path('wertschrift/<int:id>/', views.wertschrift, name='wertschrift'),
    path('plan/', views.plan, name='plan'),
    path('einstellungen/', views.einstellungen, name='einstellungen'),
    path('trade/<int:id>/', views.trade, name='trade'),
    path('plan_form/<int:id>/', views.plan_form, name='plan_form'),
    path('login/', auth_views.login, name='login'),
    path('register/', views.signup, name='register'),
    path('register/signup', views.signup, name='signup'),
    path('compute', views.compute, name='compute'),
    path('raise', views.raise_main, name='raise'),
    path('favoriten/<int:id>/', views.favorisieren, name='favorisieren'),
    path('plan/delete/<int:id>/', views.deleteplan, name='deleteplan'),
    path('favoriten/delete/<int:id>/', views.deletefavorit, name='deletefavorit'),
    path('buy/delete/<int:id>/', views.deletebuy, name='deletebuy'),
    path('sell/delete/<int:id>/', views.deletesell, name='deletesell'),
    #path('<int:share_id>/', views.share, name='share'),
]

