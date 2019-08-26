"""etherapie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path
from django.views.generic import TemplateView


handler404 = TemplateView.as_view(template_name="error/404.html")
handler403 = TemplateView.as_view(template_name="error/403.html")

urlpatterns = [
    path('FAQ', TemplateView.as_view(template_name="FAQ.html"), name="FAQ"),
    path('', TemplateView.as_view(template_name="home.html"), name="home"),
    path('choix', TemplateView.as_view(template_name="choix.html"), name="choix"),
    path('contact', TemplateView.as_view(template_name="contact.html"), name="contact"),
    path('admin/', admin.site.urls),
    ################################## Inclusion des applications liés ###########################################
    path('user/', include('user.urls')),
    path('module/', include('module.urls')),
    ################################## Ckeditor ###########################################
    path("ckdeditor", include('ckeditor_uploader.urls'))
]

from django.conf import settings

if settings.DEBUG:
    import debug_toolbar
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.conf.urls.static import static
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()
