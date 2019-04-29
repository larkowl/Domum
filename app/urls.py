from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('announcement/<int:pk>/', views.AnnouncementDetailView.as_view(), name='announcement_view'),
    path('users/<int:pk>/', views.profile_view, name='profile'),
    path('users/edit<int:pk>', views.profile_edit, name='profile_edit'),
    path('announcement/new/', views.new_announcement, name='new_announcement'),
    path('announcement/edit<int:pk>/', views.announcement_edit, name="announcement_edit"),
    path('accounts/new', views.signup, name="registration"),
    path('users/change<int:pk>', views.change_password, name='change_password'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]