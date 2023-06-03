"""
URL configuration for socialnetwork project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
import allauth.account
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import user_signup_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', user_signup_view, name='signup'),
    path('account/', include('accounts.urls')),
    path('accounts/', include('allauth.account.urls')),
    path('', include('posts.urls')),
    path('groups/', include('groups.urls')),
    path('chats/', include('chats.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
