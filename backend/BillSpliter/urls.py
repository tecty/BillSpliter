"""BillSpliter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
# bill views
from Bills.views import UserViewSet,\
    TransactionViewSet, BillViewSet,\
    BriefTransactionViewSet, SettleTransactionViewSet,\
    SettlementViewSet
from BillGroups.views import GroupViewSet
# urls
from django.views import generic
# jwt route 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



# main router
router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('groups', GroupViewSet)
router.register('trans', TransactionViewSet)
router.register('bills', BillViewSet)
router.register('brief_tr', BriefTransactionViewSet)
router.register('settle_tr', SettleTransactionViewSet)
router.register('settlement', SettlementViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^v0/', include(router.urls)),
    url(r'^v0/jwt/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^v0/jwt_refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
]
