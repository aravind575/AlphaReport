from django.contrib import admin
from django.urls import path, include, re_path

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


"""
Can implement a robust health check to be used in CI / CD, all included in one regex path.

For reference:

DatabaseView, CacheView, CeleryView, StorageView,
CustomHealthCheckView, FileView, RedisView, ElasticsearchView,
SolrHealthCheckView, SSLOpenSSLView, SSLLibresslView, SSLLibresslProbeView
"""

urlpatterns = [
    path('admin/', admin.site.urls),

    # search and report urls, point to api app
    path('', include('api.urls')),

    # health-check urls
    re_path(r'^ht/', include('health_check.urls')),

    # openapi schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional (Swagger/Redoc) UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]