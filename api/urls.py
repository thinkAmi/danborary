from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import NdlApiView, PackingApiView

app_name = 'api'

router = DefaultRouter()
router.register(r'packing/v1', PackingApiView)

urlpatterns = [
    # ViewSet系
    path('', include(router.urls)),
    # それ以外
    path('ndl/', NdlApiView.as_view(), name='api-ndl'),
]
