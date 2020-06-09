from django.urls import path

from . import views

app_name = 'links'

urlpatterns = [
    path('', views.LinkListView.as_view(), name='home'),

    path('users/<slug>/', views.ProfileDetailView.as_view(), name='profile'),
    path('edit-profile/',
         views.ProfileEditView.as_view(),
         name='edit_profile'),

    path('link/create/',
         views.LinkCreateView.as_view(),
         name='create'),
    path('link/<int:pk>/',
         views.LinkDetailView.as_view(),
         name='detail'),
    path('link/<int:pk>/update',
         views.LinkUpdateView.as_view(),
         name='update'),
    path('link/<int:pk>/delete',
         views.LinkDeleteView.as_view(),
         name='delete'),

    path('vote/', views.VoteFormView.as_view(), name='vote'),
]
