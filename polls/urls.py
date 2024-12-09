from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('<int:question_id>/close_election/', views.close_election, name='close_election'),
    path('<int:question_id>/continue_voting/', views.continue_voting, name='continue_voting'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('resultsdata/<str:obj>/', views.resultsData, name='resultsdata'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('close_voting/<int:question_id>/', views.close_voting, name='close_voting'),
    path('continue_voting/<int:question_id>/', views.continue_voting, name='continue_voting'),
    path('admin_results/', views.admin_results, name='admin_results'),
]
