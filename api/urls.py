from django.urls import include, path

from api.spectacular.urls import urlpatterns as doc_urls
from organizations.urls import urlpatterns as organization_urls
from vacations.urls import urlpatterns as vacation_urls
from users.urls import urlpatterns as user_urls

app_name = 'api'

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += doc_urls
urlpatterns += organization_urls
urlpatterns += vacation_urls
urlpatterns += user_urls
