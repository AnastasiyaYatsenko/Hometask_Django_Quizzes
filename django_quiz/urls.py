from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path
from quiz import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, )

app_name = 'quiz'

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', views.TestListView.as_view(), name='index'),
    path('api/', include('api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('add', views.CreateTestView.as_view(), name='create_test'),
    path('add_question', views.CreateQuestionView.as_view(), name='create_question'),
    path('search', views.SearchTestView.as_view(), name='search'),
    path('filter', views.FilterTestView.as_view(), name='filter'),
    path('run_<test_id>', views.CreateTestrunView.as_view(), name='run_test'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('admin/', admin.site.urls)
]
