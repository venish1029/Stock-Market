from django.urls import path
from . import views

urlpatterns=[
    path('',views.index),
    path('user_login',views.user_login),
    path('admin_Homepage',views.admin_Homepage),
    path('search_save',views.search_save),
    path('save_details/<str:code>/',views.save_details),
    path('search_data/<str:code>/',views.search_data),
    path('sell_items/<str:code>',views.sell_items),
    path('details',views.detail),
]