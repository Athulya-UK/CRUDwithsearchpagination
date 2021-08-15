from django.urls import path
from . import views
app_name = 'studymaterial'
urlpatterns = [
    path('youtube',views.youtube, name='youtube'),
    path('books',views.books,name="books"),
    path('dictionary',views.dictionary,name="dictionary"),
    path('wikipedias',views.wikipedias,name="wikipedias"),
    path('joinmeeting',views.joinmeeting,name="joinmeeting"),
    path('googleform',views.googleform,name="googleform"),
]