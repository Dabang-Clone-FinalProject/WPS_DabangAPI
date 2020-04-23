"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from config import settings
from members import views
from members.urls import urlpatterns_members
from posts import apis
# from posts.apis import PostRoomViewSet, PostAddressViewSet
from posts.urls import urlpatterns_posts

# router = routers.DefaultRouter()
# router.register(r'postroom', PostRoomViewSet)
# router.register(r'postaddress', PostAddressViewSet)

urlpatterns = [
    # path('auth/', include('rest_framework_social_oauth2.urls')), # rest_framework_social_oauth2

    path('api/token/', obtain_jwt_token),  # djangorestframework-jwt
    path('api/token/verify/', verify_jwt_token),  # djangorestframework-jwt
    path('api/token/refresh/', refresh_jwt_token),  # djangorestframework-jwt

    path('admin/', admin.site.urls),
    path('members/', include(urlpatterns_members)),
    path('posts/', include(urlpatterns_posts)),
    path('login/', views.login_page, name='login-page'),  # kakao access token 받기 위한 template
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns += [
    path('sentry-debug/', trigger_error),
]
