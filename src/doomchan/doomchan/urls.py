from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
#from django.utils.translation import gettext_lazy as _

from rest_framework.documentation import include_docs_urls

urlpatterns = i18n_patterns(
    path('api/', include('apps.imageboard.api.urls')),
    path('api/auth/', include('rest_framework.urls')),
    path('api/docs/', include_docs_urls()),
    path('rosetta/', include('rosetta.urls')),
    path('wow_wee/', admin.site.urls),
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
