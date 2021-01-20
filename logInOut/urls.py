from django.urls import path

from logInOut.views import logIn

urlpatterns=[
	path("",logIn)
]
