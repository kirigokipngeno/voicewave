from django.urls import path

from polls.views import AdminLoginView, AdminLogoutView
from users import views as user_views
from django.contrib.auth import views as auth_views
from users import views as user_views
from polls import views as polls_views
app_name = 'users'
urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('change_password/', user_views.change_password, name='change-pass'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path('contact/', user_views.contact, name='contact'),
path('admin_dashboard/', polls_views.admin_dashboard, name='admin_dashboard'),
    path('<int:question_id>/', polls_views.detail, name='detail'),
    path('<int:question_id>/results/', polls_views.results, name='results'),
    path('close_voting/<int:question_id>/', polls_views.close_voting, name='close_voting'),
    path('continue_voting/<int:question_id>/', polls_views.continue_voting, name='continue_voting'),
    path('admin_login/', AdminLoginView.as_view(), name='admin_login'),
    path('admin_logout/', AdminLogoutView.as_view(), name='admin_logout'),
    path('contact/', user_views.contact, name='contact'),
    path('contact_success/',user_views.contact_success, name='contact_success'),
    path('contact_list/',user_views.contact_list, name='contact_list'),  # Admin view for listing contacts
]
