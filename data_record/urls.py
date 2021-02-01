from django.urls import path, re_path
from . import views


app_name = "data_record"
urlpatterns = [
    path("index/", views.index, name="index"),
    path("del_his", views.del_his, name="delhistory"),
    # path('download/',views.download_data,name="show_all_data"),
    path('download/', views.download_data, name="download"),
    path("logout/", views.logoutRequest, name="logout"),
    path('log_in/', views.log_in, name="log_in"),
    path(
        "cdr_info/<int:page>/<str:order_type>",
        views.cdr_info,
        name="cdrinfo"),
    path('data_analysis/', views.data_analysis, name="data_analysis"),
    path('display/', views.display, name="display"),
    path('contact/', views.contact, name="contact"),
    path('search-form/', views.search_form, name="search_form"),
    path('search/', views.search, name="search"),
    path('upload/', views.upload, name="upload"),
    path('upload_file/', views.upload, name="upload"),
    path('chagepasswd/', views.chagepasswd, name="chagepasswd"),
    path('<int:History_id>/', views.detail, name="detail"),
    path('<int:History_id>/result/', views.result, name="result"),
    path('<int:History_id>/vote/', views.vote, name="vote"),
]
