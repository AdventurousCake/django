from django.urls import path
from . import views, views_likes

app_name = 'form_msg'

# NOT DRF API
urlpatterns = [
    path('send/', views.MsgFormView.as_view(), name='send_msg'),
    # path('send/', views.send_msg, name='send_msg'),

    path('edit/<int:pk>/', views.UpdateMsgView.as_view(), name='edit_msg'),
    # path('edit/<int:pk>/', views.edit_msg, name='edit_msg'),

    path('delete/<int:pk>/', views.DeleteMsgView.as_view(), name='delete_msg'),
    # path('delete/<int:pk>/', views.delete_msg, name='delete_msg'),

    # path('', views.msg_list, name='msg_list'),
    path('', views.MsgList.as_view(), name='msg_list'),

    path('<int:pk>/', views.DetailMsgView.as_view(), name='show_msg'),
    # path('<int:pk>/', views.get_msg, name='show_msg'),


    # TODO LIKES
    path('like/<int:pk>/', views_likes.UpdateLikeView.as_view(), name='like'),


    path("signup/", views.SignUp.as_view(), name="signup"),
    path("users/<int:pk>/", views.UserDetails.as_view(), name="users_details"),

]