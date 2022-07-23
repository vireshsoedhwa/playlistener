"""fileuploader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from apiv1 import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/', include('apiv1.urls')),
    # path('', include('frontend.urls'))
]

if settings.DEBUG:
    # OPENAPI
    # PATTERNS
    # UI:
    urlpatterns += [
        # path('api/', SpectacularSwaggerView.as_view(url_name='schema'),
        #      name='swagger-ui'),
        # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('admin/', admin.site.urls)
    ]
# else:
#     urlpatterns += [path('', views.RootPath.as_view(), name='root')]

# handler404 = 'apiv1.views.view_404'
