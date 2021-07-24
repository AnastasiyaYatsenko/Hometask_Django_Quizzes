from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from quiz import views

app_name = 'quiz'

urlpatterns = [
    path('', views.TestListView.as_view(), name='index'),
    path('add', views.CreateTestView.as_view(), name='create_test'),
    path('add_question', views.CreateQuestionView.as_view(), name='create_question'),
    path('search', views.SearchTestView.as_view(), name='search'),
    path('filter', views.FilterTestView.as_view(), name='run_test'),
    path('run_<test_id>', views.CreateTestrunView.as_view(), name='run_test'),
    path('admin/', admin.site.urls)
]
#if settings.DEBUG:
#    import debug_toolbar
#    urlpatterns = [
#     path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
