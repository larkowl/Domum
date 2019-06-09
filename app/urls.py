from django.urls import path, include
from . import views
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('', views.land, name='land'),
    path('pay/', views.payment, name='pay'),
    path('pay-callback/', views.check, name='pay-callback'),
    path('announcements/<int:pk>/', views.post_list, name='post_list'),
    path('announcements/', views.post_list, name='post_list'),
    path('announcement/<int:pk>/', views.announcement_view, name='announcement_view'),
    path('users/<int:pk>/', views.profile_view, name='profile'),
    path('users/edit<int:pk>', views.profile_edit, name='profile_edit'),
    path('announcement/new/', views.new_announcement, name='new_announcement'),
    path('announcement/edit<int:pk>/', views.announcement_edit, name="announcement_edit"),
    path('accounts/new', views.signup, name="registration"),
    path('users/change<int:pk>', views.change_password, name='change_password'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]

if settings.DEBUG:
    urlpatterns += [url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),]
