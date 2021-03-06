"""djangobackend URL Configuration

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
from django.urls import include, path, re_path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'assets', views.AssetViewSet)
router.register(r'vulnstatus', views.VulnStatusViewSet)

urlpatterns = [
    # re_path(r'^$', views.home, name='home'),
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^vulnerabilities/$', views.VulnerabilityListView.as_view()),
    re_path(r'^assets/(?P<asset_pk>\d+)/vuln/(?P<vuln_pk>\d+)$', views.VulnStatusUpdateView.as_view(), name='status-update'),
    re_path(r'^dashboard/$', views.dashboard)
]
