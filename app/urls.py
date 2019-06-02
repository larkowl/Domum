from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.AnnouncementsListView.as_view(), name='post_list'),
    path('announcement/<int:pk>/', views.AnnouncementDetailView.as_view(), name='announcement_view'),
    path('announcement/new/', views.new_announcement, name='new_announcement'),
    path('announcement/edit<int:pk>/', views.announcement_edit, name="announcement_edit"),
    path('accounts/new', views.signup, name="registration"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]