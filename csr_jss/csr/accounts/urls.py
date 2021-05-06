from django.urls import path
from accounts import views

urlpatterns = [
	path('login/', views.LoginView, name='login'),
	path('logout/', views.LogoutView, name='logout'),
	path('change_password/', views.ChangePasswordView, name='change_password'),
	path('forgot_password/', views.ForgotPasswordView, name='forgot_password'),
	path('set_password/', views.SetPasswordView, name='set_password'),
	path('reset_password/', views.ResetPasswordView, name='reset_password'),
	path('add_user/', views.CreateuserView, name='add_user'),
	path('activate_user/<usr_id>', views.ActivateUserView, name='activate_user'),
	path('deactivate_user/<usr_id>', views.DeactivateUserView, name='deactivate_user'),
]