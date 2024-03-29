from django.contrib.auth.views import LogoutView, PasswordChangeDoneView, PasswordResetCompleteView, \
    PasswordResetDoneView


from .views import Login, PasswordChange, PasswordReset, ResetConfirm, Profile
from django.urls import path

app_name = "authentication"
urlpatterns = [
    path('profile/', Profile.as_view(), name='profile'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset/<uidb64>/<token>/', ResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset/complete/',
         PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password_reset/', PasswordReset.as_view(), name='password_reset'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='auth/password_change_done.html'),
         name='password_change_done'),
    path('password_change/', PasswordChange.as_view(), name='password_change'),

]
