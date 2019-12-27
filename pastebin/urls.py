from django.urls import path

from . import views

app_name = 'pastebin'
urlpatterns = [
	path('', views.index, name='index'),
	path('create/', views.create, name='create'),
	path('latest/', views.latest, name='latest'),
	path('<int:paste_id>/', views.details, name='details'),
	path('<int:paste_id>/dl', views.download, name='download'),
	path('<int:paste_id>/raw', views.raw, name='raw'),
]
