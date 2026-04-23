from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

# 👉 Redirect /accounts/ to login page
def accounts_home(request):
    return redirect('login')


urlpatterns = [
    path('admin/', admin.site.urls),

    # Job app
    path('job/', include('job.urls')),

    # Auth system (login/logout/password reset)
    path('accounts/', include('django.contrib.auth.urls')),

    # Redirect root accounts page
    path('accounts/', accounts_home),
]

# 👉 Media files (IMPORTANT for images)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)