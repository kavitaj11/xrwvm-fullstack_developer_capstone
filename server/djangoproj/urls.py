from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ✅ Backend app routes FIRST
    path("", include("djangoapp.urls")),
    # ✅ Static frontend template pages
    path(
        "about/",
        TemplateView.as_view(template_name="djangoapp/about.html"),
        name="about",
    ),
    path(
        "contact/",
        TemplateView.as_view(template_name="djangoapp/contact.html"),
        name="contact",
    ),
    path("dealers/", TemplateView.as_view(template_name="index.html")),
    path(
        "postreview/<int:dealer_id>", TemplateView.as_view(
            template_name="index.html")
    ),
    path(
        'register/', 
         TemplateView.as_view(template_name="register.html")
    ),
    path("admin/", admin.site.urls),
]

# ✅ Allow static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
