"""django_tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views #import the user views directly here rather than use include
from users.views import LoginView, registerProfile



urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name="register"),
    path('create/profile', registerProfile, name='signup_profile'),
    path('profile/edit/', user_views.profile, name="edit-profile"),
    # this is a class-based view (as_view is a function that directs where the url should look for the template)
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset.html'), name="password_reset"
        ),
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'), name="password_reset_done"
        ),
    path('password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'), name="password_reset_confirm"
        ),
    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'), name="password_reset_complete"
        ),
    path('', include('blog.urls')), #the include function processes the url and sends to the blogs url file for processing.
    path('', include('activity.urls')),
    path('', include('comments.urls')),
    path('', include('relationships.urls')),
    path('api/', include('activity.api.urls')),
    path('notifications/', include('notify.urls', namespace='notifications')),
    path('api-auth/', include('rest_framework.urls')),

]
#leaving the url string empty makes it the default home page i.e localhost:8000

#Deloying static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)