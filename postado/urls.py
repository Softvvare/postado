from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('app/', include('app.urls')),
    path('chat/', include('chat.urls')),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='templates/password/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='templates/password/password_reset_confirm.html'),
        name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='templates/password/password_reset_form.html',
        email_template_name='templates/password/password_reset_email.html',
        success_url=reverse_lazy('password_reset_done'),
        subject_template_name='templates/password/password_reset_subject.txt'), name='password_reset'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='templates/password/password_reset_complete.html'),
         name='password_reset_complete'),

] + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
