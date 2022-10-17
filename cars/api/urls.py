from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from api import views

app_name = 'api'

schema_view = get_schema_view(
    openapi.Info(
        title="Cars API",
        default_version='v1',
        description=(
            "Справочники по автомобилям."
        ),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'colors', views.ColorViewSet)
router.register(r'manufacturers', views.ManufacturerViewSet)
router.register(r'models', views.CarModelViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'
    ),
    re_path(
        r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
]
