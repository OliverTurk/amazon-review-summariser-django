from django.urls import path
from .views import get_summary

urlpatterns = [
    path('summary/', get_summary, name='get_summary')
]