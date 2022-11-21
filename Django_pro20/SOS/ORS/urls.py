from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('auth/<page>/',views.auth),
    path('<page>/<action>/',views.action),
    path('<page>/<operation>/<int:id>',views.actionId),
    path('<page>/',views.actionId),

]

