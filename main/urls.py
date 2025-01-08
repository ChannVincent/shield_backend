
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", RedirectView.as_view(url="admin/", permanent=True)),
    path("admin/", admin.site.urls),
    path("security/", include("security_data.urls")),
    path("posts/", include("posts.urls")),
    path("auth/", include("user.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

