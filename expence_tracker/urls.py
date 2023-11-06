from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('bar_chart', views.bar_chart, name="bar_chart"),
    path('add-new-expense', views.add_new_expence, name="add_new_expence"),
    path('calculate-expence-reward', views.calculate_expence_reward, name="calculate_expence_reward")
]
