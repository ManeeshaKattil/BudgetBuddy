
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('login_get/', views.login_get),
    path('logout_get/', views.logout_get),
    path('admin_home_get/', views.admin_home_get),
    path('manage_expert_get/', views.manage_expert_get, ),
    path('manage_expert_post', views.manage_expert_post, ),
    path('view_users_get/', views.view_users_get, ),
    path('view_feedback_get/', views.view_feedback_get, ),
    path('view_feedback_post', views.view_feedback_post, ),
    path('complaint_get/', views.complaint_get,),
    path('complaint_post', views.complaint_post,),
    path('add_expert_get/', views.add_expert_get),
    path('manage_tips_get/', views.manage_tips_get),
    path('manage_tips_post', views.manage_tips_post),
    path('add_suggestions_get/', views.add_suggestions_get),
    path('expert_home_get/', views.expert_home_get),
    path('expert_feedback_get/', views.expert_feedback_get, ),
    path('expert_feedback_post', views.expert_feedback_post, ),
    path('insert_tips_get/', views.insert_tips_get),
    path('expert_view_user_get/', views.expert_view_user_get),
    path('expert_view_user_post', views.expert_view_user_post),
    path('view_user_details_get/<id>', views.view_user_details_get),
    path('add_expert_post/',views.add_expert_post),
    path('add_suggestions_post/',views.add_suggestions_post),
    path('insert_tips_post/',views.insert_tips_post),
    path('login_post/',views.login_post),
    path('delete_tips/<id>',views.delete_tips),
    path('edit_tips/<id>',views.edit_tips),
    path('edit_tips_post/',views.edit_tips_post),
    path('edit_expert/<id>',views.edit_expert),
    path('edit_expert_post/',views.edit_expert_post),
    path('delete_expert/<id>',views.delete_expert),
    path('reply_get/<id>',views.reply_get),
    path('reply_post/',views.reply_post),
    path('view_report_get/<id>',views.view_report_get),
    path('view_report_post/',views.view_report_post),

    path('user_register/',views.user_register),
    path('user_login/',views.user_login),
    path('viewtips/',views.viewtips),
    path('add_feedback/',views.add_feedback),
    path('viewfeedback/',views.viewfeedback),
    path('viewsuggestion/',views.viewsuggestion),
    path('add_reminder/',views.add_reminder),
    path('view_reminder/',views.view_reminder),
    path('add_complaint/', views.add_complaint),
    path('view_complaint/',views.view_complaint),
    path('add_income_expense/', views.add_income_expense),
    path('view_expense/', views.view_expense),
    path('viewExpert/', views.viewExpert),
    path('set_goal/', views.set_goal),
    path('view_goal/', views.view_goal),
    path('view_report/', views.view_report),
    path('viewProfile/', views.viewProfile),
    path('viewProfile/', views.viewProfile),
    path('edit_profile/', views.edit_profile),
    path('delete_income/', views.delete_income),
    path('delete_reminder/', views.delete_reminder),
    path('delete_goal/', views.delete_goal),
    path('forecast/', views.forecast),
    path('forecast1/', views.forecast1),
    path('user_get_notification/', views.user_get_notification),



    path('expert_chat_withuser/<id>', views.expert_chat_withuser),
    path('chat_view/', views.chat_view),
    path('chat_send/', views.chat_send),


    path('User_viewchat/', views.User_viewchat),
    path('User_sendchat/', views.User_sendchat),


    path('forgotpasswordflutter/', views.forgotpasswordflutter),
    path('verifyOtpflutterPost/', views.verifyOtpflutterPost),
    path('changePasswordflutter/', views.changePasswordflutter),

    path('forgotPassword/', views.forgotPassword),
    path('forgotPassword_otp/', views.forgotPassword_otp),
    path('verifyOtp/', views.verifyOtp),
    path('verifyOtpPost/', views.verifyOtpPost),
    path('new_password/', views.new_password),
    path('changePassword/', views.changePassword),





]
