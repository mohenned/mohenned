"""iam URL Configuration

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
from django.urls import path,include
from django.contrib.auth.views import PasswordResetView ,PasswordResetDoneView ,PasswordResetConfirmView,PasswordResetCompleteView
from legend import views
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('',views.home , name = 'home'),
    path('accounts/password_reset/',PasswordResetView.as_view(template_name='reset/password_reset_form.html',subject_template_name='reset/password_reset_subject.txt',
             email_template_name='reset/password_reset_email.html'),name='password_reset'),
    path('accounts/password_reset/done',PasswordResetDoneView.as_view(template_name='reset/password_reset_done.html'),name='password_reset_done'),
    path('accounts/password_reset/confirm/<uidb64>/<token>',PasswordResetConfirmView.as_view(template_name='reset/password_reset_confirm.html'),name='password_reset_confirm'),
    path('accounts/password_reset/complete',PasswordResetCompleteView.as_view(template_name='reset/password_reset_complete.html'),name='password_reset_complete'),
    path('accounts/change-password/', auth_views.PasswordChangeView.as_view(template_name='reset/change_password.html'),name='password_change'),
    path('accounts/change-password/done', auth_views.PasswordChangeDoneView.as_view(template_name='reset/change_password_done.html'),name='password_change_done'),
    path('', include('legend.urls')),
    path('logout/', views.user_logout, name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
