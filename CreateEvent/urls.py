from django.urls import path
from . import views

app_name = 'CreateEvent'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/<int:event_id>/', views.register_student, name='register_student'),
]