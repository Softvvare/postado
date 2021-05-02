from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('app/', include('app.urls')),
    #path('login/', views.login_request, name="login"),
    # path('logout/', auth_views.LogoutView.as_view(template_name='templates/logout.html'), name='logout'),
] + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
