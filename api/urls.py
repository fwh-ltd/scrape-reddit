from django.urls import path
from api import views

urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    path('dataget', views.dataget, name='callapi'),
    path('test', views.test_data, name='test'),
]
