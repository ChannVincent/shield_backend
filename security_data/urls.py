from django.urls import path

from . import views

urlpatterns = [
    path("communes/", views.CommuneListView.as_view(), name="communes"),
]