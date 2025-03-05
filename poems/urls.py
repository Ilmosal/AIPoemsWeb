from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('answer/<answer_code>', views.poem, name="poem"),
    path('start/', views.start, name="start"),
    path('next/<answer_code>', views.next, name="next"),
    path('results/<answer_code>', views.results, name="results"),
]
