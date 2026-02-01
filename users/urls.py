from django.urls import path
from users import views

urlpatterns = [
    path('create_user/',views.create_user,name='create_user'),
    path('update_user/',views.update_user,name='update_user'),
    path('delete_user/',views.soft_delete_user,name='delete_user'),
    path('get_users/',views.view_users,name='view_users'),
    path('logout/',views.logout_view,name='logout'),
    path('request_reset/',views.password_reset_request,name='request_reset'),
    path('password/reset/',views.password_reset,name='password_reset'),
]
