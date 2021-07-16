from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from quiz import views
urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.create_test, name='create_test'),
    path('admin/', admin.site.urls)
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
     path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
