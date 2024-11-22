from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path("", views.landing_page, name="landing"),
    path("posts/", views.posts_page, name="posts"),
    path('tutorials/', views.tutorials, name='tutorials'),
    path("tutorial/<int:tutorial_id>/", views.tutorial_detail, name="tutorial_detail"), 
    path('login/', views.login_view, name='login'),
    path("logout/", views.logout_user, name="logout"),
    path('post/<int:blog_id>/add_comment/', views.add_comment, name='add_comment'),
    path('tutorial/<int:tutorial_id>/add_comment/', views.add_tutorial_comment, name='add_tutorial_comment'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('mentorship/', views.mentorship, name='mentorship'),
    path('chat/<int:id>/<str:id_type>/', views.chat_detail, name='chat_detail'),
    path('chat/send_message/<int:chat_id>/', views.send_message, name='send_message'),
    path('profiles/', views.profiles, name='profiles'),
    path('journalist/<int:id>/', views.journalist_detail_view, name='journalist_detail'),
]
